#!/usr/bin/env python3
"""Render harness for Google Lyria RealTime (Gemini API, `lyria-realtime-exp`).

Opens a WebSocket music session via the official `google-genai` SDK, steers it
with weighted text prompts and a generation config, records the raw PCM chunks
and writes a WAV file.

Docs (read 2026-09-02):
  https://ai.google.dev/gemini-api/docs/realtime-music-generation
  https://ai.google.dev/gemini-api/docs/models/lyria-realtime-exp

Documented output format: raw 16-bit PCM, 48 kHz, 2 channels (stereo).
The actual rate is re-confirmed at runtime from each chunk's `mime_type`
(e.g. `audio/L16;codec=pcm;rate=48000`) and that value is what lands in the
WAV header.

Nothing here uploads or references audio: Lyria RealTime is text-prompt only.
"""

from __future__ import annotations

import argparse
import asyncio
import contextlib
import dataclasses
import json
import os
import re
import sys
import time
import wave
from pathlib import Path
from typing import Any

try:
    from google import genai
    from google.genai import types
except ImportError:  # pragma: no cover - surfaced to the operator immediately
    print(
        "google-genai is not installed. See lyria/README.md:\n"
        "  python3.13 -m venv ~/.venvs/lyria && ~/.venvs/lyria/bin/pip install google-genai",
        file=sys.stderr,
    )
    raise

MODEL = "models/lyria-realtime-exp"
DEFAULT_API_VERSION = "v1alpha"
# The docs' Python sample currently pins v1beta; the SDK builds the websocket
# URI as .../ws/google.ai.generativelanguage.{api_version}.GenerativeService.BidiGenerateMusic
# so the version is load-bearing. We try the requested one, then this.
FALLBACK_API_VERSION = "v1beta"

# Documented fallbacks; the wire `mime_type` wins when it is parseable.
DOC_SAMPLE_RATE = 48000
CHANNELS = 2
SAMPLE_WIDTH = 2  # 16-bit

STALL_TIMEOUT_S = 30.0  # no chunk for this long -> treat as a dropped stream
MAX_RECONNECTS = 3

RANGES = {
    "bpm": (60, 200),
    "density": (0.0, 1.0),
    "brightness": (0.0, 1.0),
    "guidance": (0.0, 6.0),
    "temperature": (0.0, 3.0),
    "top_k": (1, 1000),
    "seed": (0, 2147483647),
}

# Fields that force a hard context reset when changed mid-stream (per docs).
RESET_FIELDS = ("bpm", "scale")


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


# --------------------------------------------------------------------------
# API key
# --------------------------------------------------------------------------


def load_api_key() -> tuple[str | None, str]:
    """Return (key, source). Never log or print the key itself."""
    for var in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        val = os.environ.get(var)
        if val:
            return val.strip(), f"env:{var}"

    dotenv = Path.home() / ".claude" / ".env"
    if dotenv.is_file():
        for line in dotenv.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export ") :].strip()
            key, _, val = line.partition("=")
            if key.strip() in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
                val = val.strip().strip("'\"")
                if val:
                    return val, f"{dotenv}:{key.strip()}"
    return None, "not found"


# --------------------------------------------------------------------------
# Parsing / validation
# --------------------------------------------------------------------------


def parse_prompts(spec: Any) -> list[types.WeightedPrompt]:
    """Accept "text:weight,text:weight" or a list of {text, weight} dicts."""
    if isinstance(spec, list):
        out = []
        for item in spec:
            if isinstance(item, dict):
                text = str(item["text"]).strip()
                weight = float(item.get("weight", 1.0))
            else:
                text, weight = _split_prompt(str(item))
            out.append(_weighted(text, weight))
        if not out:
            raise ValueError("prompts list is empty")
        return out

    parts = [p.strip() for p in str(spec).split(",")]
    out = []
    for part in parts:
        if not part:
            continue
        text, weight = _split_prompt(part)
        out.append(_weighted(text, weight))
    if not out:
        raise ValueError("no prompts parsed from --prompts")
    return out


def _split_prompt(part: str) -> tuple[str, float]:
    text, sep, weight_s = part.rpartition(":")
    if not sep:
        return part.strip(), 1.0
    try:
        return text.strip(), float(weight_s.strip())
    except ValueError:
        # A colon that was part of the prompt text, not a weight.
        return part.strip(), 1.0


def _weighted(text: str, weight: float) -> types.WeightedPrompt:
    if not text:
        raise ValueError("empty prompt text")
    if weight == 0:
        # Docs: "The weight can take any value except 0."
        raise ValueError(f"prompt weight must not be 0 (prompt: {text!r})")
    return types.WeightedPrompt(text=text, weight=weight)


def _scale_aliases() -> dict[str, types.Scale]:
    aliases: dict[str, types.Scale] = {}
    for member in types.Scale:
        aliases[member.name] = member
        if "_MAJOR_" in member.name and member.name.endswith("_MINOR"):
            major, _, rest = member.name.partition("_MAJOR_")
            minor = rest[: -len("_MINOR")]
            aliases.setdefault(f"{major}_MAJOR", member)
            aliases.setdefault(f"{minor}_MINOR", member)
    for word in ("AUTO", "NONE", "UNSPECIFIED", "DEFAULT"):
        aliases[word] = types.Scale.SCALE_UNSPECIFIED
    return aliases


SCALE_ALIASES = _scale_aliases()


def parse_scale(spec: Any) -> types.Scale:
    if spec is None or (isinstance(spec, str) and not spec.strip()):
        return types.Scale.SCALE_UNSPECIFIED
    if isinstance(spec, types.Scale):
        return spec
    key = re.sub(r"[^A-Z0-9]+", "_", str(spec).upper()).strip("_")
    if key in SCALE_ALIASES:
        return SCALE_ALIASES[key]
    raise ValueError(
        f"unknown scale {spec!r}. Valid: "
        + ", ".join(sorted({m.name for m in types.Scale}))
        + " (aliases such as A_MINOR, C_MAJOR, B_FLAT_MINOR also work)"
    )


def check_range(name: str, value: Any) -> Any:
    if value is None or name not in RANGES:
        return value
    lo, hi = RANGES[name]
    if not (lo <= value <= hi):
        raise ValueError(f"{name}={value} out of documented range [{lo}, {hi}]")
    return value


# --------------------------------------------------------------------------
# Clip spec
# --------------------------------------------------------------------------


@dataclasses.dataclass
class ClipSpec:
    name: str
    seconds: float
    out: Path
    prompts: list[types.WeightedPrompt]
    bpm: int | None = None
    scale: types.Scale = types.Scale.SCALE_UNSPECIFIED
    density: float | None = None
    brightness: float | None = None
    guidance: float | None = None
    temperature: float | None = None
    seed: int | None = None
    steer: list[dict[str, Any]] = dataclasses.field(default_factory=list)

    def config_fields(self) -> dict[str, Any]:
        """The full config dict. Docs: you must always resend the WHOLE config,
        or unset fields fall back to their defaults."""
        fields = {
            "bpm": self.bpm,
            "scale": self.scale,
            "density": self.density,
            "brightness": self.brightness,
            "guidance": self.guidance,
            "temperature": self.temperature,
            "seed": self.seed,
        }
        return {k: v for k, v in fields.items() if v is not None}

    def describe(self) -> dict[str, Any]:
        cfg = self.config_fields()
        return {
            "name": self.name,
            "model": MODEL,
            "seconds": self.seconds,
            "out": str(self.out),
            "prompts": [{"text": p.text, "weight": p.weight} for p in self.prompts],
            "music_generation_config": {
                k: (v.name if isinstance(v, types.Scale) else v) for k, v in cfg.items()
            },
            "steer": [_describe_step(s) for s in self.steer],
        }


def _describe_step(step: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {"at_seconds": step["at_seconds"]}
    if "prompts" in step:
        out["prompts"] = [
            {"text": p.text, "weight": p.weight} for p in step["prompts"]
        ]
    for key in ("bpm", "density", "brightness", "guidance", "scale"):
        if key in step:
            val = step[key]
            out[key] = val.name if isinstance(val, types.Scale) else val
    if any(k in step for k in RESET_FIELDS):
        out["_resets_context"] = True
    return out


def load_steer(source: Any) -> list[dict[str, Any]]:
    """Validate a steer script: a JSON list of
    {at_seconds, prompts?, bpm?, density?, brightness?, guidance?, scale?}."""
    if source is None:
        return []
    if isinstance(source, (str, Path)) and not isinstance(source, list):
        raw = json.loads(Path(source).read_text(encoding="utf-8"))
    else:
        raw = source
    if not isinstance(raw, list):
        raise ValueError("steer script must be a JSON list of steps")

    steps: list[dict[str, Any]] = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"steer step {i} is not an object")
        if "at_seconds" not in item:
            raise ValueError(f"steer step {i} is missing at_seconds")
        step: dict[str, Any] = {"at_seconds": float(item["at_seconds"])}
        if step["at_seconds"] < 0:
            raise ValueError(f"steer step {i}: at_seconds must be >= 0")
        if "prompts" in item:
            step["prompts"] = parse_prompts(item["prompts"])
        if "scale" in item:
            step["scale"] = parse_scale(item["scale"])
        for key in ("bpm", "density", "brightness", "guidance"):
            if key in item:
                val = int(item[key]) if key == "bpm" else float(item[key])
                step[key] = check_range(key, val)
        if len(step) == 1:
            raise ValueError(f"steer step {i} changes nothing")
        steps.append(step)
    steps.sort(key=lambda s: s["at_seconds"])
    return steps


def spec_from_args(args: argparse.Namespace) -> ClipSpec:
    return ClipSpec(
        name=Path(args.out).stem,
        seconds=args.seconds if args.seconds is not None else 90.0,
        out=Path(args.out),
        prompts=parse_prompts(args.prompts),
        bpm=check_range("bpm", args.bpm),
        scale=parse_scale(args.scale),
        density=check_range("density", args.density),
        brightness=check_range("brightness", args.brightness),
        guidance=check_range("guidance", args.guidance),
        temperature=check_range("temperature", args.temperature),
        seed=check_range("seed", args.seed),
        steer=load_steer(args.steer_script),
    )


def specs_from_batch(path: Path, out_dir: Path, seconds_override: float | None) -> list[ClipSpec]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    defaults = doc.get("defaults", {})
    specs = []
    for i, clip in enumerate(doc.get("clips", [])):
        merged = {**defaults, **clip}
        name = merged.get("name") or f"clip{i + 1:02d}"
        seconds = float(seconds_override or merged.get("seconds", 90))
        specs.append(
            ClipSpec(
                name=name,
                seconds=seconds,
                out=out_dir / f"{name}.wav",
                prompts=parse_prompts(merged["prompts"]),
                bpm=check_range("bpm", merged.get("bpm")),
                scale=parse_scale(merged.get("scale")),
                density=check_range("density", merged.get("density")),
                brightness=check_range("brightness", merged.get("brightness")),
                guidance=check_range("guidance", merged.get("guidance")),
                temperature=check_range("temperature", merged.get("temperature")),
                seed=check_range("seed", merged.get("seed")),
                steer=load_steer(merged.get("steer")),
            )
        )
    if not specs:
        raise ValueError(f"{path} contains no clips")
    return specs


# --------------------------------------------------------------------------
# Recording
# --------------------------------------------------------------------------


def rate_from_mime(mime_type: str | None) -> int | None:
    if not mime_type:
        return None
    m = re.search(r"rate=(\d+)", mime_type)
    return int(m.group(1)) if m else None


class Recorder:
    """Streams raw PCM to a .part file so a crashed run is still salvageable."""

    def __init__(self, out: Path):
        self.out = out
        self.part = out.with_suffix(out.suffix + ".part")
        self.out.parent.mkdir(parents=True, exist_ok=True)
        self.fh = self.part.open("wb")
        self.bytes_written = 0
        self.chunks = 0
        self.rate: int | None = None
        self.mime_types: set[str] = set()

    @property
    def frames(self) -> int:
        return self.bytes_written // (CHANNELS * SAMPLE_WIDTH)

    @property
    def audio_seconds(self) -> float:
        return self.frames / float(self.rate or DOC_SAMPLE_RATE)

    def add(self, chunk: types.AudioChunk) -> None:
        data = chunk.data or b""
        if not data:
            return
        if chunk.mime_type:
            self.mime_types.add(chunk.mime_type)
            observed = rate_from_mime(chunk.mime_type)
            if observed and observed != self.rate:
                if self.rate is not None:
                    log(f"WARNING sample rate changed mid-stream {self.rate} -> {observed}")
                self.rate = observed
        self.fh.write(data)
        self.bytes_written += len(data)
        self.chunks += 1

    def finish(self) -> int:
        self.fh.close()
        rate = self.rate or DOC_SAMPLE_RATE
        if self.rate is None:
            log(f"no rate in mime_type; falling back to documented {DOC_SAMPLE_RATE} Hz")
        with wave.open(str(self.out), "wb") as w:
            w.setnchannels(CHANNELS)
            w.setsampwidth(SAMPLE_WIDTH)
            w.setframerate(rate)
            with self.part.open("rb") as src:
                while block := src.read(1 << 20):
                    w.writeframes(block)
        self.part.unlink(missing_ok=True)
        return rate

    def abort(self) -> None:
        with contextlib.suppress(Exception):
            self.fh.close()
        if self.bytes_written == 0:
            self.part.unlink(missing_ok=True)


async def _apply_step(session, step: dict[str, Any], config: dict[str, Any], rec: Recorder) -> None:
    changed = []
    if "prompts" in step:
        await session.set_weighted_prompts(prompts=step["prompts"])
        changed.append("prompts")

    patch = {k: v for k, v in step.items() if k not in ("at_seconds", "prompts")}
    if patch:
        config.update(patch)
        # Docs: resend the WHOLE config or the other fields reset to defaults.
        await session.set_music_generation_config(
            config=types.LiveMusicGenerationConfig(**config)
        )
        changed.extend(patch)
        if any(k in patch for k in RESET_FIELDS):
            await session.reset_context()
            changed.append("reset_context")
    log(f"  steer @{rec.audio_seconds:6.1f}s (t={step['at_seconds']}s): {', '.join(changed)}")


async def render_clip(spec: ClipSpec, client_factory, verbose: bool) -> dict[str, Any]:
    rec = Recorder(spec.out)
    config = dict(spec.config_fields())
    pending = list(spec.steer)
    target_bytes_at = lambda rate: int(spec.seconds * rate) * CHANNELS * SAMPLE_WIDTH

    reconnects = 0
    max_gap = 0.0
    first_chunk_latency: float | None = None
    filtered: list[str] = []
    started = time.monotonic()
    api_version_used: str | None = None

    while True:
        client, api_version_used = client_factory(
            advance=reconnects > 0 and rec.bytes_written == 0
        )
        connect_at = time.monotonic()
        try:
            async with client.aio.live.music.connect(model=MODEL) as session:
                await session.set_weighted_prompts(prompts=spec.prompts)
                if config:
                    await session.set_music_generation_config(
                        config=types.LiveMusicGenerationConfig(**config)
                    )
                await session.play()
                if reconnects:
                    log(f"  reconnected (#{reconnects}) at {rec.audio_seconds:.1f}s of audio")

                last_chunk_at = time.monotonic()
                stream = session.receive().__aiter__()
                while True:
                    try:
                        # A silent stall would otherwise hang the batch forever;
                        # a timeout falls through to the reconnect handler below.
                        message = await asyncio.wait_for(
                            stream.__anext__(), timeout=STALL_TIMEOUT_S
                        )
                    except StopAsyncIteration:
                        break
                    if message.filtered_prompt is not None:
                        fp = message.filtered_prompt
                        note = f"{fp.text!r}: {fp.filtered_reason}"
                        filtered.append(note)
                        log(f"  SAFETY FILTER dropped prompt {note}")
                        continue

                    content = message.server_content
                    if content is None or not content.audio_chunks:
                        continue

                    now = time.monotonic()
                    if first_chunk_latency is None:
                        first_chunk_latency = now - connect_at
                        client_factory.lock()
                        log(f"  first audio chunk after {first_chunk_latency:.2f}s")
                    else:
                        max_gap = max(max_gap, now - last_chunk_at)
                    last_chunk_at = now

                    for chunk in content.audio_chunks:
                        rec.add(chunk)
                    if verbose:
                        log(
                            f"  chunk {rec.chunks:4d} audio={rec.audio_seconds:6.2f}s "
                            f"wall={now - started:6.2f}s bytes={rec.bytes_written}"
                        )

                    while pending and rec.audio_seconds >= pending[0]["at_seconds"]:
                        await _apply_step(session, pending.pop(0), config, rec)

                    if rec.bytes_written >= target_bytes_at(rec.rate or DOC_SAMPLE_RATE):
                        await session.stop()
                        break
            break
        except asyncio.CancelledError:
            rec.abort()
            raise
        except Exception as exc:  # noqa: BLE001 - reconnect on any stream failure
            done = rec.bytes_written >= target_bytes_at(rec.rate or DOC_SAMPLE_RATE)
            if done:
                break
            reconnects += 1
            if reconnects > MAX_RECONNECTS:
                rec.abort()
                raise RuntimeError(
                    f"stream failed after {MAX_RECONNECTS} reconnects "
                    f"({rec.audio_seconds:.1f}s recorded): {type(exc).__name__}: {exc}"
                ) from exc
            log(
                f"  stream dropped at {rec.audio_seconds:.1f}s "
                f"({type(exc).__name__}: {exc}); reconnecting {reconnects}/{MAX_RECONNECTS}"
            )
            await asyncio.sleep(1.0)

    rate = rec.finish()
    wall = time.monotonic() - started
    stats = {
        "name": spec.name,
        "out": str(spec.out),
        "api_version": api_version_used,
        "sample_rate": rate,
        "channels": CHANNELS,
        "bit_depth": SAMPLE_WIDTH * 8,
        "mime_types": sorted(rec.mime_types),
        "audio_seconds": round(rec.audio_seconds, 2),
        "wall_seconds": round(wall, 2),
        "chunks": rec.chunks,
        "bytes": rec.bytes_written,
        "first_chunk_latency_s": round(first_chunk_latency, 2) if first_chunk_latency else None,
        "max_chunk_gap_s": round(max_gap, 2),
        "reconnects": reconnects,
        "filtered_prompts": filtered,
        "steer_steps_unapplied": len(pending),
    }
    log(
        f"  wrote {spec.out} — {stats['audio_seconds']}s @ {rate} Hz stereo, "
        f"{rec.chunks} chunks, max gap {max_gap:.2f}s, {reconnects} reconnect(s)"
    )
    if pending:
        log(f"  WARNING {len(pending)} steer step(s) never fired (past clip length)")
    return stats


# --------------------------------------------------------------------------
# Client
# --------------------------------------------------------------------------


def make_client_factory(api_key: str, api_version: str):
    """Returns a callable producing (client, api_version).

    Tries the requested API version, and falls back to the one the current docs
    use ONLY while no version has ever produced audio. Once one works it is
    latched for the rest of the run -- otherwise a mid-stream drop on a working
    version would push every later connection onto a version that 404s.
    """
    versions = [api_version]
    if api_version != FALLBACK_API_VERSION:
        versions.append(FALLBACK_API_VERSION)
    state = {"idx": 0, "locked": False}

    def factory(advance: bool = False):
        if advance and not state["locked"] and state["idx"] + 1 < len(versions):
            state["idx"] += 1
            log(f"  trying api_version={versions[state['idx']]}")
        version = versions[state["idx"]]
        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(api_version=version),
        )
        return client, version

    def lock() -> None:
        state["locked"] = True

    factory.lock = lock  # type: ignore[attr-defined]
    return factory


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="render.py",
        description="Record text-steered instrumental music from Lyria RealTime to WAV.",
    )
    p.add_argument("--seconds", type=float, default=None,
               help="clip length in seconds (default 90; with --batch, overrides every clip)")
    p.add_argument("--bpm", type=int, help=f"beats per minute {RANGES['bpm']}")
    p.add_argument("--scale", default=None, help="e.g. A_MINOR / C_MAJOR_A_MINOR (default: model decides)")
    p.add_argument("--density", type=float, help="0.0 sparse .. 1.0 busy")
    p.add_argument("--brightness", type=float, help="0.0 dark .. 1.0 bright")
    p.add_argument("--guidance", type=float, help="0.0 .. 6.0, default 4.0 server-side")
    p.add_argument("--temperature", type=float, help="0.0 .. 3.0, default 1.1 server-side")
    p.add_argument("--seed", type=int, help="0 .. 2147483647 (random by default)")
    p.add_argument("--prompts", help='"text:weight,text:weight" (weight may not be 0)')
    p.add_argument("--out", help="output WAV path")
    p.add_argument("--steer-script", help="JSON list of {at_seconds, prompts|bpm|density|brightness}")
    p.add_argument("--batch", help="batch JSON (e.g. lyria/batch.json) — renders every clip")
    p.add_argument("--out-dir", default="out", help="output dir for --batch (default: out/)")
    p.add_argument("--api-version", default=DEFAULT_API_VERSION,
                   help=f"websocket API version (default {DEFAULT_API_VERSION}, falls back to {FALLBACK_API_VERSION})")
    p.add_argument("--dry-run", action="store_true", help="validate + print config, never connect")
    p.add_argument("--verbose", action="store_true", help="log every audio chunk")
    return p


async def run(specs: list[ClipSpec], api_key: str, api_version: str, verbose: bool) -> int:
    factory = make_client_factory(api_key, api_version)
    results = []
    failures = 0
    for i, spec in enumerate(specs, 1):
        log(f"[{i}/{len(specs)}] {spec.name}: {spec.seconds:.0f}s -> {spec.out}")
        try:
            results.append(await render_clip(spec, factory, verbose))
        except Exception as exc:  # noqa: BLE001
            failures += 1
            log(f"  FAILED {spec.name}: {type(exc).__name__}: {exc}")
    print(json.dumps(results, indent=2))
    return 1 if failures else 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return _main(args, argv)
    except (ValueError, KeyError, json.JSONDecodeError, FileNotFoundError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


def _main(args: argparse.Namespace, argv: list[str] | None) -> int:
    if args.batch:
        specs = specs_from_batch(Path(args.batch), Path(args.out_dir), args.seconds)
    else:
        missing = [f for f in ("prompts", "out") if not getattr(args, f)]
        if missing:
            print(f"error: --{' and --'.join(missing)} required (or use --batch)", file=sys.stderr)
            return 2
        specs = [spec_from_args(args)]

    key, source = load_api_key()

    if args.dry_run:
        print(json.dumps(
            {
                "dry_run": True,
                "model": MODEL,
                "api_version": args.api_version,
                "api_version_fallback": FALLBACK_API_VERSION,
                "output_format": {
                    "encoding": "raw 16-bit PCM -> WAV",
                    "sample_rate_documented": DOC_SAMPLE_RATE,
                    "sample_rate_actual": "read from chunk mime_type at runtime",
                    "channels": CHANNELS,
                },
                "api_key": {"present": key is not None, "source": source},
                "clips": [s.describe() for s in specs],
            },
            indent=2,
        ))
        if key is None:
            log("dry run OK — no GEMINI_API_KEY yet, so nothing was contacted.")
        return 0

    if key is None:
        print(
            "error: no GEMINI_API_KEY in the environment or ~/.claude/.env. "
            "Re-run with --dry-run to validate the config without a key.",
            file=sys.stderr,
        )
        return 2
    log(f"API key loaded from {source}")

    return asyncio.run(run(specs, key, args.api_version, args.verbose))


if __name__ == "__main__":
    sys.exit(main())
