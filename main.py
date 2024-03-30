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
wing_group = {'Wing': [0.1477, np.nan], 'lgear': [0.0271, np.nan]}
fuselage_group =  {'Htail':[0.0137, np.nan], 'Vtail': [0.0095, np.nan],
                'fuselage': [0.1929, 0.47*Fokker.f_l], 'ngear':[0.0047, np.nan],
                'nacelle':[0.0183, np.nan], 'Prop':[0.0912, np.nan]}
cg_wing = cg_calc(wing_group)
cg_fuselage = cg_calc(fuselage_group)

cg_OEW = cg_calc({**wing_group, **fuselage_group})

