import numpy as np
import matplotlib.pyplot as plt

class Coeff:
    def __init__(self):
        self.url = 'https://customer-janes-com.tudelft.idm.oclc.org/entityprofile/equipment/Equipment_12900/specifications?explorerState=7a3d6ad9-907d-4673-ab0d-8573805a660e&rootEntity=Equipment_12900'
        ###Fuselage
        self.f_l = 32.5  # fuselage length [m]
        self.b_f = np.nan  # fuselage width [m]
        self.h_f = np.nan # fuselage height [m]
        self.wb = 14.01  # Wheelbase [m]
        self.wt = 5.04  # wheeltrack [m]
        self.dw = 3.75  # Nose wheel distance
        self.dwing = 14.25  # Distance nose Cr wing
        self.de = 21.9  # Distance front engine
        self.ln = 4.71  # length nacelle
        self.b_n = np.nan # nacelle width

        ###Wing
        self.b = 28.08  # wingspan [m]
        self.A = 8.4  # Aspect ratio
        self.S = 93.50 # wing area [m^2]
        self.Snet = np.nan # net area of the wing
        self.c = self.b / self.A
        self.cr = 5.28  # chord root length
        self.ct = 1.26  # chord tip length
        self.taper = self.ct / self.cr # taper ratio
        self.LabdaLead = 20.2 # Leading edge sweep angle
        self.l_fn = np.nan # nose to start wing length

        ##Tail
        self.b_ht = 10.04  # Tail span
        self.cr_ht = 3.14 # Horizontal Tail chord root
        self.ct_ht = 1.26 # Horizontal Tail chord tip
        self.LabdaLeadH = 31.3 # Horizontal tail Leading edge sweep angle
        self.b_vt = 3.75 # Vertical Tail span
        self.cr_vt = 4.25   # Vertical Tail chord root
        self.ct_vt = 3.32   # Vertical Tail chord tip
        self.LabdaLeadV = 42.1 # Vertical tail Leading edge sweep angle
        self.Svt = 10  # vertical fin area
        self.Sht = 17.76  # Horizontal Tailplane area
        self.l_h = np.nan  # length from tail to wing

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
        nose_to_LECR = 13.7
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
        nose_to_LECRH = 31.3
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
        nose_to_LECRV = 27.8
        return nose_to_LECRV + np.tan(np.radians(self.LabdaLeadV)) * self.MACyV

    def sweep(self, percentage):
        if percentage > 1 or percentage < 0:
            raise ValueError("Percentage should be between 0 and 1")
        start_tip = np.tan(np.radians(self.LabdaLead)) * self.b/2
        root = self.cr * percentage
        tip = self.ct * percentage + start_tip
        return np.arctan((tip-root)/(self.b/2))

    def sweepH(self, percentage):
        if percentage > 1 or percentage < 0:
            raise ValueError("Percentage should be between 0 and 1")
        start_tip = np.tan(np.radians(self.LabdaLeadH)) * self.b_ht/2
        root = self.cr_ht * percentage
        tip = self.ct_ht * percentage + start_tip
        return np.arctan((tip-root)/(self.b_ht/2))


    def sweepV(self, percentage):
        if percentage > 1 or percentage < 0:
            raise ValueError("Percentage should be between 0 and 1")
        start_tip = np.tan(np.radians(self.LabdaLeadV)) * self.b_vt/2
        root = self.cr_vt * percentage
        tip = self.ct_vt * percentage + start_tip
        return np.arctan((tip-root)/(self.b_vt/2))

    def x_ac(self,wing_contribution_c, C_L_alpha_Ah):
        """Aerodynamic center of the aircraft less tail obtained from AE3211 lecture 6
        :param wing_contribution_c: Wing contribution to the aerodynamic center
        :param C_L_alpha_Ah: Lift rate coefficient of the aircraft less tail
        :param b: wingspan
        :param b_f: fuselage width
        :param b_n: nacelle width
        :param h_f: fuselage height
        :param l_fn: nose to start wing length
        :param l_n: nacelle length
        :param S: wing area
        :param c: Mean aerodynamic chord
        :param taper: taper ratio
        :param sweep25: 25% sweep angle in radians"""
        b = self.b
        b_f = self.b_f
        b_n = self.b_n
        h_f = self.h_f
        l_fn = self.l_fn
        l_n = self.ln
        S = self.S
        c = self.MAC
        taper = self.taper
        sweep25 = self.sweep(0.25)

        c_g = S / b  # Mean geometric chord
        fuselage_contribution1_c = -(1.8 / C_L_alpha_Ah) * (b_f * h_f * l_fn) / (S * c)
        fuselage_contribution2_c = (0.25 / (1 + taper)) * (b_f * c_g * (b - b_f)) / (c * c * (b + 2.15 * b_f)) * np.tan(
            sweep25)
        nacelles_contribution_c = 2 * -2.5 * b_n * b_n * l_n / (S * c * C_L_alpha_Ah)
        return (wing_contribution_c + fuselage_contribution1_c + fuselage_contribution2_c + nacelles_contribution_c) * c

    def c_m_ac(self):
        raise NotImplementedError("This method is not implemented yet")

    def C_L_alpha_h(self,M):
        """Lift rate coefficient of the horizontal tail obtained from AE3211 lecture 6
        :param M: Mach number
        :param A_h: Aspect ratio of the horizontal tail
        :param sweep50h: 50% sweep angle of the horizontal tail in radians"""
        A_h = self.Sht
        sweep50h = self.sweepH(0.5)

        beta = np.sqrt(1 - M * M)
        result = 2 * np.pi * A_h / (2 + np.sqrt(4 + (A_h * beta / 0.95) ** 2) * (1 + (np.tan(sweep50h) / beta) ** 2))
        if np.isnan(result):
            raise ValueError("Not all values are defined")
        return result

    def C_L_alpha_Ah(self,C_L_alpha_w):
        """Lift rate coefficient of the aircraft less tail obtained from AE3211 lecture 6
        :param C_L_alpha_w: Lift rate coefficient of the wing
        :param b: wingspan
        :param b_f: fuselage width
        :param S: wing area
        :param S_net: net area of the wing"""
        b = self.b
        b_f = self.b_f
        S = self.S
        S_net = self.Snet

        result = C_L_alpha_w * (1 + 2.15 * (b_f / b)) * (S_net / S) + (np.pi * b_f ** 2) / (S * 2)
        if np.isnan(result):
            raise ValueError("Not all values are defined")
        return result

    def de_dalpha(self, sweep25, m_tv, C_L_alpha_w):
        """downwash effect of the wing on the tail obtained from AE3211 lecture 6
        :param sweep25: 25% sweep angle of the wing in radians
        :param l_h: length from tail to wing
        :param b: wingspan
        :param m_tv: m_tv*b/2 = Distance between the horizontal tail and the vortex shed plane, which can be approximated with the plane from the wing root chord
        :param C_L_alpha_w: Lift rate coefficient of the wing
        :param A: Aspect ratio of the wing
        """
        l_h = self.l_h
        b = self.b
        A = self.A

        r = l_h / (b / 2)
        Kel = ((0.1124 + 0.1265 * sweep25 + 0.1766 * sweep25 ** 2) / (r ** 2)) + (0.1024 / r) + 2
        Kel0 = (0.1124 / (r ** 2)) + (0.1024 / r) + 2
        deda = Kel / Kel0 * ((r / (r ** 2 + m_tv ** 2)) * (0.4876 / np.sqrt(r ** 2 + 0.6319 + m_tv ** 2)) +
                             (1 + ((r ** 2) / (r ** 2) + 0.7915 + 5.0734 * m_tv ** 2) ** 0.3113) * (
                                         1 - np.sqrt((m_tv ** 2) / (1 + m_tv ** 2)))
                             * (C_L_alpha_w / (np.pi * A)))
        if np.isnan(deda):
            raise ValueError("Not all values are defined")
        return deda

    def Vh_V_square(self):
        """Tail wing speed ratio obtained from AE3211 lecture 6"""
        return 1

    def C_L_alpha_w(self, M, eta=0.95):
        """Lift rate coefficient of the wing obtained from AE2111 - II course aircraft lecture 2
        :param M: Mach number
        :param A: Aspect ratio of the wing
        :param sweep25: 25% sweep angle of the wing in radians"""
        A = self.A
        sweep25 = self.sweep(0.25)
        beta = np.sqrt(1 - M * M)
        result = 2 * np.pi * A / (2 + np.sqrt(4 + ((A * beta / eta) ** 2) * (1 + (np.tan(sweep25) / beta) ** 2)))
        if np.isnan(result):
            raise ValueError("Not all values are defined")
        return result

if __name__ == "__main__":
    Fokker = Coeff()
    percentage = 0.0
    sweep_angle = Fokker.sweep(percentage)
    print(np.degrees(sweep_angle))
    plt.plot([0, Fokker.b/2, Fokker.b/2,0,0],[0, -Fokker.b/2 * np.tan(np.radians(Fokker.LabdaLead)), -Fokker.b/2 * np.tan(np.radians(Fokker.LabdaLead))-Fokker.ct,-Fokker.cr,0],label='Wing outline')
    plt.plot([0,Fokker.b/2], [-percentage * Fokker.cr, -percentage * Fokker.cr - np.tan(sweep_angle) * Fokker.b / 2], "-.", label=f'{percentage * 100}% sweep')
    plt.vlines(Fokker.MACy,-Fokker.LEMAC+13.7,-Fokker.LEMAC+13.7-Fokker.MAC,'k',label='MAC')
    plt.legend()
    plt.show()