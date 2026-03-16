#!/usr/bin/env python3
"""
COMPLETE NUCLEOSYNTHESIS LOGIC TREE — H through Ni
All elements Z=0(n) through Z=28(Ni), all major isotopes,
all fusion/capture/decay pathways including improbable ones.
"""

import math

# ===================================================================
# ATOMIC MASSES (AMU) — AME2020
# Complete: n through Ni-62, all nucleosynthetically relevant isotopes
# ===================================================================
M = {
    # Z=0
    "n":      1.0086649,
    # Z=1
    "p":      1.0078250, "D":      2.0141018, "H-3":    3.0160493,
    # Z=2
    "He-3":   3.0160293, "He-4":   4.0026033,
    # Z=3
    "Li-6":   6.0151228, "Li-7":   7.0160034,
    # Z=4
    "Be-7":   7.0169292, "Be-8":   8.0053051, "Be-9":   9.0121831,
    # Z=5
    "B-8":    8.0246073, "B-10":  10.0129370, "B-11":  11.0093054,
    # Z=6
    "C-12":  12.0000000, "C-13":  13.0033548, "C-14":  14.0032420,
    # Z=7
    "N-13":  13.0057386, "N-14":  14.0030740, "N-15":  15.0001089,
    # Z=8
    "O-15":  15.0030656, "O-16":  15.9949146, "O-17":  16.9991317, "O-18":  17.9991610,
    # Z=9
    "F-17":  17.0020952, "F-18":  18.0009380, "F-19":  18.9984032,
    # Z=10
    "Ne-20": 19.9924402, "Ne-21": 20.9938853, "Ne-22": 21.9913851,
    # Z=11
    "Na-22": 21.9944364, "Na-23": 22.9897693,
    # Z=12
    "Mg-23": 22.9941249, "Mg-24": 23.9850417, "Mg-25": 24.9858370, "Mg-26": 25.9825930,
    # Z=13
    "Al-26": 25.9868917, "Al-27": 26.9815386,
    # Z=14
    "Si-28": 27.9769265, "Si-29": 28.9764947, "Si-30": 29.9737702,
    # Z=15
    "P-30":  29.9783138, "P-31":  30.9737615,
    # Z=16
    "S-32":  31.9720707, "S-33":  32.9714585, "S-34":  33.9678670,
    # Z=17
    "Cl-35": 34.9688527, "Cl-36": 35.9683069, "Cl-37": 36.9659026,
    # Z=18
    "Ar-36": 35.9675463, "Ar-37": 36.9667759, "Ar-38": 37.9627324, "Ar-39": 38.9643130, "Ar-40": 39.9623831,
    # Z=19
    "K-39":  38.9637069, "K-40":  39.9639982, "K-41":  40.9618260,
    # Z=20
    "Ca-40": 39.9625909, "Ca-41": 40.9622783, "Ca-42": 41.9586180, "Ca-43": 42.9587666, "Ca-44": 43.9554811,
    "Ca-48": 47.9525340,
    # Z=21
    "Sc-45": 44.9559119,
    # Z=22
    "Ti-44": 43.9596901, "Ti-46": 45.9526316, "Ti-47": 46.9517631, "Ti-48": 47.9479463,
    # Z=23
    "V-50":  49.9471585, "V-51":  50.9439595,
    # Z=24
    "Cr-48": 47.9540291, "Cr-50": 49.9460442, "Cr-52": 51.9405075, "Cr-53": 52.9406494,
    "Cr-54": 53.9388804,
    # Z=25
    "Mn-52": 51.9455655, "Mn-55": 54.9380451,
    # Z=26
    "Fe-52": 51.9481131, "Fe-54": 53.9396105, "Fe-56": 55.9349375, "Fe-57": 56.9353940,
    "Fe-58": 57.9332756,
    # Z=27
    "Co-56": 55.9398393, "Co-59": 58.9331950,
    # Z=28
    "Ni-56": 55.9421320, "Ni-58": 57.9353429, "Ni-59": 58.9343467, "Ni-60": 59.9307864, "Ni-61": 60.9310560,
    "Ni-62": 61.9283451,
}

# (A, Z) lookup
AZ = {
    "n":(1,0),
    "p":(1,1),"D":(2,1),"H-3":(3,1),
    "He-3":(3,2),"He-4":(4,2),
    "Li-6":(6,3),"Li-7":(7,3),
    "Be-7":(7,4),"Be-8":(8,4),"Be-9":(9,4),
    "B-8":(8,5),"B-10":(10,5),"B-11":(11,5),
    "C-12":(12,6),"C-13":(13,6),"C-14":(14,6),
    "N-13":(13,7),"N-14":(14,7),"N-15":(15,7),
    "O-15":(15,8),"O-16":(16,8),"O-17":(17,8),"O-18":(18,8),
    "F-17":(17,9),"F-18":(18,9),"F-19":(19,9),
    "Ne-20":(20,10),"Ne-21":(21,10),"Ne-22":(22,10),
    "Na-22":(22,11),"Na-23":(23,11),
    "Mg-23":(23,12),"Mg-24":(24,12),"Mg-25":(25,12),"Mg-26":(26,12),
    "Al-26":(26,13),"Al-27":(27,13),
    "Si-28":(28,14),"Si-29":(29,14),"Si-30":(30,14),
    "P-30":(30,15),"P-31":(31,15),
    "S-32":(32,16),"S-33":(33,16),"S-34":(34,16),
    "Cl-35":(35,17),"Cl-36":(36,17),"Cl-37":(37,17),
    "Ar-36":(36,18),"Ar-37":(37,18),"Ar-38":(38,18),"Ar-39":(39,18),"Ar-40":(40,18),
    "K-39":(39,19),"K-40":(40,19),"K-41":(41,19),
    "Ca-40":(40,20),"Ca-41":(41,20),"Ca-42":(42,20),"Ca-43":(43,20),"Ca-44":(44,20),"Ca-48":(48,20),
    "Sc-45":(45,21),
    "Ti-44":(44,22),"Ti-46":(46,22),"Ti-47":(47,22),"Ti-48":(48,22),
    "V-50":(50,23),"V-51":(51,23),
    "Cr-48":(48,24),"Cr-50":(50,24),"Cr-52":(52,24),"Cr-53":(53,24),"Cr-54":(54,24),
    "Mn-52":(52,25),"Mn-55":(55,25),
    "Fe-52":(52,26),"Fe-54":(54,26),"Fe-56":(56,26),"Fe-57":(57,26),"Fe-58":(58,26),
    "Co-56":(56,27),"Co-59":(59,27),
    "Ni-56":(56,28),"Ni-58":(58,28),"Ni-59":(59,28),"Ni-60":(60,28),"Ni-61":(61,28),"Ni-62":(62,28),
    "γ":(0,0),"e⁻":(0,-1),"ν_e":(0,0),"e⁺":(0,1),
}

MASSLESS = {"γ","ν_e"}
LEPTON = {"e⁻":0.000549,"e⁺":0.000549}

def Q(r, p):
    def gm(x):
        if x in MASSLESS: return 0.0
        if x in LEPTON: return LEPTON[x]
        return M[x]
    return (sum(gm(x) for x in r) - sum(gm(x) for x in p)) * 931.494

def chk(r, p):
    Ar=sum(AZ[x][0] for x in r); Zr=sum(AZ[x][1] for x in r)
    Ap=sum(AZ[x][0] for x in p); Zp=sum(AZ[x][1] for x in p)
    return (Ar==Ap and Zr==Zp), Ar, Zr, Ap, Zp

# ===================================================================
# TIME-TEMPERATURE (calibrated)
# ===================================================================
_alpha = math.log(2) / math.log(5)
_A = 0.8e9 * (100.0 ** _alpha)

def T_of_t(t):
    if t <= 1.0: return 10.4e9 / math.sqrt(t)
    elif t <= 10.0:
        f = math.log(t) / math.log(10.0)
        return (10.4e9/math.sqrt(t))*(1-f) + (_A*t**(-_alpha))*f
    else: return _A * t**(-_alpha)

def T9(t): return T_of_t(t)/1e9
def rho_b(t9): return 1.1e-4 * 6.1 * t9**3

# ===================================================================
# COMPLETE REACTION DATABASE
# ===================================================================
# Every reaction: [id, reactants, products, generation, probability, note]

R = [
    # ═══ GEN 0: FREEZE-OUT ═══
    # (no reactions, just n/p ratio setting)

    # ═══ GEN 1: DEUTERIUM ═══
    ["1.1", ["p","n"], ["D","γ"], 1, "dominant",
     "Gateway reaction; Q=2.225 MeV"],

    # ═══ GEN 2: MASS-3 ═══
    ["2.1", ["D","D"], ["He-3","n"], 2, "dominant", "~50% of D+D"],
    ["2.2", ["D","D"], ["H-3","p"], 2, "dominant", "~50% of D+D"],
    ["2.3", ["D","p"], ["He-3","γ"], 2, "significant", "radiative proton capture"],
    ["2.4", ["D","n"], ["H-3","γ"], 2, "moderate", "radiative neutron capture"],

    # ═══ GEN 3: He-4 ═══
    ["3.1", ["H-3","D"], ["He-4","n"], 3, "dominant", "fastest He-4 path"],
    ["3.2", ["He-3","D"], ["He-4","p"], 3, "dominant", "complementary path"],
    ["3.3", ["He-3","He-3"], ["He-4","p","p"], 3, "significant", "pp-chain branch"],
    ["3.4", ["H-3","H-3"], ["He-4","n","n"], 3, "rare", "neutron-rich"],
    ["3.5", ["He-3","n"], ["H-3","p"], 3, "significant", "charge exchange"],
    ["3.6", ["H-3","p"], ["He-3","n"], 3, "significant", "reverse charge exchange"],

    # ═══ GEN 4: Li, Be (A=6-9) ═══
    ["4.1", ["He-4","D"], ["Li-6","γ"], 4, "rare", "Li-6 production"],
    ["4.2", ["He-4","H-3"], ["Li-7","γ"], 4, "moderate", "direct Li-7"],
    ["4.3", ["He-4","He-3"], ["Be-7","γ"], 4, "moderate", "Be-7 → Li-7 later"],
    ["4.4", ["Be-7","e⁻"], ["Li-7","ν_e"], 4, "certain", "EC; t½≈53d"],
    ["4.5", ["Be-7","n"], ["Li-7","p"], 4, "significant", "destroys Be-7"],
    ["4.6", ["Li-6","p"], ["He-4","He-3"], 4, "dominant", "DESTROYS Li-6"],
    ["4.7", ["Li-7","p"], ["He-4","He-4"], 4, "significant", "DESTROYS Li-7"],
    ["4.8", ["Li-6","n"], ["Li-7","γ"], 4, "rare", "n-capture on Li-6"],
    ["4.9", ["Li-7","n"], ["Li-7","n"], 4, "negligible", "elastic only; Li-8 unbound"],
    ["4.10", ["He-4","He-4"], ["Be-8"], 4, "unstable",
     "Be-8 lives ~6×10⁻¹⁷ s; decays back to 2 He-4"],
    ["4.11", ["Be-7","D"], ["Be-9","e⁺","ν_e"], 4, "negligible",
     "extremely rare; would need weak interaction"],

    # Be-9 paths (if it existed in abundance)
    ["4.12", ["Li-7","D"], ["Be-9","γ"], 4, "rare",
     "Be-9 production; tiny at BBN densities"],
    ["4.13", ["Be-9","p"], ["Li-6","He-4"], 4, "significant",
     "destroys Be-9 if any forms"],
    ["4.14", ["Be-9","p"], ["B-10","γ"], 4, "rare",
     "proton capture to boron"],
    ["4.15", ["Be-9","He-4"], ["C-12","n"], 4, "moderate",
     "alpha on Be-9; alternative to triple-alpha"],

    # Boron
    ["4.16", ["B-10","n"], ["Li-7","He-4"], 4, "dominant",
     "destroys B-10"],
    ["4.17", ["B-11","p"], ["He-4","He-4","He-4"], 4, "dominant",
     "destroys B-11 → 3 alphas"],
    ["4.18", ["B-10","p"], ["Be-7","He-4"], 4, "moderate",
     "p on B-10 → Be-7 + alpha"],
    ["4.19", ["Be-9","D"], ["B-10","n"], 4, "rare", "d-capture on Be-9"],
    ["4.20", ["B-10","He-4"], ["N-14","γ"], 4, "rare",
     "alpha capture; seed for CNO if it happened"],
    ["4.21", ["B-11","He-4"], ["N-14","n"], 4, "rare",
     "alpha on B-11"],

    # ═══ GEN 5: MASS-5/8 GAP + TRIPLE ALPHA ═══
    ["5.1", ["He-4","He-4","He-4"], ["C-12","γ"], 5, "impossible_BBN",
     "Hoyle resonance; needs ρ>10⁵ g/cm³"],
    ["5.2", ["He-4","He-4","He-4"], ["C-12","γ"], 5, "locked_pocket",
     "IF 28 MeV jolt creates transient ρ~10⁶"],
    ["5.3", ["Be-9","He-4"], ["C-12","n"], 5, "rare",
     "bypasses triple-alpha IF Be-9 exists"],

    # ═══ GEN 6: C-12, C-13, C-14 + CNO CYCLE ═══
    # Alpha captures
    ["6.1", ["C-12","He-4"], ["O-16","γ"], 6, "stellar",
     "critical 12C(α,γ)16O rate"],
    ["6.2", ["C-13","He-4"], ["O-16","n"], 6, "stellar",
     "neutron source for s-process"],

    # Proton captures (CNO-I)
    ["6.3", ["C-12","p"], ["N-13","γ"], 6, "stellar", "CNO-I step 1"],
    ["6.4", ["N-14","p"], ["O-15","γ"], 6, "stellar",
     "CNO bottleneck; slowest step. O-15 then β⁺ decays to N-15"],
    ["6.5", ["C-13","p"], ["N-14","γ"], 6, "stellar", "CNO-I step 3"],
    ["6.6", ["N-15","He-4"], ["F-19","γ"], 6, "stellar",
     "alpha capture on N-15; fluorine production path"],
    ["6.7", ["C-12","He-4"], ["O-16","γ"], 6, "stellar",
     "duplicate of 6.1; listed for CNO context — C made by CNO returns to He-burning"],
    ["6.8", ["N-15","p"], ["C-12","He-4"], 6, "stellar",
     "CNO-I completes; returns C-12 catalyst"],
    ["6.9", ["N-15","p"], ["O-16","γ"], 6, "stellar",
     "~0.1% branch; leaks into CNO-II"],

    # Neutron captures on C
    ["6.10", ["C-12","n"], ["C-13","γ"], 6, "stellar",
     "n-capture; builds C-13"],
    ["6.11", ["C-13","n"], ["C-14","γ"], 6, "stellar",
     "n-capture; C-14 is long-lived (t½=5730yr)"],
    ["6.12", ["C-14","n"], ["C-14","n"], 6, "negligible",
     "C-15 unbound; elastic only"],

    # D captures on C
    ["6.13", ["C-12","D"], ["N-14","γ"], 6, "stellar",
     "deuteron capture"],
    ["6.14", ["C-13","D"], ["N-14","n"], 6, "stellar",
     "deuteron capture + neutron out"],

    # ═══ GEN 7: OXYGEN ISOTOPES ═══
    ["7.1", ["O-16","He-4"], ["Ne-20","γ"], 7, "stellar",
     "alpha capture chain"],
    ["7.2", ["O-16","p"], ["F-17","γ"], 7, "stellar",
     "p-capture; F-17 β⁺ decays to O-17 (t½=65s)"],
    ["7.3", ["O-16","n"], ["O-17","γ"], 7, "stellar", "n-capture"],
    ["7.4", ["O-17","n"], ["O-18","γ"], 7, "stellar", "n-capture chain"],
    ["7.5", ["O-17","p"], ["N-14","He-4"], 7, "stellar",
     "CNO-II branch"],
    ["7.6", ["O-17","He-4"], ["Ne-20","n"], 7, "stellar",
     "alpha + neutron out"],
    ["7.7", ["O-18","p"], ["F-19","γ"], 7, "stellar", "p-capture"],
    ["7.8", ["O-18","He-4"], ["Ne-22","γ"], 7, "stellar",
     "important for Ne-22; s-process neutron source later"],
    ["7.9", ["O-18","p"], ["N-15","He-4"], 7, "stellar",
     "CNO-III branch completion"],

    # ═══ GEN 8: FLUORINE ═══
    ["8.1", ["F-18","p"], ["O-15","He-4"], 8, "stellar",
     "F-18(p,α)O-15; competes with F-18 β⁺ decay (t½=110min)"],
    ["8.2", ["F-19","p"], ["O-16","He-4"], 8, "stellar",
     "destroys F-19; why fluorine is rare"],
    ["8.3", ["F-19","He-4"], ["Ne-22","p"], 8, "stellar",
     "alpha on fluorine"],
    ["8.4", ["F-19","n"], ["F-19","n"], 8, "negligible",
     "F-20 very short-lived"],

    # ═══ GEN 9: NEON ISOTOPES ═══
    ["9.1", ["Ne-20","He-4"], ["Mg-24","γ"], 9, "stellar",
     "alpha capture"],
    ["9.2", ["Ne-20","n"], ["Ne-21","γ"], 9, "stellar", "n-capture"],
    ["9.3", ["Ne-21","n"], ["Ne-22","γ"], 9, "stellar", "n-capture chain"],
    ["9.4", ["Ne-22","He-4"], ["Mg-26","γ"], 9, "stellar",
     "bypasses Mg-24,25"],
    ["9.5", ["Ne-22","He-4"], ["Mg-25","n"], 9, "stellar",
     "important s-process neutron source: ²²Ne(α,n)²⁵Mg"],
    ["9.6", ["Ne-20","p"], ["F-17","He-4"], 9, "rare",
     "Ne-20(p,α)F-17; F-17 β⁺ decays to O-17"],
    # Neon burning (photodisintegration)
    ["9.7", ["Ne-20","γ"], ["O-16","He-4"], 9, "stellar",
     "NEON BURNING: photodisintegration at T>1.2×10⁹ K"],
    ["9.8", ["Ne-20","He-4"], ["Mg-24","γ"], 9, "stellar",
     "released α recaptured; net: 2 Ne-20 → O-16 + Mg-24"],

    # ═══ GEN 10: SODIUM ═══
    ["10.1", ["Ne-22","p"], ["Na-23","γ"], 10, "stellar", "p-capture"],
    ["10.2", ["Ne-21","p"], ["Na-22","γ"], 10, "stellar", "p-capture"],
    ["10.3", ["Na-22","n"], ["Na-23","γ"], 10, "stellar", "n-capture"],
    ["10.4", ["Na-23","p"], ["Mg-24","γ"], 10, "stellar",
     "NeNa cycle completion"],
    ["10.5", ["Na-23","p"], ["Ne-20","He-4"], 10, "stellar",
     "alternate; returns Ne-20"],
    ["10.6", ["Na-23","He-4"], ["Al-27","γ"], 10, "stellar",
     "alpha capture"],

    # ═══ GEN 11: CARBON BURNING ═══
    ["11.1", ["C-12","C-12"], ["Ne-20","He-4"], 11, "stellar",
     "~44% branch — dominant"],
    ["11.2", ["C-12","C-12"], ["Na-23","p"], 11, "stellar",
     "~56% branch — most common"],
    ["11.3", ["C-12","C-12"], ["Mg-24","γ"], 11, "stellar",
     "<1% radiative; NOT dominant"],
    ["11.4", ["C-12","C-12"], ["Mg-23","n"], 11, "negligible",
     "neutron channel; endothermic (~-2.6 MeV)"],

    # ═══ GEN 12: MAGNESIUM ISOTOPES ═══
    ["12.1", ["Mg-24","He-4"], ["Si-28","γ"], 12, "stellar",
     "alpha capture chain"],
    ["12.2", ["Mg-24","D"], ["Al-26","γ"], 12, "rare",
     "d-capture; ²⁶Al production path"],
    ["12.3", ["Mg-24","n"], ["Mg-25","γ"], 12, "stellar", "n-capture"],
    ["12.4", ["Mg-25","n"], ["Mg-26","γ"], 12, "stellar", "n-capture"],
    ["12.5", ["Mg-25","p"], ["Al-26","γ"], 12, "stellar",
     "²⁶Al production (t½=7.2×10⁵ yr; 1.809 MeV γ-line)"],
    ["12.6", ["Mg-26","p"], ["Al-27","γ"], 12, "stellar", "p-capture"],
    ["12.7", ["Mg-26","He-4"], ["Si-30","γ"], 12, "stellar",
     "alpha to Si-30"],
    ["12.8", ["Mg-26","n"], ["Mg-26","n"], 12, "negligible",
     "Mg-27 short-lived"],

    # ═══ GEN 13: ALUMINUM ═══
    ["13.1", ["Al-27","p"], ["Si-28","γ"], 13, "stellar",
     "MgAl cycle completion"],
    ["13.2", ["Al-27","He-4"], ["P-31","γ"], 13, "stellar",
     "alpha capture"],
    ["13.3", ["Al-27","n"], ["Al-27","n"], 13, "negligible",
     "Al-28 β⁻ decays rapidly"],
    ["13.4", ["Al-26","He-4"], ["P-30","γ"], 13, "rare",
     "alpha capture on ²⁶Al"],
    ["13.5", ["Al-26","n"], ["Al-27","γ"], 13, "stellar", "n-capture"],

    # ═══ GEN 14: SILICON ISOTOPES ═══
    ["14.1", ["Si-28","He-4"], ["S-32","γ"], 14, "stellar",
     "alpha capture chain"],
    ["14.2", ["Si-28","D"], ["P-30","γ"], 14, "rare",
     "d-capture on Si-28"],
    ["14.3", ["Si-28","n"], ["Si-29","γ"], 14, "stellar", "n-capture"],
    ["14.4", ["Si-29","n"], ["Si-30","γ"], 14, "stellar", "n-capture"],
    ["14.5", ["Si-29","p"], ["P-30","γ"], 14, "stellar", "p-capture"],
    ["14.6", ["Si-30","p"], ["P-31","γ"], 14, "stellar", "p-capture"],
    ["14.7", ["Si-30","He-4"], ["S-34","γ"], 14, "stellar",
     "alpha to S-34"],

    # ═══ GEN 15: OXYGEN BURNING ═══
    ["15.1", ["O-16","O-16"], ["Si-28","He-4"], 15, "stellar",
     "dominant O-burn channel"],
    ["15.2", ["O-16","O-16"], ["S-32","γ"], 15, "stellar",
     "radiative channel (minor)"],
    ["15.3", ["O-16","O-16"], ["P-31","p"], 15, "stellar",
     "proton channel"],
    ["15.4", ["O-16","O-16"], ["Mg-24","He-4","He-4"], 15, "stellar",
     "double-alpha channel; breakup products"],

    # ═══ GEN 16: PHOSPHORUS ═══
    ["16.1", ["P-31","p"], ["S-32","γ"], 16, "stellar", "p-capture"],
    ["16.2", ["P-31","He-4"], ["Cl-35","γ"], 16, "stellar",
     "alpha capture"],
    ["16.3", ["P-31","n"], ["P-31","n"], 16, "negligible",
     "P-32 β⁻ decays (t½=14d)"],
    ["16.4", ["P-30","n"], ["P-31","γ"], 16, "stellar",
     "n-capture; builds P-31 from radioactive P-30"],

    # ═══ GEN 17: SULFUR ═══
    ["17.1", ["S-32","He-4"], ["Ar-36","γ"], 17, "stellar",
     "alpha capture chain"],
    ["17.2", ["S-34","p"], ["Cl-35","γ"], 17, "stellar",
     "p-capture on S-34 → Cl-35"],
    ["17.3", ["S-32","n"], ["S-33","γ"], 17, "stellar", "n-capture"],
    ["17.4", ["S-33","n"], ["S-34","γ"], 17, "stellar", "n-capture"],
    ["17.5", ["S-34","He-4"], ["Ar-38","γ"], 17, "stellar",
     "alpha capture"],
    ["17.6", ["S-33","D"], ["Cl-35","γ"], 17, "rare",
     "d-capture on S-33"],

    # ═══ GEN 18: CHLORINE ═══
    ["18.1", ["Cl-35","p"], ["Ar-36","γ"], 18, "stellar", "p-capture"],
    ["18.2", ["Cl-35","He-4"], ["K-39","γ"], 18, "stellar",
     "alpha capture"],
    ["18.3", ["Cl-35","n"], ["Cl-36","γ"], 18, "stellar",
     "n-capture → Cl-36 (t½=3×10⁵ yr); then Cl-36+n→Cl-37"],
    ["18.4", ["Cl-37","p"], ["Ar-38","γ"], 18, "stellar", "p-capture"],
    ["18.5", ["Cl-37","He-4"], ["K-41","γ"], 18, "stellar",
     "alpha capture"],

    # ═══ GEN 19: ARGON ═══
    ["19.1", ["Ar-36","He-4"], ["Ca-40","γ"], 19, "stellar",
     "alpha capture chain — approaching iron peak"],
    ["19.2", ["Ar-36","n"], ["Ar-37","γ"], 19, "stellar",
     "n-capture → Ar-37 (EC, t½=35d); then Ar-37+n→Ar-38"],
    ["19.3", ["Ar-38","He-4"], ["Ca-42","γ"], 19, "stellar",
     "alpha capture"],
    ["19.4", ["Ar-38","n"], ["Ar-39","γ"], 19, "stellar",
     "n-capture → Ar-39 (β⁻, t½=269yr); then Ar-39+n→Ar-40"],
    ["19.5", ["Ar-38","p"], ["K-39","γ"], 19, "stellar",
     "p-capture on Ar-38 → K-39"],

    # ═══ GEN 20: POTASSIUM ═══
    ["20.1", ["K-39","p"], ["Ca-40","γ"], 20, "stellar", "p-capture"],
    ["20.2", ["K-41","He-4"], ["Sc-45","γ"], 20, "stellar",
     "alpha capture; Sc-45 production"],
    ["20.3", ["K-39","n"], ["K-40","γ"], 20, "stellar", "n-capture"],
    ["20.4", ["K-40","n"], ["K-41","γ"], 20, "stellar", "n-capture"],
    ["20.5", ["K-41","p"], ["Ca-42","γ"], 20, "stellar", "p-capture"],

    # ═══ GEN 21: CALCIUM ═══
    ["21.1", ["Ca-40","He-4"], ["Ti-44","γ"], 21, "stellar",
     "alpha capture; Ti-44 is key (t½=60yr, 44Ti line in SNR)"],
    ["21.2", ["Ca-44","p"], ["Sc-45","γ"], 21, "stellar",
     "p-capture; main Sc-45 production path"],
    ["21.3", ["Ca-40","n"], ["Ca-41","γ"], 21, "stellar",
     "n-capture → Ca-41 (EC, t½=10⁵yr); then Ca-41+n→Ca-42"],
    ["21.4", ["Ca-42","He-4"], ["Ti-46","γ"], 21, "stellar",
     "alpha capture"],
    ["21.5", ["Ca-44","He-4"], ["Ti-48","γ"], 21, "stellar",
     "alpha capture"],
    ["21.6", ["Ca-42","n"], ["Ca-43","γ"], 21, "stellar",
     "n-capture → Ca-43 (stable); then Ca-43+n→Ca-44"],

    # ═══ GEN 22: SCANDIUM ═══
    ["22.1", ["Sc-45","p"], ["Ti-46","γ"], 22, "stellar", "p-capture"],
    ["22.2", ["Sc-45","He-4"], ["Ti-48","p"], 22, "stellar",
     "Sc-45(α,p)Ti-48"],
    ["22.3", ["Sc-45","n"], ["Sc-45","n"], 22, "negligible",
     "Sc-46 β⁻ (t½=84d)"],
    ["22.4", ["Ca-44","p"], ["Sc-45","γ"], 22, "stellar",
     "how Sc-45 is made"],

    # ═══ GEN 23: TITANIUM ═══
    ["23.1", ["Ti-44","He-4"], ["Cr-48","γ"], 23, "stellar",
     "alpha capture → Cr-48"],
    ["23.2", ["Ti-46","He-4"], ["Cr-50","γ"], 23, "stellar",
     "alpha capture"],
    ["23.3", ["Ti-48","He-4"], ["Cr-52","γ"], 23, "stellar",
     "alpha capture → most abundant Cr"],
    ["23.4", ["Ti-48","D"], ["V-50","γ"], 23, "rare",
     "d-capture → V-50"],
    ["23.5", ["Ti-46","n"], ["Ti-47","γ"], 23, "stellar",
     "n-capture → Ti-47 (stable); then Ti-47+n→Ti-48"],
    ["23.6", ["Ti-48","n"], ["Ti-48","n"], 23, "negligible",
     "Ti-49,50 exist but rates marginal here"],

    # ═══ GEN 24: VANADIUM ═══
    ["24.1", ["V-51","p"], ["Cr-52","γ"], 24, "stellar", "p-capture"],
    ["24.2", ["V-51","He-4"], ["Mn-55","γ"], 24, "stellar",
     "alpha capture → Mn-55"],
    ["24.3", ["V-51","n"], ["V-51","n"], 24, "negligible",
     "V-52 β⁻ (t½=3.7min)"],
    ["24.4", ["V-50","n"], ["V-51","γ"], 24, "stellar", "n-capture"],
    ["24.5", ["V-50","D"], ["Cr-52","γ"], 24, "rare",
     "d-capture on V-50 → Cr-52"],

    # ═══ GEN 25: CHROMIUM ═══
    ["25.1", ["Cr-52","He-4"], ["Fe-56","γ"], 25, "stellar",
     "alpha capture → Fe-56 (most abundant isotope in universe)"],
    ["25.2", ["Cr-50","He-4"], ["Fe-54","γ"], 25, "stellar",
     "alpha capture"],
    ["25.3", ["Cr-52","n"], ["Cr-53","γ"], 25, "stellar",
     "n-capture → Cr-53 (stable); then Cr-53+n→Cr-54"],
    ["25.4", ["Cr-53","n"], ["Cr-54","γ"], 25, "stellar",
     "n-capture chain continues"],
    ["25.5", ["Cr-54","He-4"], ["Fe-58","γ"], 25, "stellar",
     "alpha capture"],
    ["25.6", ["Cr-48","He-4"], ["Fe-52","γ"], 25, "stellar",
     "alpha capture; Fe-52 β⁺ chain → Cr-52"],

    # ═══ GEN 26: MANGANESE ═══
    ["26.1", ["Mn-55","p"], ["Fe-56","γ"], 26, "stellar",
     "p-capture → Fe-56"],
    ["26.2", ["Mn-55","He-4"], ["Co-59","γ"], 26, "stellar",
     "alpha capture → only stable Co"],
    ["26.3", ["Mn-55","n"], ["Mn-55","n"], 26, "negligible",
     "Mn-56 β⁻ (t½=2.6hr)"],
    ["26.4", ["Mn-52","p"], ["Fe-52","n"], 26, "negligible",
     "Mn-52 β⁺ (t½=5.6d); rarer path"],

    # ═══ GEN 27: IRON ISOTOPES ═══
    ["27.1", ["Fe-54","He-4"], ["Ni-58","γ"], 27, "stellar",
     "alpha capture → Ni-58"],
    ["27.2", ["Fe-56","He-4"], ["Ni-60","γ"], 27, "stellar",
     "alpha capture → Ni-60"],
    ["27.3", ["Fe-56","p"], ["Co-56","n"], 27, "rare",
     "(p,n) reaction; Co-56 then EC→Fe-56"],
    ["27.4", ["Fe-54","D"], ["Co-56","γ"], 27, "rare",
     "d-capture → Co-56; Co-56 EC → Fe-56"],
    ["27.5", ["Fe-56","n"], ["Fe-57","γ"], 27, "stellar",
     "n-capture → Fe-57 (stable); then Fe-57+n→Fe-58"],
    ["27.6", ["Fe-58","He-4"], ["Ni-62","γ"], 27, "stellar",
     "alpha capture → Ni-62 (HIGHEST binding energy per nucleon)"],
    ["27.7", ["Fe-58","n"], ["Fe-58","n"], 27, "negligible",
     "Fe-59 β⁻ (t½=44d); s-process continues beyond Ni"],

    # ═══ GEN 28: COBALT ═══
    ["28.1", ["Co-59","p"], ["Ni-60","γ"], 28, "stellar",
     "p-capture"],
    ["28.2", ["Co-59","D"], ["Ni-60","n"], 28, "rare",
     "d-capture + n out"],
    ["28.3", ["Co-59","n"], ["Co-59","n"], 28, "negligible",
     "Co-60 β⁻ (t½=5.27yr)"],
    ["28.4", ["Co-56","e⁻"], ["Fe-56","ν_e"], 28, "certain",
     "Co-56 EC (t½=77d); from Ni-56→Co-56→Fe-56 chain"],

    # ═══ GEN 29: NICKEL — THE END ═══
    ["29.1", ["Ni-56","e⁻"], ["Co-56","ν_e"], 29, "certain",
     "Ni-56 EC (t½=6.1d) → Co-56 → Fe-56; powers SN light curves"],
    ["29.2", ["Ni-58","n"], ["Ni-59","γ"], 29, "stellar",
     "n-capture → Ni-59 (t½=7.6×10⁴yr); then Ni-59+n→Ni-60"],
    ["29.3", ["Ni-60","n"], ["Ni-61","γ"], 29, "stellar",
     "n-capture → Ni-61 (stable); then Ni-61+n→Ni-62"],
    ["29.4", ["Ni-62","n"], ["Ni-62","n"], 29, "negligible",
     "Ni-63 β⁻ (t½=100yr); s-process proceeds to Cu,Zn..."],

    # ═══ GEN 30: NSE / SILICON BURNING (not real fusion) ═══
    ["30.1", ["Si-28","Si-28"], ["Ni-56"], 30, "NOT_REAL",
     "DOES NOT HAPPEN. Coulomb Z=14+14 prohibitive. "
     "Real Si-burn is NSE: Si photodisintegrates into α,p,n "
     "which reassemble into iron-peak nuclei."],
]

# ===================================================================
# Probability symbols
# ===================================================================
SYM = {
    "dominant":"■■■■■", "significant":"■■■░░", "moderate":"■■░░░",
    "rare":"■░░░░", "certain":"■■■■■", "negligible":"░░░░░",
    "unstable":"■■■✗✗", "impossible_BBN":"✗✗✗✗✗",
    "locked_pocket":"??■??", "stellar":"☆☆☆☆☆",
    "NOT_REAL":"XXXXX",
}

# ===================================================================
# OUTPUT
# ===================================================================
W = 80
print("=" * W)
print("  COMPLETE NUCLEOSYNTHESIS LOGIC TREE")
print("  n → H → He → Li → Be → B → C → N → O → F → Ne → Na → Mg")
print("  → Al → Si → P → S → Cl → Ar → K → Ca → Sc → Ti → V")
print("  → Cr → Mn → Fe → Co → Ni")
print("  All isotopes. All pathways. Probable and impossible.")
print("=" * W)

# Calibration table
print(f"\n{'─'*W}")
print("  TIME-TEMPERATURE (calibrated to T(100)=0.8e9, T(500)=0.4e9 K)")
print(f"{'─'*W}")
for t in [1,10,50,100,180,200,300,500,1200]:
    t9=T9(t); rho=rho_b(t9)
    print(f"  t={t:>5.0f}s  T={t9:.3f}×10⁹ K  ρ_b={rho:.2e} g/cm³")

# Reactions
print(f"\n{'─'*W}")
print("  REACTION TREE")
print(f"{'─'*W}")

errors = 0
cur_gen = -1
gen_labels = {
    0:"FREE NUCLEONS", 1:"DEUTERIUM", 2:"MASS-3 (H-3,He-3)",
    3:"He-4", 4:"Li/Be/B (A=6-11)", 5:"TRIPLE ALPHA → C-12",
    6:"C ISOTOPES + CNO", 7:"O ISOTOPES", 8:"FLUORINE",
    9:"NEON + Ne BURNING", 10:"SODIUM", 11:"CARBON BURNING",
    12:"MAGNESIUM", 13:"ALUMINUM", 14:"SILICON ISOTOPES",
    15:"OXYGEN BURNING", 16:"PHOSPHORUS", 17:"SULFUR",
    18:"CHLORINE", 19:"ARGON", 20:"POTASSIUM", 21:"CALCIUM",
    22:"SCANDIUM", 23:"TITANIUM", 24:"VANADIUM", 25:"CHROMIUM",
    26:"MANGANESE", 27:"IRON", 28:"COBALT", 29:"NICKEL",
    30:"Si BURNING / NSE",
}

for rxn in R:
    rid, react, prod, gen, prob, note = rxn
    
    if gen != cur_gen:
        cur_gen = gen
        label = gen_labels.get(gen, f"GEN {gen}")
        print(f"\n  ╔══ GEN {gen}: {label} ══")

    q = Q(react, prod)
    ok, Ar, Zr, Ap, Zp = chk(react, prod)
    if not ok: errors += 1
    
    tag = "✓" if ok else "✗"
    sym = SYM.get(prob, "?????")
    r_str = " + ".join(react)
    p_str = " + ".join(prod)

    print(f"  ║ [{rid:>5s}] {r_str} → {p_str}")
    print(f"  ║         Q={q:+8.3f} MeV  A:{Ar}→{Ap} Z:{Zr}→{Zp} [{tag}]"
          f"  {sym}")
    if note:
        # Wrap long notes
        words = note.split()
        lines = []
        line = ""
        for w in words:
            if len(line) + len(w) + 1 > 60:
                lines.append(line)
                line = w
            else:
                line = f"{line} {w}" if line else w
        if line: lines.append(line)
        for ln in lines:
            print(f"  ║         {ln}")

# Summary
print(f"\n{'═'*W}")
print(f"  AUDIT")
print(f"{'═'*W}")
print(f"  Total reactions: {len(R)}")
print(f"  Conservation errors: {errors}")
print(f"  Isotopes in mass table: {len(M)}")
print(f"  Elements covered: Z=0(n) through Z=28(Ni)")

# Count unique species
species = set()
for rxn in R:
    for x in rxn[1]+rxn[2]:
        if x not in ("γ","e⁻","e⁺","ν_e"):
            species.add(x)
print(f"  Unique nuclear species in reactions: {len(species)}")

# List all species by Z
print(f"\n{'─'*W}")
print("  ISOTOPE INVENTORY")
print(f"{'─'*W}")
by_z = {}
for s in species:
    if s in AZ:
        z = AZ[s][1]
        by_z.setdefault(z, []).append(s)

elem_names = {
    0:"n",1:"H",2:"He",3:"Li",4:"Be",5:"B",6:"C",7:"N",8:"O",
    9:"F",10:"Ne",11:"Na",12:"Mg",13:"Al",14:"Si",15:"P",16:"S",
    17:"Cl",18:"Ar",19:"K",20:"Ca",21:"Sc",22:"Ti",23:"V",
    24:"Cr",25:"Mn",26:"Fe",27:"Co",28:"Ni"
}

for z in sorted(by_z.keys()):
    isos = sorted(by_z[z], key=lambda x: AZ[x][0])
    name = elem_names.get(z, f"Z={z}")
    print(f"  Z={z:>2d} ({name:>2s}): {', '.join(isos)}")

# Binding energy per nucleon for iron-peak
print(f"\n{'─'*W}")
print("  BINDING ENERGY PER NUCLEON — IRON PEAK")
print(f"{'─'*W}")
for iso in ["Fe-54","Fe-56","Fe-58","Co-59","Ni-56","Ni-58","Ni-60","Ni-62"]:
    a, z = AZ[iso]
    n_count = a - z
    # B = Z*m_p + N*m_n - M(A,Z)
    B = (z * M["p"] + n_count * M["n"] - M[iso]) * 931.494
    bpa = B / a
    print(f"  {iso:>6s}:  B/A = {bpa:.3f} MeV/nucleon  (B = {B:.1f} MeV)")

print(f"\n  → Ni-62 has the HIGHEST B/A, not Fe-56.")
print(f"    Fe-56 is most abundant because Ni-56 is the NSE product")
print(f"    and Ni-56 → Co-56 → Fe-56 via β-decay.\n")
