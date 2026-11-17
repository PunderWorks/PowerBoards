# PowerBoards — Agent Notes

## What this is

A set of small power PCBs for droid builds, one folder per board under `PCB/`. See [README.md](README.md)
for the board list and status.

- **Distribution** (`PCB/distribution/`): six interchangeable WAGO 2601 lever terminals over shared V+ and
  GND planes. Any terminal can be the input. No active or passive components.
- **Regulator** (`PCB/regulator/`): not started. Its requirements and design decisions go in
  [PCB/regulator/README.md](PCB/regulator/README.md) once they are settled.

Each board's README records its requirements and the decisions behind them. Read it before changing that
board, and add to it rather than re-deciding something already settled there.

## Repository layout

- `manifest.kdl`: the Stackup version and the parts library, pinned by commit. Shared by every board.
- `PCB/<board>/`: the KiCad project (`<board>.kicad_pro`, `.kicad_pcb`, `.stackup_sch`), plus
  `stackup/board.kdl` (the circuit), `diagrams/`, `analysis/` and `production/`.
- `PCB/libraries/stackup/parts.kdl`: the Stackup parts shared by every board, with MPNs, LCSC numbers and
  datasheet notes. Add new parts here, not in a per-board `parts.kdl`.
- `PCB/libraries/PowerBoards.pretty/`: custom KiCad footprints. `PCB/libraries/3dmodels/`: 3D models (see
  its README for the models that cannot be redistributed).
- `PCB/datasheets/`: manufacturer datasheets, fetched with the `pcb-design` skill's `datasheet.py` and
  recorded in `manifest.json`.
- `scripts/spice/`: ngspice harnesses, named `<board>_<circuit>_sim.py`.

## Git workflow

**All changes go through pull requests. Never push directly to `main`.** History is linear: rebase,
never merge. Land PRs with `gh pr merge --rebase`. Check `git remote -v` for the remote to push to.

Because PRs land by rebase, `git branch -d` and `--merged` won't recognize a landed branch. Confirm via
`git log --oneline` or `gh pr view <branch> --json state`, then `git branch -D <branch>`.

## Hardware design (Stackup)

The electrical design is Stackup KDL (`PCB/<board>/stackup/board.kdl` plus the shared `parts.kdl`), not
KiCad schematics, of which there are none. Hardware work follows the `pcb-design` skill.

- Check a design with `stackup check PCB/<board>/stackup/board.kdl --locked` from the repository root
  (Stackup CLI 0.2).
- After any change to the KDL, sync `PCB/<board>/<board>.kicad_pcb` from it with the Stackup KiCad
  plugin (never edit footprint nets by hand), and commit the PCB with the KDL. Footprints record their
  `board.kdl` line, so even reordering lines needs a resync. A change to the shared `parts.kdl` can
  affect every board, so check and resync each board that uses the changed part.
- Mounting holes and logos are KiCad `board_only` footprints; the sync leaves them alone.
- Copper is kept clear of mounting holes so metal screws and standoffs are safe.
