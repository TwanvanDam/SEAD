from plots import calc_potato
from Fok100 import Coeff


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









