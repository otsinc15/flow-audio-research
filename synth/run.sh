#!/usr/bin/env bash
# One command: build the venv (uv), render all six clips, measure them.
#   ./synth/run.sh [OUTDIR]
# Requires ~/.local/bin/uv. Writes WAVs to OUTDIR (default ./out) and the
# measurement table to OUTDIR/measurements.json. Never touches the repo.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="${1:-$HERE/out}"
UV="${UV:-$HOME/.local/bin/uv}"
VENV="${VENV:-$HERE/.venv}"

if [ ! -x "$VENV/bin/python" ]; then
  "$UV" venv "$VENV"
  VIRTUAL_ENV="$VENV" "$UV" pip install numpy scipy soundfile pyloudnorm librosa static-ffmpeg
fi
PY="$VENV/bin/python"
mkdir -p "$OUT"

# palette : seed : bpm  -- three clips per palette, different seeds and tempi
for spec in a:11:114.5 a:23:116.0 a:37:118.0 b:41:115.0 b:53:117.0 b:67:119.0; do
  IFS=: read -r pal seed bpm <<<"$spec"
  echo "rendering palette $pal seed $seed at $bpm BPM"
  ( cd "$HERE" && "$PY" render.py --palette "$pal" --seed "$seed" --bpm "$bpm" \
      --out "$OUT" --name "synth-$pal-$seed" >/dev/null )
done

"$PY" "$HERE/measure.py" "$OUT"/synth-*.wav > "$OUT/measurements.json"
echo "wrote $OUT/measurements.json"
