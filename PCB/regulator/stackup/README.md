# Regulator board Stackup design

`board.kdl` defines the electrical design. Its parts, with their manufacturer part numbers and
datasheet notes, go in the shared [`../../libraries/stackup/parts.kdl`](../../libraries/stackup/parts.kdl).

The board layout is in `../regulator.kicad_pcb`. To check the design, run
`stackup check PCB/regulator/stackup/board.kdl` from the repository root. To update the
PCB, use the Stackup KiCad plugin with `PCB/regulator/regulator.stackup_sch`.
Run `stackup bom PCB/regulator/stackup/board.kdl --locked` to export the purchasing CSV.
