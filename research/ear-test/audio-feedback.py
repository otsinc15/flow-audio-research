#!/usr/bin/env python3
"""Assess local audio through Gemini generateContent; send inline bytes, never filenames.

python3 audio-feedback.py models
python3 audio-feedback.py assess --model gemini-3.8-flash --clip A=/path/a.wav \
    --clip B=/path/b.wav --prompt-file /path/prompt.txt --output-dir /path/results

Only explicitly supplied clips and prompt are transmitted. Audio is locally
re-encoded as FLAC with metadata removed (requires ffmpeg). Results and the local
source mapping stay in the requested output directory. No Files API is used.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import http.client
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://generativelanguage.googleapis.com/v1beta"
MAX_REQUEST_BYTES = 20_000_000
MAX_AUDIO_BYTES = MAX_REQUEST_BYTES * 3 // 4
MIME_TYPES = {
    ".wav": "audio/wav", ".mp3": "audio/mp3", ".aiff": "audio/aiff",
    ".aif": "audio/aiff", ".aac": "audio/aac", ".ogg": "audio/ogg",
    ".flac": "audio/flac",
}


def load_api_key() -> str:
    for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if value := os.environ.get(name, "").strip():
            return value
    dotenv = Path.home() / ".claude" / ".env"
    if dotenv.is_file():
        for line in dotenv.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[7:].strip()
            name, _, value = line.partition("=")
            value = value.strip().strip("'\"")
            if name.strip() in ("GEMINI_API_KEY", "GOOGLE_API_KEY") and value:
                return value
    raise ValueError("No Gemini credential found in environment or ~/.claude/.env")


def request_json(endpoint: str, key: str, body: bytes | None = None) -> dict:
    request = urllib.request.Request(
        API + endpoint, data=body,
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        # Server errors can echo request data; expose only the status code.
        raise RuntimeError(f"Gemini request failed (HTTP {error.code}); no retry sent") from None
    except (urllib.error.URLError, http.client.HTTPException, OSError):
        raise RuntimeError("Gemini connection or response read failed; outcome unknown, no retry sent") from None
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise RuntimeError("Gemini returned invalid JSON; outcome unknown, no retry sent") from None
    if not isinstance(result, dict):
        raise RuntimeError("Gemini returned an unexpected JSON structure")
    return result


def clean_audio(path: Path) -> bytes:
    with tempfile.TemporaryDirectory(prefix="audio-feedback-") as directory:
        output = Path(directory) / "clip.flac"
        try:
            result = subprocess.run([
                "ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
                "-i", str(path), "-map", "0:a:0", "-vn", "-sn", "-dn",
                "-map_metadata", "-1", "-map_metadata:s:a", "-1", "-map_chapters", "-1",
                "-c:a", "flac", "-fflags", "+bitexact", "-flags:a", "+bitexact",
                "-metadata", "encoder=", "-fs", str(MAX_AUDIO_BYTES + 1), str(output),
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60, check=False)
        except FileNotFoundError:
            raise RuntimeError("ffmpeg is required to remove embedded audio metadata") from None
        except subprocess.TimeoutExpired:
            raise RuntimeError("Local audio cleanup timed out; no audio sent") from None
        if result.returncode != 0:
            raise RuntimeError("ffmpeg could not decode and clean the audio; no audio sent")
        if output.stat().st_size >= MAX_AUDIO_BYTES:
            raise ValueError("Cleaned audio exceeds the inline request limit; trim the clip first")
        return output.read_bytes()


def list_models(key: str) -> list[dict]:
    models = []
    token = None
    while True:
        query = {"pageSize": 1000}
        if token:
            query["pageToken"] = token
        result = request_json("/models?" + urllib.parse.urlencode(query), key)
        models.extend(result.get("models", []))
        token = result.get("nextPageToken")
        if not token:
            return models


def make_payload(clips: list[str], prompt: str, max_output_tokens: int) -> tuple[bytes, list[dict]]:
    if not prompt.strip():
        raise ValueError("The assessment prompt must not be empty")
    parts = [{"text": prompt}]
    mapping = []
    seen = set()
    total_audio_bytes = 0
    for spec in clips:
        label, separator, filename = spec.partition("=")
        if not separator or not re.fullmatch(r"[A-Z]", label):
            raise ValueError("Each --clip must be a single anonymous letter and path: A=/path/audio.wav")
        if label in seen:
            raise ValueError(f"Duplicate clip label: {label}")
        seen.add(label)
        path = Path(filename).expanduser().resolve()
        if path.suffix.lower() not in MIME_TYPES:
            raise ValueError(f"Unsupported audio extension for clip {label}; convert to WAV or FLAC")
        data = clean_audio(path)
        mime = "audio/flac"
        total_audio_bytes += len(data)
        if total_audio_bytes * 4 / 3 > MAX_REQUEST_BYTES:
            raise ValueError("Audio exceeds the 20 MB inline request limit; trim or compress first")
        parts.extend([
            {"text": f"Clip {label}. Timestamps restart at 00:00 for this clip."},
            {"inlineData": {"mimeType": mime, "data": base64.b64encode(data).decode("ascii")}},
        ])
        mapping.append({
            "label": label, "local_path": str(path), "mime_type": mime,
            "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
        })
    body = json.dumps({
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"maxOutputTokens": max_output_tokens, "responseModalities": ["TEXT"]},
    }).encode("utf-8")
    if len(body) > MAX_REQUEST_BYTES:
        raise ValueError("Combined prompt and audio exceed the 20 MB inline request limit")
    return body, mapping


def response_text(result: dict) -> tuple[str, str]:
    candidates = result.get("candidates", [])
    if not isinstance(candidates, list) or not candidates or not isinstance(candidates[0], dict):
        raise RuntimeError("Gemini returned no candidate; inspect response.json for block details")
    candidate = candidates[0]
    parts = candidate.get("content", {}).get("parts", [])
    text = "\n".join(
        part["text"] for part in parts
        if isinstance(part, dict) and isinstance(part.get("text"), str) and not part.get("thought")
    ).strip()
    if not text:
        raise RuntimeError("Gemini returned no assessment text; inspect response.json")
    return text, candidate.get("finishReason", "UNKNOWN")


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("models", help="List models supporting generateContent; no audio sent")
    assess = commands.add_parser("assess", help="Send explicitly supplied local audio for text assessment")
    assess.add_argument("--model", required=True, help="Exact model identifier; use models to discover availability")
    assess.add_argument("--clip", action="append", required=True, metavar="A=PATH")
    prompts = assess.add_mutually_exclusive_group(required=True)
    prompts.add_argument("--prompt")
    prompts.add_argument("--prompt-file", type=Path)
    assess.add_argument("--output-dir", type=Path, required=True, help="New directory for raw result, text, usage and local mapping")
    assess.add_argument("--max-output-tokens", type=int, default=4096)
    args = parser.parse_args(argv)
    try:
        if args.command == "models":
            for model in list_models(load_api_key()):
                if "generateContent" in model.get("supportedGenerationMethods", []):
                    print(model["name"])
            return 0
        model = args.model.removeprefix("models/")
        if not re.fullmatch(r"[a-zA-Z0-9._-]+", model):
            raise ValueError("Invalid model identifier")
        if not 1 <= args.max_output_tokens <= 16384:
            raise ValueError("--max-output-tokens must be between 1 and 16384")
        prompt = args.prompt if args.prompt is not None else args.prompt_file.expanduser().read_text(encoding="utf-8")
        body, mapping = make_payload(args.clip, prompt, args.max_output_tokens)
        key = load_api_key()
        out = args.output_dir.expanduser().resolve()
        out.mkdir(parents=True, exist_ok=False)
        write_json(out / "request-metadata.json", {
            "model_requested": model, "prompt": prompt, "clips": mapping,
            "max_output_tokens": args.max_output_tokens, "request_bytes": len(body),
            "transport": "inlineData; metadata removed by local FLAC re-encoding; local paths and hashes not sent",
        })
        started = time.monotonic()
        try:
            result = request_json(f"/models/{model}:generateContent", key, body)
        except RuntimeError as error:
            write_json(out / "usage.json", {
                "model_requested": model, "model_returned": None,
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "request_outcome": "unknown", "billing_outcome": "unknown",
                "usage": None, "retry_sent": False, "error": str(error),
            })
            raise
        write_json(out / "response.json", result)
        write_json(out / "usage.json", {
            "model_requested": model, "model_returned": result.get("modelVersion"),
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "request_outcome": "response_received", "retry_sent": False,
            "usage": result.get("usageMetadata"),
        })
        text, finish = response_text(result)
        (out / "assessment.txt").write_text(text + "\n", encoding="utf-8")
        print(text)
        print(f"\nResults: {out}\nFinish reason: {finish}", file=sys.stderr)
        return 0 if finish == "STOP" else 2
    except (ValueError, RuntimeError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
