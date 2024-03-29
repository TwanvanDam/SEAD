from Fok100 import Coeff
from plots import piechart
from cgfunc import cg_calc
import numpy as np

plot= False
Fokker = Coeff()
### Pie chart
data = {'OEW': Fokker.OEW,'Fuel': Fokker.OEW - Fokker.MP,'Payload': Fokker.MP}
piechart(data, plot)

### CG calculation
data = {'Wing': [0.1477, np.nan], 'Htail':[0.0137, np.nan], 'Vtail': [0.0095, np.nan],
        'fuselage': [0.1929, 0.47*Fokker.f_l], 'ngear':[0.0047, np.nan], 'lgear': [0.0271, np.nan],
        'nacelle':[0.0183, np.nan], 'Prop':[0.0912, np.nan]}
cgoew = cg_calc(data)

