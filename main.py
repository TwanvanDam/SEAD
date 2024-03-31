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
m = Fokker.MTOW
wing_group = {'Wing': [0.1477*m, Fokker.LEMAC + cg_chord_factor * Fokker.MAC], 'lgear': [0.0271*m, Fokker.dw + Fokker.wb]}
fuselage_group =  {'Htail':[0.0137*m, Fokker.LEMACH + cg_chord_factor* Fokker.MACH], 'Vtail': [0.0095*m, Fokker.LEMACV + cg_chord_factor* Fokker.MACV],
                'fuselage': [0.1929*m, 0.47*Fokker.f_l], 'ngear':[0.0047*m, Fokker.dw],
                'nacelle':[0.0183*m, Fokker.de + cg_engine_factor * Fokker.ln], 'Prop':[0.0912*m, Fokker.de + cg_engine_factor * Fokker.ln]}
cg_wing = cg_calc(wing_group)
cg_fuselage = cg_calc(fuselage_group)

cg_OEW = cg_calc({**wing_group, **fuselage_group})
print(cg_OEW, Fokker.dw + Fokker.wb)


