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
    Fokker100.loading_diagram(plot)
    Fokker120.loading_diagram(plot)

    Fokker100.loading_diagram(two_plots=True, show_cg_limits=True,show_plot=False)
    Fokker120.loading_diagram(show_plot=plot, two_plots=True ,show_cg_limits=True, battery_before_boarding=True)

    stability_static_margin = 0.05
    control_stability(np.arange(0, 1, 0.01), control(coeff100(0.193)), stability(coeff100(0.77)), stability_static_margin, plot, Fokker100.Sht/Fokker100.S, Fokker100.cg_range, Fokker100.name)
    control_stability(np.arange(0, 1, 0.01), control(coeff120(0.193)), stability(coeff120(0.77)), stability_static_margin, plot, Fokker120.Sht / Fokker120.S, Fokker120.cg_range, Fokker120.name)

if __name__ == '__main__':
    plot = True
    model(C100, C120, plot)
    # # print(Fokker.cf * np.cos(np.radians(42))*0.75/3.33 + 1)
    # print(Fokker.b**2 / ((1+Fokker.Swf/Fokker.S*(Fokker.cprimec -1))*Fokker.S))
    # print(Fokker.C_L_AminH())