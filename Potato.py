import matplotlib.pyplot as plt
import numpy as np
from Fok100 import Coeff
import cgfunc

def calc_potato_pass(cg_0:float, OEW_0:float, Wpass:float, first_row:float, X_lemac:float=0, mac:float=1, plot:bool=True, boarding_order:tuple=("windows", "aisles", "middle"), n_rows:int=22, pitch:int=32) -> tuple:
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
            if plot:
                plt.plot(cgfunc.convert_global_xlemac(cg_pax,X_lemac,mac), OEW_pax,".-", label=dir+ " " + column)
    return cg_pax[-1], OEW_pax[-1], min_cg, max_cg

def calc_potato_cargo(cg_0:float, OEW_0:float, Wcargo:float, cargo_hold_locations:tuple, cargo_volumes:tuple, X_lemac:float=0, mac:float=1, plot:bool=True) -> tuple:
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
            if plot:
                if i:
                    line, = plt.plot(cgfunc.convert_global_xlemac(cg_cargo,X_lemac,mac),OEW_cargo, label=f"cargo {dir}")
                    i = 0
                else:
                    plt.plot(cgfunc.convert_global_xlemac(cg_cargo,X_lemac,mac), OEW_cargo, line.get_color())
    return cg_cargo[-1], OEW_cargo[-1], min_cg, max_cg

def calc_potato_fuel(cg_0:float, OEW:float, Wfuel, tank_location, X_lemac:float=0, mac:float=1, plot:bool=True) -> tuple:
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
        if plot:
            plt.plot(cgfunc.convert_global_xlemac(cg_fuel,X_lemac,mac), OEW_fuel, label="fuel")
    return cg_fuel[-1], OEW_fuel[-1], min_cg, max_cg


def calc_potato(cg_0:float, OEW:float, Wcargo:float, cargo_hold_locations:tuple, cargo_volumes:tuple, Wpass:float, first_row:float,tank_location:tuple,Wfuel:tuple ,X_lemac:float=0, mac:float=1,plot:bool=True):
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

    cg_cargo, OEW_cargo, min_cg_cargo, max_cg_cargo = calc_potato_cargo(cg_0,OEW, Wcargo, cargo_hold_locations, cargo_volumes,X_lemac,mac, plot)
    cg_pass, OEW_pass, min_cg_pass, max_cg_pass = calc_potato_pass(cg_cargo, OEW_cargo, Wpass, first_row,X_lemac, mac, plot)
    cg_fuel, OEW_fuel, min_cg_fuel, max_cg_fuel = calc_potato_fuel(cg_pass, OEW_pass, Wfuel, tank_location,X_lemac, mac, plot)
    min_cg = (min(min_cg_cargo,min_cg_pass, min_cg_fuel)-X_lemac)/mac
    max_cg = (max(max_cg_pass,max_cg_cargo, max_cg_fuel)-X_lemac)/mac
    if plot:
        plt.grid()
        plt.axvline(min_cg, color='k')
        plt.axvline(max_cg, color='k')
        plt.ylabel("mass [kg]")
        plt.xlabel(r"$x_{cg}$ [mac]")
        plt.legend()
        plt.savefig("./Plots/potato.pdf")
        plt.show()
    return min_cg, max_cg

if __name__ == "__main__":
    # Dummy inputs
    Fokker = Coeff()

    first_row = 6.7  # [m]
    cg_0 = 17.66  # [m] from catia in whatsapp

    # Verified from here:
    pitch = 32 # [inch]
    n_seats = 109
    n_rows = 22

    # seats per row
    windows = 2
    aisles = 2
    middle = 1

    OEW = Fokker.OEW
    Wpass_tot = Fokker.MP - Fokker.maxc
    Wpass = Wpass_tot / n_seats
    Wcargo = Fokker.maxc
    Wfuel = Fokker.MRW - Fokker.MZFW



    cargo_hold_locations = (5,20)
    cargo_volumes = (Fokker.holdf, Fokker.holda)

    X_lemac = 16.13
    mac = 4
    tank_location = X_lemac+ 0.5 * mac

    calc_potato(cg_0, OEW, Wcargo, cargo_hold_locations, cargo_volumes, Wpass, first_row, tank_location, Wfuel, X_lemac, mac, plot=True)









