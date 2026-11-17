#!/usr/bin/env bash
# Regenerate the fab files for one board, or all of them:
#
#   scripts/export_production.sh                 # every board under PCB/
#   scripts/export_production.sh regulator       # one board
#
# Writes, under PCB/<board>/production/:
#   bom/<board>-bom.csv            purchasing BOM (stackup bom --locked)
#   gerbers/                       Gerbers (Protel extensions, X2), PTH/NPTH Excellon drills, drill maps, job file
#   placement/<board>-pos.csv      placement file, mm, both sides, DNP excluded
#   jlcpcb/<board>-gerbers.zip     everything in gerbers/, ready to upload to a fab
#
# Run from the repository root. Check the board first: stackup check, PCB in sync, and DRC
# (kicad-cli pcb drc --refill-zones --severity-all) with only the warnings its README documents.
set -euo pipefail

K=${KICAD_CLI:-/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli}
LAYERS=F.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts

boards=("$@")
if [ ${#boards[@]} -eq 0 ]; then
    for d in PCB/*/; do
        b=$(basename "$d")
        [ -f "PCB/$b/$b.kicad_pcb" ] && boards+=("$b")
    done
fi

for b in "${boards[@]}"; do
    pcb="PCB/$b/$b.kicad_pcb"
    out="PCB/$b/production"
    [ -f "$pcb" ] || { echo "no board at $pcb" >&2; exit 1; }
    echo "== $b"

    stackup check "PCB/$b/stackup/board.kdl" --locked
    stackup bom "PCB/$b/stackup/board.kdl" --locked > "$out/bom/$b-bom.csv"

    find "$out/gerbers" -type f ! -name .gitkeep -delete
    "$K" pcb export gerbers --check-zones --layers "$LAYERS" --subtract-soldermask -o "$out/gerbers/" "$pcb" >/dev/null
    "$K" pcb export drill --excellon-separate-th --generate-map --map-format gerberx2 -o "$out/gerbers/" "$pcb" >/dev/null
    "$K" pcb export pos --format csv --units mm --side both --exclude-dnp -o "$out/placement/$b-pos.csv" "$pcb" >/dev/null

    rm -f "$out/jlcpcb/$b-gerbers.zip"
    (cd "$out/gerbers" && find . -type f ! -name .gitkeep -exec basename {} \; | sort | xargs zip -q "../jlcpcb/$b-gerbers.zip")
    echo "   $(ls "$out/gerbers" | wc -l | tr -d ' ') files in gerbers/, $(unzip -l "$out/jlcpcb/$b-gerbers.zip" | tail -1 | awk '{print $2}') in the zip"
done
