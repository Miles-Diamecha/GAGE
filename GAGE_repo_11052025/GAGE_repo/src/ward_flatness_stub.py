#!/usr/bin/env python3
def betaXi_over_logQ(alpha_s, alpha2, alpha_em, betas):
    return 16*betas["beta_s"]/alpha_s + 13*betas["beta_2"]/alpha2 + 2*betas["beta_em"]/alpha_em
def normalized_F_sigma(betaXi, sigma_chi): return betaXi / sigma_chi
if __name__=="__main__":
    print("Stub: provide (Q, alpha_s, alpha_2, alpha, betas) grid and accumulate |F_sigma| stats.")
