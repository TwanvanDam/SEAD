import numpy as np


class Coeff:
    def __init__(self):
        self.url = 'https://customer-janes-com.tudelft.idm.oclc.org/entityprofile/equipment/Equipment_12900/specifications?explorerState=7a3d6ad9-907d-4673-ab0d-8573805a660e&rootEntity=Equipment_12900'
        ###Fuselage
        self.f_l = 32.5  # fuselage length [m]
        self.wb = 14.01  # Wheelbase [m]
        self.wt = 5.04  # wheeltrack [m]
        self.dw = 3.69  # Nose wheel distance
        self.dwing = 14.25  # Distance nose Cr wing
        self.de = 22.4 #Distance front engine
        self.ln = 4.71

        ###Wing
        self.b = 28.08  # wingspan [m]
        self.A = 8.4  # Aspect ratio
        self.S = 93.50
        self.c = self.b / self.A
        self.cr = 5.28  # chord root length
        self.ct = 1.26  # chord tip length
        self.Labdaquart = 17.45
        self.LabdaLead = 21.2

        ##Tail
        self.b_ht = 10.04  # Tail span
        self.cr_ht = 3.095
        self.ct_ht = 1.45
        self.LabdaLeadH = 32
        self.b_vt = 3.550
        self.cr_vt = 4.57
        self.ct_vt = 3.21
        self.LabdaLeadV = 42
        self.Svt = 10  # fin area
        self.Sht = 17.76  # Tailplane area

        ###Control
        self.Sa = 3.53  # Aileron area [m^2]
        self.Sf = 17.08  # Flap area
        self.Ss = 3.62  # Spoiler area
        self.Sr = 2.30  # Rudder area
        self.Se = 3.96  # Elevator area

        ###Weights (tay620 engine) [kg]
        self.OEW = 24593
        self.MZFW = 35830  # Max zero fuel weight
        self.MRW = 43320  # Max ramp weight
        self.MTOW = 43090  # Max take of weight
        self.MLW = 38780  # Max landing weight
        self.MP = 11108  # Max payload

        ###Loading
        self.T = 61607 * 2  # Thrust N
        self.WS = self.MTOW / self.S  # Max wing loading = kg/m2
        self.WT = self.MTOW / self.T  # Thrust loading = kg/N

        ##Cargo
        self.maxc = 900  # kg virgin australia
        self.massp = self.MP - self.maxc
        self.holdf = 9.5  # volumes hold m3
        self.holda = 7.2
        self.cargof = self.maxc * self.holdf / (self.holdf + self.holda)
        self.cargoa = self.maxc * self.holda / (self.holdf + self.holda)

    @property
    def MAC(self):
        t = self.ct / self.cr  # taper ratio
        return self.cr * 2 / 3 * ((1 + t + t ** 2) / (1 + t))

    @property
    def MACy(self):
        return self.b * (self.MAC - self.cr) / (2 * (self.ct - self.cr))

    @property
    def LEMAC(self):
        nose_to_LECR = 14.25
        return nose_to_LECR + np.tan(np.radians(self.LabdaLead)) * self.MACy

    @property
    def MACH(self):
        t = self.ct_ht / self.cr_ht  # taper ratio
        return self.cr_ht * 2 / 3 * ((1 + t + t ** 2) / (1 + t))

    @property
    def MACyH(self):
        return self.b_ht * (self.MACH - self.cr_ht) / (2 * (self.ct_ht - self.cr_ht))

    @property
    def LEMACH(self):
        nose_to_LECRH = 31.8
        return nose_to_LECRH + np.tan(np.radians(self.LabdaLeadH)) * self.MACyH

    @property
    def MACV(self):
        t = self.ct_vt / self.cr_vt  # taper ratio
        return self.cr_vt * 2 / 3 * ((1 + t + t ** 2) / (1 + t))

    @property
    def MACyV(self):
        return self.b_vt * (self.MACV - self.cr_vt) / (2 * (self.ct_vt - self.cr_vt))

    @property
    def LEMACV(self):
        nose_to_LECRV = 27.82
        return nose_to_LECRV + np.tan(np.radians(self.LabdaLeadV)) * self.MACyV
