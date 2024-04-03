import matplotlib.pyplot as plt
import numpy as np
# from Fok100 import Coeff
import cgfunc

def piechart(data, plot, name):
    categories, weights = list(data.keys()) ,list(data.values())

    plt.figure()
    plt.pie(weights, labels=categories, autopct=lambda p: '{:,.0f} [kg]  \n {:.1f}%'.format((p / 100) * sum(weights), p), startangle=90)
    plt.axis('equal')
    plt.title('Distribution of weights')
    plt.savefig(f"./Plots/piechart_{name}.pdf")
    if plot:
        plt.show()

def calc_potato_pass(cg_0:float, OEW_0:float, Wpass:float, first_row:float, X_lemac:float=0, mac:float=1,plot:bool=True, boarding_order:tuple=("windows", "aisles", "middle"), n_rows:int=22, pitch:int=32, color=None) -> tuple:
    """This function calculates the loading diagram of the passengers with the given inputs and returns the minimum and maximum cg locations.
    :param cg_0: initial cg location at OEW measured from front of aircraft
    :param OEW_0: Operating Empty Weight
    :param Wpass: Weight of a single passenger
    :param first_row: Distance from nose to first row of seats
    :param X_lemac: Distance from nose to leading edge of mean aerodynamic chord
    :param mac: Mean aerodynamic chord if mac=1 and X_lemac=0, the cg locations will be in meters from the nose
    :param plot: Boolean to determine if a plot should be displayed
    :param boarding_order: Tuple with the order of boarding the passengers, by default it is ("windows", "aisles", "middle")
    :param n_rows: Number of rows in the aircraft, by default it is 22
    :param pitch: Distance between rows, by default it is 32 inch
    :return: Tuple with the minimum and maximum cg locations in the global coordinate system
    """
    min_cg = np.inf
    max_cg = -np.inf
    for dir in ["back", "forward"]:
        OEW_pax = [OEW_0]
        cg_pax = [cg_0]
        for column in boarding_order:
            cg_pax = [cg_pax[-1]]
            OEW_pax = [OEW_pax[-1]]
            n_pax_row = 2
            if dir == "back":
                if column == "middle":
                    rows = range(n_rows - 1)
                    n_pax_row = 1
                else:
                    rows = range(n_rows)
            if dir == "forward":
                if column == "middle":
                    rows = range(n_rows - 2, -1, -1)
                    n_pax_row = 1
                else:
                    rows = range(n_rows - 1, -1, -1)
            for i in rows:
                cg_pax.append(cgfunc.xcg_new(OEW_pax[-1], n_pax_row * Wpass, cg_pax[-1], first_row + i * pitch * 0.0254))
                OEW_pax.append(n_pax_row*Wpass + OEW_pax[-1])
            min_cg = np.min([min_cg, *cg_pax])
            max_cg = np.max([max_cg, *cg_pax])
            if color == None:
                plt.plot(cgfunc.convert_global_xlemac(cg_pax,X_lemac,mac), OEW_pax,".-", label=dir+ " " + column)
            else:
                plt.plot(cgfunc.convert_global_xlemac(cg_pax,X_lemac,mac), OEW_pax, color=color)
    return cg_pax[-1], OEW_pax[-1], min_cg, max_cg

def calc_potato_cargo(cg_0:float, OEW_0:float, Wcargo:float, cargo_hold_locations:tuple, cargo_volumes:tuple, X_lemac:float=0, mac:float=1, plot:bool=True, color=None) -> tuple:
    """This function calculates the loading diagram of the cargo with the given inputs and returns the minimum and maximum cg locations.
    :param cg_0: initial cg location at OEW measured from front of aircraft
    :param OEW_0: Operating Empty Weight
    :param Wcargo: Cargo weight excluding the passengers
    :param cargo_hold_locations: Tuple with the locations of the cargo holds measured from front of aircraft
    :param cargo_volumes: Tuple with the volumes of the cargo holds
    :param X_lemac: Distance from nose to leading edge of mean aerodynamic chord
    :param mac: Mean aerodynamic chord if mac=1 and X_lemac=0, the cg locations will be in meters from the nose
    :param plot: Boolean to determine if a plot should be displayed
    :return: Tuple with the minimum and maximum cg locations in the global coordinate system
    """

    total_volume = sum(cargo_volumes)
    cargo_weights = Wcargo * (np.array(cargo_volumes) / total_volume)
    print(cargo_weights)
    print((np.array(cargo_hold_locations)-X_lemac)/mac)
    min_cg = np.inf
    max_cg = -np.inf

    for dir in ["back", "forward"]:
        OEW_cargo = [OEW_0]
        cg_cargo = [cg_0]
        i = 1
        if dir == "back":
            cargo_zip = zip(cargo_weights, cargo_hold_locations)
        elif dir =="forward":
            cargo_zip = zip(cargo_weights[::-1], cargo_hold_locations[::-1])
        for cargo_weight, cargo_hold_location in cargo_zip:
            OEW_cargo = [OEW_cargo[-1]]
            cg_cargo = [cg_cargo[-1]]
            cg_cargo.append(cgfunc.xcg_new(OEW_cargo[-1],cargo_weight , cg_cargo[-1],cargo_hold_location))
            OEW_cargo.append(OEW_cargo[-1]+cargo_weight)
            min_cg = np.min([min_cg, *cg_cargo])
            max_cg = np.max([max_cg, *cg_cargo])
            if color == None:
                if i:
                    line, = plt.plot(cgfunc.convert_global_xlemac(cg_cargo,X_lemac,mac),OEW_cargo, label=f"cargo {dir}")
                    i = 0
                else:
                    plt.plot(cgfunc.convert_global_xlemac(cg_cargo,X_lemac,mac), OEW_cargo, line.get_color())
            else:
                plt.plot(cgfunc.convert_global_xlemac(cg_cargo,X_lemac,mac), OEW_cargo, color=color)
    return cg_cargo[-1], OEW_cargo[-1], min_cg, max_cg

def calc_potato_fuel(cg_0:float, OEW:float, Wfuel, tank_location, X_lemac:float=0, mac:float=1, plot:bool=True, color=None) -> tuple:
    """This function calculates the loading diagram of the fuel with the given inputs and returns the minimum and maximum cg locations.
    :param cg_0: initial cg location at OEW measured from front of aircraft
    :param OEW: Operating Empty Weight
    :param Wfuel: Tuple with the weights of the fuel tanks
    :param tank_location: Tuple with the locations of the fuel tanks measured from front of aircraft
    :param X_lemac: Distance from nose to leading edge of mean aerodynamic chord
    :param mac: Mean aerodynamic chord if mac=1 and X_lemac=0, the cg locations will be in meters from the nose
    :param plot: Boolean to determine if a plot should be displayed
    :return: Tuple with the minimum and maximum cg locations in the global coordinate system
    """

    min_cg = np.inf
    max_cg = -np.inf
    OEW_fuel = [OEW]
    cg_fuel = [cg_0]
    if (type(Wfuel) != tuple) & (type(tank_location) != tuple):
        Wfuel = [Wfuel]
        tank_location = [tank_location]
    for tank_weight, location in zip(Wfuel, tank_location):
        cg_fuel.append(cgfunc.xcg_new(OEW_fuel[-1], tank_weight, cg_fuel[-1], location))
        OEW_fuel.append(OEW_fuel[-1] + tank_weight)
        min_cg = np.min([min_cg, *cg_fuel])
        max_cg = np.max([max_cg, *cg_fuel])
        if color == None:
            plt.plot(cgfunc.convert_global_xlemac(cg_fuel,X_lemac,mac), OEW_fuel, label="fuel")
        else:
            if color == "b":
                name = "Fokker 100"
            if color == "r":
                name = "Fokker 120"
            plt.plot(cgfunc.convert_global_xlemac(cg_fuel,X_lemac,mac), OEW_fuel, color=color, label=name)
    return cg_fuel[-1], OEW_fuel[-1], min_cg, max_cg

def calc_potato(cg_0:float, OEW:float, Wcargo:float, cargo_hold_locations:tuple, cargo_volumes:tuple, Wpass:float, first_row:float,tank_location:tuple,Wfuel:tuple ,X_lemac:float=0, mac:float=1,plot:bool=True,name=None):
    """This function calculates the loading diagram of the aircraft with the given inputs and returns the minimum and maximum cg locations.
    :param cg_0: initial cg location at OEW measured from front of aircraft
    :param OEW: Operating Empty Weight
    :param Wcargo: Cargo weight excluding the passengers
    :param cargo_hold_locations: Tuple with the locations of the cargo holds measured from front of aircraft
    :param cargo_volumes: Tuple with the volumes of the cargo holds
    :param Wpass: Weight of a single passenger
    :param first_row: Distance from nose to first row of seats
    :param X_lemac: Distance from nose to leading edge of mean aerodynamic chord
    :param mac: Mean aerodynamic chord if mac=1 and X_lemac=0, the cg locations will be in meters from the nose
    :param plot: Boolean to determine if a plot should be displayed
    :return: Tuple with the minimum and maximum cg locations in the local coordinate system
    """
    if name == None:
        color = None
    if name == "Fokker 100":
        color = "b"
    if name == "Fokker 120":
        color = "r"
    cg_cargo, OEW_cargo, min_cg_cargo, max_cg_cargo = calc_potato_cargo(cg_0,OEW, Wcargo, cargo_hold_locations, cargo_volumes,X_lemac,mac, plot, color=color)
    cg_pass, OEW_pass, min_cg_pass, max_cg_pass = calc_potato_pass(cg_cargo, OEW_cargo, Wpass, first_row,X_lemac, mac, plot, color=color)
    cg_fuel, OEW_fuel, min_cg_fuel, max_cg_fuel = calc_potato_fuel(cg_pass, OEW_pass, Wfuel, tank_location,X_lemac, mac, plot, color=color)
    min_cg = (min(min_cg_cargo,min_cg_pass, min_cg_fuel)-X_lemac)/mac
    max_cg = (max(max_cg_pass,max_cg_cargo, max_cg_fuel)-X_lemac)/mac
    if name == None or name == "Fokker 120":
        plt.grid()
        plt.axvline(min_cg - 0.02, color='k')
        plt.axvline(max_cg + 0.02, color='k')
        plt.ylabel("mass [kg]")
        plt.xlabel(r"$x_{cg}$ [mac]")
        plt.legend()
        plt.savefig("./Plots/potato.pdf")
        plt.show()
    return min_cg, max_cg


def control_stability(x_range, control, stability, stability_static_margin, plot,y, cg):
    plt.plot(x_range, control, color='red', label='Control')
    plt.fill_between(x_range, control, facecolor='red', alpha=0.5, label='Not controllable')
    plt.plot(x_range, stability, color='blue',label='Stability')
    plt.hlines(y, np.min(x_range), np.max(x_range),"k","--", label=r'Fokker 100 $S_h/S$')
    plt.axhline(y, cg[0], cg[1], label='Operational CG range', color='g')
    plt.fill_between(x_range+stability_static_margin, stability, facecolor='blue', alpha=0.5, label='Not stable')
    plt.ylim([0,1*np.max([np.max(stability), np.max(control)])])
    plt.xlim([np.min(x_range), np.max(x_range)])
    plt.xlabel(r'$x$ [mac]')
    plt.ylabel(r'$S_h/S$ [-]')
    plt.grid()
    plt.legend()
    plt.savefig("./Plots/scissor.pdf")
    if plot:
        plt.show()

def stability(c,wing_contribution=0.29):
    x = np.arange(0, 1, 0.01)
    CLalphaw = c.C_L_alpha_w()
    CLalphah = c.C_L_alpha_h()
    CLalphaAh = c.C_L_alpha_Ah(CLalphaw)
    deda = 0* c.de_dalpha(c.sweep(0.25), CLalphaw)
    x_ac = c.x_ac(wing_contribution, c.C_L_alpha_Ah(CLalphaw))

    a = (CLalphah / CLalphaAh) * (1-deda) * (c.l_h/c.MAC) * c.Vh_V_square() #TODO downwash 0?
    y  =  x/a - (x_ac - 0.05)/a
    return y

def control(c, wing_contribution=0.27):
    x = np.arange(0, 1, 0.01)
    a = 1 / ((-0.8 * c.l_h * c.Vh_V_square())/(c.C_L_AminH() * c.MAC))
    y = a * x + (c.C_m_ac()/c.C_L_AminH() - c.x_ac(wing_contribution, c.C_L_alpha_Ah(c.C_L_alpha_w()))) * a
    return y

if __name__ == "__main__":
    x = np.arange(0, 1, 0.01)
    # stability = -1.2 + 3*x
    # control = 1.5 - 2*x
    stability_static_margin = 0.05
    # control_stability(x, control(Coeff(0.193)), stability(Coeff(0.77)), stability_static_margin)

