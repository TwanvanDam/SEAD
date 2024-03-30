import numpy as np

def x_ac(wing_contribution_c,C_L_alpha_Ah,b, b_f, b_n, h_f, l_fn, l_n, S, c, taper, sweep25):
    """Aerodynamic center of the aircraft less tail
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
    :param sweep25: 25% sweep angle"""
    c_g = S/b # Mean geometric chord
    fuselage_contribution1_c = -(1.8/C_L_alpha_Ah) * (b_f * h_f * l_fn) / (S * c)
    fuselage_contribution2_c = (0.25/(1+ taper)) * (b_f*c_g*(b-b_f)) / (c*c * (b + 2.15*b_f)) * np.tan(np.radians(sweep25))
    nacelles_contribution_c =  2* -2.5 * b_n * b_n * l_n / (S * c * C_L_alpha_Ah)
    return (wing_contribution_c + fuselage_contribution1_c + fuselage_contribution2_c + nacelles_contribution_c)*c

def C_L_alpha_h(M, A_h, sweep50h):
    """Lift rate coefficient of the horizontal tail
    :param M: Mach number
    :param A_h: Aspect ratio of the horizontal tail
    :param sweep50h: 50% sweep angle of the horizontal tail"""
    beta = np.sqrt(1-M*M)
    return 2*np.pi* A_h / (2 + np.sqrt(4 + (A_h*beta/0.95)**2) * (1 + (np.tan(np.radians(sweep50h))/beta)**2))

def C_L_alpha_Ah(C_L_alpha_w,b, b_f, S,S_net):
    """Lift rate coefficient of the aircraft less tail
    :param C_L_alpha_w: Lift rate coefficient of the wing
    :param b: wingspan
    :param b_f: fuselage width
    :param S: wing area
    :param S_net: net area of the wing"""
    return C_L_alpha_w*(1+2.15*(b_f/b))*(S_net/S) + (np.pi * b_f ** 2) / (S*2)

def de_dalpha(sweep25, l_h, b, m_tv, C_L_alpha_w, A):
    """downwash effect of the wing on the tail
    :param sweep25: 25% sweep angle of the wing
    :param l_h: length from tail to wing
    :param b: wingspan
    :param m_tv: m_tv*b/2 = Distance between the horizontal tail and the vortex shed plane, which can be approximated with the plane from the wing root chord
    :param C_L_alpha_w: Lift rate coefficient of the wing
    :param A: Aspect ratio of the wing
    """

    r = l_h / (b/2)
    Kel = ((0.1124 + 0.1265 * np.radians(sweep25) + 0.1766 * np.radians(sweep25) ** 2) / (r**2)) +( 0.1024 / r) + 2
    Kel0 = (0.1124 / (r**2)) + (0.1024 / r) + 2
    deda = Kel/Kel0 * ( (r/(r**2 + m_tv**2)) *(0.4876 / np.sqrt(r**2 + 0.6319 + m_tv**2)) +
                        (1 + ((r**2)/(r**2) + 0.7915 + 5.0734* m_tv**2)**0.3113)* (1-np.sqrt((m_tv**2)/(1+m_tv**2)))
                        * (C_L_alpha_w/(np.pi*A)) )
    return deda

def Vh_V_square():
    """Tail wing speed ratio"""
    return 1


