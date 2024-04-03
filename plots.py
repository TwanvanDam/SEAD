import matplotlib.pyplot as plt
import numpy as np
from Fok100 import Coeff

def piechart(data, plot):
    categories, weights = list(data.keys()) ,list(data.values())

    plt.figure()
    plt.pie(weights, labels=categories, autopct=lambda p: '{:,.0f} [kg]  \n {:.1f}%'.format((p / 100) * sum(weights), p), startangle=90)
    plt.axis('equal')
    plt.title('Distribution of weights')
    plt.savefig("./Plots/piechart.pdf")
    if plot:
        plt.show()

def control_stability(x_range, control, stability, stability_static_margin, plot,y, cg):
    plt.plot(x_range, control, color='red', label='Control')
    plt.fill_between(x_range, control, facecolor='red', alpha=0.5, label='Not controllable')
    plt.plot(x_range, stability, color='blue',label='Stability')
    plt.axhline(y, cg[0], cg[1], label='Operational CG range', color='g')
    plt.fill_between(x_range+stability_static_margin, stability, facecolor='blue', alpha=0.5, label='Not stable')
    plt.ylim([0,1*np.max([np.max(stability), np.max(control)])])
    plt.xlim([np.min(x_range), np.max(x_range)])
    plt.xlabel(r'$x$ [mac]')
    plt.ylabel(r'$S_h/S$ [-]')
    plt.legend()
    plt.savefig("./Plots/scissor.pdf")
    if plot:
        plt.show()

def stability(c: Coeff):
    x = np.arange(0, 1, 0.01)
    a = 1 / (c.C_L_alpha_h() / c.C_L_alpha_Ah(c.C_L_alpha_w()) * (1-c.de_dalpha(c.sweep(0.25), c.C_L_alpha_w())) * c.l_h/c.MAC * c.Vh_V_square()) #TODO downwash 0?
    y  =  a * x - (c.x_ac(0.29, c.C_L_alpha_Ah(c.C_L_alpha_w())) - 0.05) * a
    print(c.x_ac(0.29, c.C_L_alpha_Ah(c.C_L_alpha_w())))
    return y

def control(c: Coeff):
    x = np.arange(0, 1, 0.01)
    a = 1 / ((-0.8 * c.l_h * c.Vh_V_square())/(c.C_L_AminH() * c.MAC))
    y = a * x + (c.C_m_ac()/c.C_L_AminH() - c.x_ac(0.27, c.C_L_alpha_Ah(c.C_L_alpha_w())))*a
    return y

if __name__ == "__main__":
    x = np.arange(0, 1, 0.01)
    # stability = -1.2 + 3*x
    # control = 1.5 - 2*x
    stability_static_margin = 0.05
    control_stability(x, control(Coeff(0.193)), stability(Coeff(0.77)), stability_static_margin)

