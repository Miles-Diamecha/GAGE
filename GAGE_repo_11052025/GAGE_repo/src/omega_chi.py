#!/usr/bin/env python3
import json, math
def load_pins(path="pins.json"):
    with open(path,"r") as f: return json.load(f)
def alpha2(alpha_em, sin2w): return alpha_em / sin2w
def omega_chi(a_s, a2, a): return (a_s**16)*(a2**13)*(a**2)
def alpha_G_pp(G, mp, hb, c): return G*(mp**2)/(hb*c)
def loo_alpha_s_star(aGpp, a2, a): return (aGpp/(a2**13*a**2))**(1.0/16.0)
if __name__=="__main__":
    P = load_pins(); Pp, Gp = P["pins"], P["gate"]
    aem = 1.0/float(Pp["inv_alpha_MZ"]); s2w=float(Pp["sin2_thetaW_MZ"]); a_s=float(Pp["alpha_s_MZ"])
    a2=alpha2(aem,s2w); aGpp=alpha_G_pp(float(Pp["G_N_SI"]),float(Pp["m_p_SI_kg"]),float(Pp["hbar_SI_Js"]),float(Pp["c_SI_mps"]))
    Om=omega_chi(a_s,a2,aem); closure=Om/aGpp; a_s_star=loo_alpha_s_star(aGpp,a2,aem)
    Lchi=float(Gp["sigma_chi"])/float(Gp["K_eq_norm_chi"])
    out={"alpha2_MZ":a2,"Omega_chi":Om,"alpha_G_pp":aGpp,"closure_ratio_Omega_over_alphaGpp":closure,"alpha_s_star_MZ":a_s_star,"Lambda_chi":Lchi}
    import sys, json
    with open("results.json","w") as f: json.dump(out,f,indent=2,sort_keys=True)
    s=(f"alpha2(MZ) = {a2:.9f}\n"+f"Omega_chi = {Om:.12e}\n"+f"alphaG_pp = {aGpp:.12e}\n"+
       f"closure Omega_chi/alphaG_pp = {closure:.8f}\n"+f"alpha_s* (LOO) = {a_s_star:.9f}\n"+f"Lambda_chi = {Lchi:.6f}\n")
    print(s,end=""); open("stdout.txt","w").write(s)
