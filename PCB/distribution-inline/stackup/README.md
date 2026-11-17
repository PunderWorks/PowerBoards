# Inline distribution board Stackup design

`board.kdl` defines the electrical design. Its only part, the WAGO 2601-1102 terminal block (with its
MPN and LCSC number), is in the shared [`../../libraries/stackup/parts.kdl`](../../libraries/stackup/parts.kdl).

The board layout is in `../distribution-inline.kicad_pcb`. To check the design, run
`stackup check PCB/distribution-inline/stackup/board.kdl --locked` from the repository root. To update
the PCB, use the Stackup KiCad plugin with `PCB/distribution-inline/distribution-inline.stackup_sch`.
Run `stackup bom PCB/distribution-inline/stackup/board.kdl --locked` to export the purchasing CSV.
