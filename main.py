from Fok100 import Coeff as C100
from plots import piechart, stability, control, control_stability
from cgfunc import cg_calc, cg_calc_oew, convert_global_xlemac
from Potato import calc_potato
import numpy as np


def model(coeff, plot):
    ### Pie chart
    Fokker = coeff(0.77)
    data = {'OEW': Fokker.OEW,'Fuel': Fokker.MTOW- Fokker.MP - Fokker.OEW,'Payload': Fokker.MP} #how is fuel weight OEW - Wpayload
    piechart(data, plot)

    ### CG calculation
    ### I & II & III
    # cg_chord_factor = 0.4
    # cg_engine_factor = 0.5
    # m = Fokker.MTOW
    # wing_group = {'Wing': [0.1477*m, Fokker.LEMAC + cg_chord_factor * Fokker.MAC], 'lgear': [0.0271*m, Fokker.dw + Fokker.wb]}
    # fuselage_group =  {'Htail':[0.0137*m, Fokker.LEMACH + cg_chord_factor* Fokker.MACH], 'Vtail': [0.0095*m, Fokker.LEMACV + cg_chord_factor* Fokker.MACV],
    #                 'fuselage': [0.1929*m, 0.47*Fokker.f_l], 'ngear':[0.0047*m, Fokker.dw],
    #                 'nacelle':[0.0183*m, Fokker.de + cg_engine_factor * Fokker.ln], 'Prop':[0.0912*m, Fokker.de + cg_engine_factor * Fokker.ln]}
    cg_wing = cg_calc(Fokker.wing_group)
    cg_fuselage = cg_calc(Fokker.fuselage_group)

    cg_OEW = cg_calc({**Fokker.wing_group, **Fokker.fuselage_group})


    #TODO below values guessed
    cargo_hold_locations = (0.3 * Fokker.f_l,0.7 * Fokker.f_l)
    first_row = 6.56
    tank_location = Fokker.LEMAC + 0.5 * Fokker.MAC
    potato = calc_potato(cg_OEW, Fokker.OEW, Fokker.maxc, cargo_hold_locations, (Fokker.holdf, Fokker.holda),Fokker.massp/109,first_row, tank_location, Fokker.MRW - Fokker.MZFW, Fokker.LEMAC, Fokker.MAC, plot=False,name='Fokker 100')
    potato = calc_potato(cg_OEW+0.1, Fokker.OEW, Fokker.maxc, cargo_hold_locations, (Fokker.holdf, Fokker.holda),
                         Fokker.massp / 109, first_row, tank_location, Fokker.MRW - Fokker.MZFW, Fokker.LEMAC,
                         Fokker.MAC, plot=False, name='Fokker 120')

    stability_static_margin = 0.05
    control_stability(np.arange(0, 1, 0.01), control(coeff(0.193)), stability(coeff(0.77)), stability_static_margin, plot, Fokker.Sht/Fokker.S, potato)

if __name__ == '__main__':
    plot = True
    model(C100, plot)
    # # print(Fokker.cf * np.cos(np.radians(42))*0.75/3.33 + 1)
    # print(Fokker.b**2 / ((1+Fokker.Swf/Fokker.S*(Fokker.cprimec -1))*Fokker.S))
    # print(Fokker.C_L_AminH())