#!/usr/bin/env python3
"""Study a bounded public YouTube passage through Gemini; no media download."""

import argparse
import http.client
import json
import math
import os
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request


def youtube_url(value):
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme != "https" or parsed.username or parsed.password or parsed.port:
        raise ValueError("Use an HTTPS public YouTube watch URL")
    if parsed.hostname == "youtu.be":
        video_id = parsed.path.removeprefix("/")
    elif parsed.hostname in {"youtube.com", "www.youtube.com"} and parsed.path == "/watch":
        ids = urllib.parse.parse_qs(parsed.query).get("v", [])
        video_id = ids[0] if len(ids) == 1 else ""
    else:
        raise ValueError("Use a youtube.com/watch or youtu.be URL")
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
        raise ValueError("Invalid YouTube video ID")
    return "https://www.youtube.com/watch?v=" + video_id


def api_key():
    for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        if os.environ.get(name, "").strip():
            return os.environ[name].strip()
    path = Path.home() / ".claude/.env"
    if path.is_file():
        for line in path.read_text().splitlines():
            key, _, value = line.strip().removeprefix("export ").partition("=")
            if key.strip() in {"GEMINI_API_KEY", "GOOGLE_API_KEY"} and value.strip():
                return value.strip().strip("\"'")
    raise ValueError("Set GEMINI_API_KEY or GOOGLE_API_KEY")


def payload(url, start, end, fps, prompt):
    if not all(math.isfinite(x) for x in (start, end, fps)):
        raise ValueError("Time and frame rate must be finite")
    if not 0 <= start < end or end - start > 900 or not 0 < fps <= 5:
        raise ValueError("Choose an interval of at most 900 seconds and 0 < fps <= 5")
    if not prompt.strip():
        raise ValueError("Prompt is empty")
    return {
        "contents": [{"role": "user", "parts": [
            {"fileData": {"fileUri": youtube_url(url), "mimeType": "video/*"},
             "videoMetadata": {"startOffset": f"{start:g}s", "endOffset": f"{end:g}s", "fps": fps}},
            {"text": prompt},
        ]}],
        "generationConfig": {"maxOutputTokens": 6000},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", required=True)
    parser.add_argument("--start", type=float, required=True)
    parser.add_argument("--end", type=float, required=True)
    parser.add_argument("--fps", type=float, default=1)
    parser.add_argument("--model", required=True)
    parser.add_argument("--prompt-file", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        if not re.fullmatch(r"gemini-[a-zA-Z0-9.-]+", args.model):
            raise ValueError("Invalid Gemini model name")
        body = payload(args.url, args.start, args.end, args.fps, args.prompt_file.read_text())
        key = api_key()
        args.output_dir.mkdir(parents=True, exist_ok=False)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    out = args.output_dir
    (out / "request.json").write_text(json.dumps({"model": args.model, **body}, indent=2))
    request = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{args.model}:generateContent",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.load(response)
        (out / "response.json").write_text(json.dumps(result, indent=2))
        candidates = result.get("candidates", [])
        candidate = candidates[0] if candidates else {}
        answer = "\n".join(p["text"] for p in candidate.get("content", {}).get("parts", [])
                           if "text" in p and not p.get("thought"))
        (out / "usage.json").write_text(json.dumps(result.get("usageMetadata", {}), indent=2))
        if not answer or candidate.get("finishReason") != "STOP":
            raise RuntimeError("No complete analysis returned; inspect response.json. No retry sent")
        (out / "analysis.md").write_text(answer + "\n")
        print(out / "analysis.md")
        print(json.dumps(result.get("usageMetadata", {})))
    except (urllib.error.URLError, http.client.HTTPException, OSError, ValueError, RuntimeError) as error:
        message = (str(error) if isinstance(error, RuntimeError) else
                   "Video analysis request or response failed; billing outcome unknown. No retry sent")
        (out / "failure.json").write_text(json.dumps({"error": message, "billing": "unknown"}))
        raise SystemExit(message) from None


if __name__ == "__main__":
    main()
