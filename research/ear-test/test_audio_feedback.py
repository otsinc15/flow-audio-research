import base64
from contextlib import redirect_stderr
import http.client
import importlib.util
import io
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
from unittest.mock import MagicMock, patch
import urllib.error
import wave

spec = importlib.util.spec_from_file_location("audio_feedback", Path(__file__).with_name("audio-feedback.py"))
audio_feedback = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audio_feedback)


class AudioFeedbackTests(unittest.TestCase):
    def tagged_wav(self, path):
        samples = struct.pack("<" + "h" * 320, *([0, 1000, -1000, 500] * 80))
        with wave.open(str(path), "wb") as audio:
            audio.setnchannels(1)
            audio.setsampwidth(2)
            audio.setframerate(16000)
            audio.writeframes(samples)
        tags = b"INFO"
        for name, value in ((b"INAM", b"PRIVATE-REJECTED-SONG"), (b"IART", b"PRIVATE-ARTIST")):
            value += b"\0"
            tags += name + struct.pack("<I", len(value)) + value + (b"\0" if len(value) % 2 else b"")
        data = path.read_bytes() + b"LIST" + struct.pack("<I", len(tags)) + tags
        path.write_bytes(data[:4] + struct.pack("<I", len(data) - 8) + data[8:])
        return samples

    def test_only_anonymous_labels_are_sent(self):
        with tempfile.TemporaryDirectory() as directory:
            clip = Path(directory) / "private-filename-rejected.wav"
            samples = self.tagged_wav(clip)
            self.assertIn(b"PRIVATE-REJECTED-SONG", clip.read_bytes())
            body, mapping = audio_feedback.make_payload([f"A={clip}"], "Compare honestly.", 100)
        self.assertNotIn(b"private-filename", body)
        self.assertNotIn(directory.encode(), body)
        self.assertEqual(mapping[0]["local_path"], str(clip.resolve()))
        parts = json.loads(body)["contents"][0]["parts"]
        self.assertIn("Clip A", parts[1]["text"])
        self.assertEqual(parts[2]["inlineData"]["mimeType"], "audio/flac")
        cleaned = base64.b64decode(parts[2]["inlineData"]["data"])
        self.assertTrue(cleaned.startswith(b"fLaC"))
        self.assertNotIn(b"PRIVATE-REJECTED-SONG", cleaned)
        self.assertNotIn(b"PRIVATE-ARTIST", cleaned)
        self.assertNotIn(b"private-filename", cleaned)
        decoded = subprocess.run([
            "ffmpeg", "-v", "error", "-i", "pipe:0", "-f", "s16le", "pipe:1",
        ], input=cleaned, capture_output=True, timeout=10, check=True)
        self.assertEqual(decoded.stdout, samples)

    def test_duplicate_labels_fail_before_network(self):
        with tempfile.TemporaryDirectory() as directory:
            clip = Path(directory) / "a.wav"
            self.tagged_wav(clip)
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                audio_feedback.make_payload([f"A={clip}", f"A={clip}"], "Compare.", 100)

    def test_missing_credentials_are_actionable_without_network(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(Path, "is_file", return_value=False):
            with self.assertRaisesRegex(ValueError, "No Gemini credential"):
                audio_feedback.load_api_key()

    def test_environment_credential_takes_precedence(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": " fixture-key ", "GOOGLE_API_KEY": "other"}):
            self.assertEqual(audio_feedback.load_api_key(), "fixture-key")

    def test_http_failure_does_not_echo_key_or_server_body(self):
        error = urllib.error.HTTPError("https://example.invalid", 403, "fixture-key", {}, io.BytesIO(b"fixture-key"))
        with patch.object(audio_feedback.urllib.request, "urlopen", side_effect=error) as urlopen:
            with self.assertRaises(RuntimeError) as caught:
                audio_feedback.request_json("/models", "fixture-key")
        self.assertIn("403", str(caught.exception))
        self.assertNotIn("fixture-key", str(caught.exception))
        request = urlopen.call_args.args[0]
        self.assertNotIn("fixture-key", request.full_url)
        self.assertEqual(request.get_header("X-goog-api-key"), "fixture-key")

    def test_protocol_read_errors_are_sanitized_and_never_retried(self):
        for error in (
            http.client.IncompleteRead(b"fixture-key-private-response", 200),
            http.client.BadStatusLine("fixture-key-private-response"),
        ):
            response = MagicMock()
            response.__enter__.return_value = response
            response.read.side_effect = error
            with self.subTest(error=type(error).__name__), patch.object(
                audio_feedback.urllib.request, "urlopen", return_value=response,
            ) as urlopen:
                with self.assertRaises(RuntimeError) as caught:
                    audio_feedback.request_json("/models/test:generateContent", "fixture-key", b"{}")
            self.assertIn("outcome unknown", str(caught.exception))
            self.assertNotIn("fixture-key", str(caught.exception))
            self.assertNotIn("private-response", str(caught.exception))
            urlopen.assert_called_once()

    def test_incomplete_response_saves_unknown_billing_outcome(self):
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.side_effect = http.client.IncompleteRead(b"fixture-key-private-response", 200)
        stderr = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            clip = Path(directory) / "a.wav"
            self.tagged_wav(clip)
            out = Path(directory) / "results"
            with patch.object(audio_feedback, "load_api_key", return_value="fixture-key"), patch.object(
                audio_feedback.urllib.request, "urlopen", return_value=response,
            ) as urlopen, redirect_stderr(stderr):
                exit_code = audio_feedback.main([
                    "assess", "--model", "test-model", "--clip", f"A={clip}",
                    "--prompt", "Compare.", "--output-dir", str(out),
                ])
            usage = json.loads((out / "usage.json").read_text())
            saved_files = "\n".join(p.read_text() for p in out.iterdir())
        self.assertEqual(exit_code, 1)
        self.assertEqual(usage["request_outcome"], "unknown")
        self.assertEqual(usage["billing_outcome"], "unknown")
        self.assertIsNone(usage["usage"])
        self.assertFalse(usage["retry_sent"])
        self.assertNotIn("fixture-key", stderr.getvalue() + saved_files)
        self.assertNotIn("private-response", stderr.getvalue() + saved_files)
        urlopen.assert_called_once()

    def test_response_parser_excludes_thoughts_and_reports_truncation(self):
        text, reason = audio_feedback.response_text({"candidates": [{
            "content": {"parts": [{"text": "hidden", "thought": True}, {"text": "audible evidence"}]},
            "finishReason": "MAX_TOKENS",
        }]})
        self.assertEqual(text, "audible evidence")
        self.assertEqual(reason, "MAX_TOKENS")

    def test_blocked_and_empty_results_are_failures(self):
        for response in ({"promptFeedback": {"blockReason": "SAFETY"}}, {"candidates": [{"finishReason": "STOP"}]}):
            with self.subTest(response=response), self.assertRaises(RuntimeError):
                audio_feedback.response_text(response)


if __name__ == "__main__":
    unittest.main()
