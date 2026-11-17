#!/usr/bin/env python3
"""Regulator board: battery hot-plug spike at the Pololu D42V55Fx's VIN.

Plugging a charged battery into a module whose input is mostly low-ESR ceramic capacitance makes an
LC tank with the battery leads; the first overshoot can approach twice the battery voltage. The
D42V55Fx is rated to 60 V on VIN and the highest battery is about 32 V, so an undamped spike can come
close to it. C_IN (one Rubycon 63ZLJ100, 100 µF) on VRP damps the ringing.

C_IN sits behind the module's reverse-voltage protection. Its circuit is not published, so it is
modelled both ways: as a closed switch (protection FET on) and as a bare diode (FET still off at the
first edge). The module's own input capacitance is not published either, so it is swept, as are the
lead inductance (about 0.5-2 m of loosely routed battery wire) and C_IN's ESR (0.13 Ω max at 20 °C,
0.39 Ω max at -10 °C, Rubycon ZLJ table p. 3; lower when warm).

    python3 scripts/spice/regulator_hotplug_sim.py          # the design: exit 1 on any failure
    python3 scripts/spice/regulator_hotplug_sim.py --bare   # without C_IN: what the module sees alone
"""
import argparse
import sys

from ngspice_harness import NgSpice, report
from spice_lib import corners, peak, ramp, run_matrix

# ---- component values (keep in sync with PCB/regulator/stackup/board.kdl) -------------------------
C_IN = "100u"            # Rubycon 63ZLJ100M8X11.5
L_CIN = "20n"            # lead + can + trace inductance, estimate

# ---- limits ---------------------------------------------------------------------------------------
VIN_MAX = 60.0           # D42V55Fx VIN upper limit (PCB/datasheets/Pololu_D42V55F5.html, Connections)
VBATT = 32.0             # highest battery voltage the board is specified for

# ---- swept unknowns -------------------------------------------------------------------------------
PROTECTION = ("fet_on", "diode_only")   # module reverse protection, VIN -> VRP (unpublished)
C_MODULE = ("10u", "22u", "47u")        # module input capacitance, ceramic (unpublished; assumed)
L_LEADS = ("0.5u", "1u", "2u")          # battery lead loop inductance
ESR_CIN = ("0.05", "0.13", "0.39")      # C_IN ESR: warm, 20 °C max, -10 °C max
EDGE = "100n"                           # contact closure


def netlist(protection, c_module, l_leads, esr, bulk=True):
    prot = ("Rp vin vrp 0.01" if protection == "fet_on"
            else ".model DB D(IS=1e-12 N=1.2 RS=0.01)\nDp vin vrp DB")
    bulk_part = (f"Rb vrp b1 {esr}\nLb b1 b2 {L_CIN}\nCb b2 0 {C_IN}"
                 if bulk else "* C_IN removed")
    return f"""* regulator hot-plug
Vbat vb 0 {ramp(VBATT, EDGE, start='10u', end='1')}
Rbat vb l1 0.03
Ll l1 l2 {l_leads}
Rl l2 vin 0.02
{prot}
Cm vrp cm {c_module}
Rcm cm 0 0.005
{bulk_part}
Rload vrp 0 100
.tran 20n 400u uic
.end
"""


def hotplug(sim, bulk):
    def build(protection, c_module, l_leads, esr):
        return netlist(protection, c_module, l_leads, esr, bulk)

    def check(tr, c):
        vin = peak(tr.time, tr["vin"])
        vrp = peak(tr.time, tr["vrp"])
        ok = max(vin, vrp) <= VIN_MAX
        return ok, f"VIN peak {vin:.1f} V, VRP peak {vrp:.1f} V (limit {VIN_MAX:.0f} V)"

    esr = ESR_CIN if bulk else ESR_CIN[:1]
    return run_matrix(sim, "hotplug", build,
                      corners(protection=PROTECTION, c_module=C_MODULE, l_leads=L_LEADS, esr=esr),
                      ["vin", "vrp"], check)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--bare", action="store_true", help="remove C_IN")
    args = parser.parse_args(argv)
    return report(hotplug(NgSpice(), bulk=not args.bare))


if __name__ == "__main__":
    sys.exit(main())
