import matplotlib.pyplot as plt
import numpy as np
from Fok100 import Coeff
from cgfunc import xcg_new

def calc_potato_pass(cg_0:float, OEW_0:float, Wpass:float, first_row:float, X_lemac:float=0, mac:float=1, boarding_order:tuple=("windows", "aisles", "middle"), n_rows:int=22, pitch:int=32) -> tuple:
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
                cg_pax.append(xcg_new(OEW_pax[-1], n_pax_row * Wpass, cg_pax[-1], first_row + i * pitch * 0.0254))
                OEW_pax.append(n_pax_row*Wpass + OEW_pax[-1])
            min_cg = np.min([min_cg, *cg_pax])
            max_cg = np.max([max_cg, *cg_pax])
            plt.plot((np.array(cg_pax)-X_lemac)/mac, OEW_pax,".-", label=dir+ " " + column)
    return cg_pax[-1], OEW_pax[-1], min_cg, max_cg

def calc_potato_cargo(cg_0:float, OEW_0:float, Wcargo:float, cargo_hold_locations:tuple, cargo_volumes:tuple, X_lemac:float=0, mac:float=1) -> tuple:
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
            cg_cargo.append(xcg_new(OEW_cargo[-1],cargo_weight , cg_cargo[-1],cargo_hold_location))
            OEW_cargo.append(OEW_cargo[-1]+cargo_weight)
            min_cg = np.min([min_cg, *cg_cargo])
            max_cg = np.max([max_cg, *cg_cargo])

            if i:
                line, = plt.plot((np.array(cg_cargo)-X_lemac)/mac,OEW_cargo, label=f"cargo {dir}")
                i = 0
            else:
                plt.plot((np.array(cg_cargo)-X_lemac)/mac, OEW_cargo, line.get_color())
    return cg_cargo[-1], OEW_cargo[-1], min_cg, max_cg

def calc_potato(cg_0,OEW,Wcargo, cargo_hold_locations, cargo_volumes, Wpass, first_row,X_lemac, mac):
    cg_cargo, OEW_cargo, min_cg_cargo, max_cg_cargo = calc_potato_cargo(cg_0,OEW, Wcargo, cargo_hold_locations, cargo_volumes,X_lemac,mac)
    cg_0, OEW, min_cg_pass, max_cg_pass = calc_potato_pass(cg_cargo, OEW_cargo, Wpass, first_row,X_lemac, mac)
    min_cg = min(min_cg_cargo,min_cg_pass)
    max_cg = max(max_cg_pass,max_cg_cargo)
    plt.grid()
    plt.axvline((min_cg-X_lemac)/mac, color='k')
    plt.axvline((max_cg-X_lemac)/mac, color='k')
    plt.ylabel("mass [kg]")
    plt.xlabel(r"$x_{cg}$ [mac]")
    plt.legend()
    plt.show()

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

    cargo_hold_locations = (8, 20)
    cargo_volumes = (7, 3)

    X_lemac = 16.0
    mac = 2

    calc_potato(cg_0, OEW, Wcargo, cargo_hold_locations, cargo_volumes, Wpass,first_row,X_lemac, mac)











