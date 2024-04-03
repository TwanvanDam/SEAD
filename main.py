from Fok100 import Coeff as C100
from Fok120 import Coeff as C120
from plots import piechart, stability, control, control_stability
from cgfunc import cg_calc, cg_calc_oew, convert_global_xlemac
from Potato import calc_potato
import numpy as np


def model(coeff100, coeff120, plot):
    ### Pie chart
    Fokker100 = coeff100(0.77)
    Fokker120 = coeff120(0.77)
    Fokker100.pie_chart(plot)
    Fokker120.pie_chart(plot)

    ### CG calculation
    ### I & II & III
    cg_OEW = Fokker100.cg_oew
    cargo_hold_locations = (0.3 * Fokker100.f_l,0.7 * Fokker100.f_l)
    first_row = 6.56
    potato = calc_potato(cg_OEW, Fokker100.OEW, Fokker100.maxc, cargo_hold_locations, (Fokker100.holdf, Fokker100.holda),Fokker100.massp/109,first_row, Fokker100.tank_location, Fokker100.MRW - Fokker100.MZFW, Fokker100.LEMAC, Fokker100.MAC, plot=False,name='Fokker 100')
    potato = calc_potato(cg_OEW+0.1, Fokker100.OEW, Fokker100.maxc, cargo_hold_locations, (Fokker100.holdf, Fokker100.holda),
                         Fokker100.massp / 109, first_row, Fokker100.tank_location, Fokker100.MRW - Fokker100.MZFW, Fokker100.LEMAC,
                         Fokker100.MAC, plot=False, name='Fokker 120')

    stability_static_margin = 0.05
    control_stability(np.arange(0, 1, 0.01), control(coeff100(0.193)), stability(coeff100(0.77)), stability_static_margin, plot, Fokker100.Sht/Fokker100.S, potato, Fokker100.name)
    control_stability(np.arange(0, 1, 0.01), control(coeff120(0.193)), stability(coeff120(0.77)),
                      stability_static_margin, plot, Fokker120.Sht / Fokker120.S, potato, Fokker120.name)

if __name__ == '__main__':
    plot = True
    model(C100, C120, plot)
    # # print(Fokker.cf * np.cos(np.radians(42))*0.75/3.33 + 1)
    # print(Fokker.b**2 / ((1+Fokker.Swf/Fokker.S*(Fokker.cprimec -1))*Fokker.S))
    # print(Fokker.C_L_AminH())