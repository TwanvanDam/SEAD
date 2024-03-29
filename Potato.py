import matplotlib.pyplot as plt
from Fok100 import Coeff
from cgfunc import xcg_new

#Dummy inputs
Fokker = Coeff()
First_row = 6.7 #[m]
cg = [23.66] #[m] from catia in whatsapp
OEW = [Fokker.OEW]
Wpass_tot = Fokker.MP - Fokker.maxc

#Verified from here:
pitch = 32 * 0.0254 #[m]
n_seats = 109
n_rows = 22

Wpass = Wpass_tot / n_seats

windows = 2 * n_rows
aisles = 2 * n_rows
middle = n_rows -1
assert windows + aisles + middle == n_seats

boarding_order = [windows, aisles, middle]

for column in boarding_order:
    #from front to back:
    for i in range(column):
        OEW.append(Wpass + OEW[-1])
        cg.append(xcg_new(OEW[-2], OEW[-1] + Wpass, cg[-1], First_row + i * pitch))
        print(First_row + i * pitch)

plt.plot(cg, OEW)
plt.show()










