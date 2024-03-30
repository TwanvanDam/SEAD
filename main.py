from Fok100 import Coeff
from plots import piechart
from cgfunc import cg_calc
import numpy as np

plot= False
Fokker = Coeff()
### Pie chart
data = {'OEW': Fokker.OEW,'Fuel': Fokker.OEW - Fokker.MP,'Payload': Fokker.MP} #how is fuel weight OEW - Wpayload
piechart(data, plot)

### CG calculation
### I & II & III
cg_chord_factor = 0.4
cg_engine_factor = 0.5
wing_group = {'Wing': [0.1477, Fokker.LEMAC + cg_chord_factor * Fokker.MAC], 'lgear': [0.0271, Fokker.dw + Fokker.wb]}
fuselage_group =  {'Htail':[0.0137, Fokker.LEMACH + cg_chord_factor* Fokker.MACH], 'Vtail': [0.0095, Fokker.LEMACV + cg_chord_factor* Fokker.MACV],
                'fuselage': [0.1929, 0.47*Fokker.f_l], 'ngear':[0.0047, Fokker.dw],
                'nacelle':[0.0183, Fokker.de + cg_engine_factor * Fokker.ln], 'Prop':[0.0912, Fokker.de + cg_engine_factor * Fokker.ln]}
cg_wing = cg_calc(wing_group)
cg_fuselage = cg_calc(fuselage_group)

cg_OEW = cg_calc({**wing_group, **fuselage_group})


