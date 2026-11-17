# Regulator Board

A power distribution board with a plug-in step-down regulator. One WAGO terminal takes the battery and
feeds a Pololu D42V55Fx module plugged into a socket in the middle of the board; the module's output
feeds a V+ plane shared by four more WAGO terminals, over a GND plane. The output voltage is whichever
module is plugged in: **D42V55F5 for 5 V, D42V55F12 for 12 V**. Swapping the module changes the board's
output; nothing else on the board changes.

The electrical design is in [Stackup KDL](stackup/board.kdl), using the shared
[parts file](../libraries/stackup/parts.kdl). The KiCad PCB (`regulator.kicad_pcb`) is linked to it
through `regulator.stackup_sch`; sync it with the Stackup KiCad plugin. Run
`stackup check PCB/regulator/stackup/board.kdl --locked` from the repository root before syncing.

## Ratings

| | 5 V (D42V55F5) | 12 V (D42V55F12) |
|---|---|---|
| Input | 9-32 V DC (module: up to 60 V) | 14-32 V DC (module: up to 60 V) |
| Output current, total | **6 A** | **5 A** |
| What limits it | The module's two VOUT header pins, 3 A each | The module's thermal limit, derated for an enclosure |
| Module alone, 24-32 V in, open air | 7.1-6.8 A | 5.9-5.4 A |
| Wire | 26-16 AWG, strip 8-9 mm (WAGO 2601) | Same |

The four outputs share the total; it is not per output. Input current is far lower than the output
current: about 2.8 A at 24 V in for 12 V x 5 A out. The terminals (17.5 A IEC) are nowhere near their
limit.

Module currents are from Pololu's "maximum continuous output current" graph on the
[product page](../datasheets/Pololu_D42V55F5.html) (room temperature, still air, no heat sinking).
The 9 V and 14 V input minimums are a working allowance for dropout at full load, not Pololu figures;
see the dropout graph on the product page.

## Parts

| Ref | Function | Part | Notes |
|---|---|---|---|
| J1 (`J_IN`) | Battery input | WAGO 2601-1102 | Pin 1 VIN, pin 2 GND |
| J2-J5 (`J_OUT1-4`) | Regulated outputs | WAGO 2601-1102 | Pin 1 VOUT, pin 2 GND |
| J6 (`J_REG`) | Regulator socket | Samtec SSW-106-01-T-D, 2x6 female, 2.54 mm | 4.7 A per contact. Second source Sullins PPTC062LFBN-RC |
| C1 (`C_IN`) | Input bulk, on VRP | Rubycon 63ZLJ100M8X11.5, 100 µF 63 V | Damps hot-plug ringing |
| — | Regulator module | Pololu D42V55F5 (#5571) or D42V55F12 (#5577) | Bought separately, plugs into J6 on its supplied male headers |

## Design decisions

- **A plug-in module, not a regulator on the board.** The board stays passive and through-hole, and one
  PCB covers every output voltage. The D42V55Fx family was chosen over the D36V50Fx for its 60 V input
  (against 50 V), which leaves room above 32 V battery peaks and hot-plug spikes, and for holding more
  current near 32 V in. Its pins are a 2x6 grid on 0.1" pitch in the order EN/PG, VRP, VIN, GND, GND,
  VOUT, with EN on the edge row and PG on the inner row. The D36V50Fx has the same order and should fit
  the same socket, but that is from Pololu's pinout photos, not a dimensioned drawing.
- **One input capacitor, no TVS.** With the module alone, simulated hot-plug at 32 V through 0.5-2 µH
  of battery lead peaks at up to 57 V at VIN, close to the 60 V limit. C_IN brings the worst case to 42 V.
  See `scripts/spice/regulator_hotplug_sim.py` (`--bare` for the module alone).
- **C_IN is on VRP, not VIN.** VRP is the module's input after its reverse-voltage protection. A
  polarized capacitor there is never reverse-biased by a battery wired backwards, so there is no need for
  a bipolar capacitor (the 63 V ones are poorly stocked) or a back-to-back pair. The simulation models
  the unpublished protection both as a closed switch and as a bare diode; both pass.
- **No extra output capacitor.** The module carries its own output capacitors, and Pololu gives no
  guidance on adding more.
- **EN and PG unconnected.** The module pulls EN up to VIN through 1 MΩ, so it is always on. No on/off
  switch, LED, servo headers, USB or VIN passthrough: the board is meant to stay simple. A distribution
  board on the battery side gives a passthrough if one is needed.
- **Inspiration:** the Sure Robotics DC Converter (6 A, 9-36 V in, 5/6 V out, four screw-terminal
  outputs).

## Not yet verified

- The D42V55Fx's reverse-voltage limit is not published. Pololu says only that VIN has reverse
  protection.
- The module's input capacitance and protection circuit are not published. The simulation sweeps both.
- The socket position relative to the module's outline and M2 mounting holes comes from photos.
  Pololu publishes no dimensioned drawing for the D42V55Fx.

## Bench checklist

- Before fitting the module, check continuity: J1 pin 1 to J6 pads 5-6; J2-J5 pin 1 to J6 pads 11-12;
  every terminal's pin 2 to J6 pads 7-10; C1 `+` to J6 pads 3-4. Confirm there is no short from VIN,
  VRP or VOUT to GND.
- Check that a D42V55F5 and a D42V55F12 both seat fully in J6, with the body over the marked outline. If
  a D36V50Fx is available, check that it seats too.
- Power up from a current-limited bench supply at 12 V and then 32 V, with no load. Check VOUT.
- Hot-plug a charged battery (or a 32 V supply on a long lead) several times, scoping VIN at J6.
  Expect under about 45 V peak.
- Run the rated load (6 A at 5 V, 5 A at 12 V) through all four outputs for 15 minutes at the highest
  battery voltage. Check the module, C1 and the terminals for heat, and VOUT for droop.
