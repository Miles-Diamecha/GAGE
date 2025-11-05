#!/usr/bin/env python3
import json
def load_gate(path="pins.json"):
    with open(path,"r") as f: j=json.load(f); return float(j["gate"]["sigma_chi"]), float(j["gate"]["K_eq_norm_chi"])
def deltaG_over_G_from_phi(phi, sigma, normK): dXi = normK*phi; return (dXi/sigma)**2
if __name__=="__main__":
    sigma, norm = load_gate(); phi=1.0
    print(f"phi_chi={phi}, DeltaG/G ~= {deltaG_over_G_from_phi(phi, sigma, norm):.6e}")
