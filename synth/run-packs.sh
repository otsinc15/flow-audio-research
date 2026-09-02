#!/usr/bin/env bash
# Round 5 pipeline: ingest a loop pack, audition it, then layer it.
#   ./synth/run-packs.sh <PACK_DIR> <PACK_NAME> [OUTDIR]
# Uses the same venv convention as run.sh. Writes no audio into the repo.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACK="${1:?usage: run-packs.sh <PACK_DIR> <PACK_NAME> [OUTDIR]}"
NAME="${2:?usage: run-packs.sh <PACK_DIR> <PACK_NAME> [OUTDIR]}"
OUT="${3:-$HOME/Documents/AI Agent Outputs/Artifacts/flow-audio-candidates/round5-packs}"
UV="${UV:-$HOME/.local/bin/uv}"
VENV="${VENV:-$HERE/.venv}"

if [ ! -x "$VENV/bin/python" ]; then
  "$UV" venv "$VENV"
  VIRTUAL_ENV="$VENV" "$UV" pip install numpy scipy soundfile pyloudnorm librosa static-ffmpeg
fi
PY="$VENV/bin/python"
INV="$HERE/.pack-$NAME.json"
DOC="$HERE/../research/ear-test/pack-inventory-$NAME.md"

"$PY" "$HERE/packs.py" --pack "$PACK" --name "$NAME" --out "$DOC" --json "$INV"
"$PY" "$HERE/layer.py" audition --inv "$INV" --out "$OUT/audition" --wipe
"$PY" "$HERE/layer.py" combos   --inv "$INV" --out "$OUT/combos"   --wipe
echo "inventory -> $DOC"
echo "audio     -> $OUT"
