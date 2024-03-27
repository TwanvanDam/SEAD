

class Coeff():
    def __init__(self):
        self.url = 'https://customer-janes-com.tudelft.idm.oclc.org/entityprofile/equipment/Equipment_12900/specifications?explorerState=7a3d6ad9-907d-4673-ab0d-8573805a660e&rootEntity=Equipment_12900'
        ###Tail
        self.f_l = 32.5 #fuselage length [m]
        self.wb = 14.01 #Wheelbase [m]
        self.wt = 5.04 #wheeltrack [m]

        ###Wing
        self.b = 28.08 #wingspan [m]
        self.A = 8.4 #Aspect ratio
        self.S = 93.50
        self.c = self.b / self.A
        self.cr = 5.28 #chord root length
        self.ct = 1.26 #chord tip length

        ##Tail
        self.b_t = 10.04 #Tail span
        self.Svt = 10 #fin area
        self.Sht = 17.76 #Tailplane area


        ###Control
        self.Sa = 3.53 #Aileron area [m^2]
        self.Sf = 17.08 #Flap area
        self.Ss = 3.62 #Spoiler area
        self.Sr = 2.30  # Rudder area
        self.Se = 3.96 #Elevator area

        ###Weights (tay620 engine) [kg]
        self.OEW = 24593
        self.MZFW = 35830 #Max zero fuel weight
        self.MRW = 43320 #Max ramp weight
        self.MTOW = 43090  #Max take of weight
        self.MLW = 38780 #Max landing weight
        self.MP = 11108 #Max payload

        ###Loading
        self.T = 61607*2 #Thrust N
        self.WS = self.MTOW / self.S #Max wing loading = kg/m2
        self.WT = self.MTOW / self.T #Thrust loading = kg/N



