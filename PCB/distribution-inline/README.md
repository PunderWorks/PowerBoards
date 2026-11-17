# Inline Distribution Board

Five identical 2-pole terminals in a single row share a V+ plane (`VPWR`, top copper) and a ground
plane (`GND`, bottom copper). Any terminal can be the input; the other four are outputs. There are no
active or passive components.

This is the [distribution board](../distribution/README.md) laid out in one row instead of a 3 x 2 grid,
for where a long, narrow board fits better. The terminal, ratings and design decisions are the same;
only the layout differs, and that is described here.

## Ratings

| | |
|---|---|
| Current | **17.5 A total** through whichever terminal is the input, with 16 AWG wire (IEC/EN 60664-1 rating of the terminals). **10 A** if you need the UL/CSA rating. |
| Wire | 26-16 AWG solid, 24-16 AWG fine-stranded. Strip 8-9 mm. |
| Voltage | DC power distribution, far below the terminals' 160 V IEC / 300 V UL rating. |
| Polarity | `+` and `-` are printed behind every terminal. Any terminal can be the input. |
| Mounting | Four M3 holes. Screws and standoffs may be metal: copper is kept clear of every hole. |

The input terminal carries the sum of every output's current, so the 17.5 A limit applies to the total,
not to each output. See the [distribution board README](../distribution/README.md#terminal-wago-2601-1102)
for the terminal's datasheet figures.

The electrical design is in [Stackup KDL](stackup/board.kdl), using the shared
[parts file](../libraries/stackup/parts.kdl). The KiCad PCB (`distribution-inline.kicad_pcb`) is linked
to it through `distribution-inline.stackup_sch`; sync it with the Stackup KiCad plugin. Run
`stackup check PCB/distribution-inline/stackup/board.kdl --locked` from the repository root before
syncing.

## Hardware overview

| Ref | Function | Part |
|---|---|---|
| J1-J5 | Power terminal, input or output | WAGO 2601-1102 |

Every terminal has pin 1 (square pad, `+` on the silkscreen) on `VPWR` and pin 2 (`-`) on `GND`.

## Layout

- **65.5 x 24 mm, one row.** J1-J5 sit on the same 10 mm pitch as the 3 x 2 board (8.5 mm body plus
  room to work the levers), all with their wires entering from the bottom edge. The wire entry faces
  are flush with that edge, so the 10 `silk_edge_clearance` DRC warnings (two per terminal) are
  expected, as on the 3 x 2 board.
- **Ratings across the top.** A single row leaves no side strips tall enough for text, so "17.5A MAX
  TOTAL / 16 AWG" and "WIRE 26-16 AWG / STRIP 8-9mm" run as two lines along the top edge, above the `+`
  and `-` marks.
- **Four M3 mounting holes on side extensions**, two each side, each centre 4.45 mm from the nearest
  terminal body, with the same 8 mm copper keep-out on both layers.
- **Planes, not traces.** V+ on top and GND on the bottom span the whole board, joined to the pads
  through thermal reliefs with 1.0 mm spokes (8 mm of copper per pole), as on the 3 x 2 board.
- **Back:** the 10 mm PunderWorks logo beside "POWER DISTRIBUTION" and the IEC/UL ratings.

## Bench checklist

- Before connecting a load, check continuity between all five `+` pins and between all five `-` pins,
  and confirm there is no short between V+ and GND.
- Run the full intended load through the input and one output, and check the input terminal and the
  board near it for heating.
