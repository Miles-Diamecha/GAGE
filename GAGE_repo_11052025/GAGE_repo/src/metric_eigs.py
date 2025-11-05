#!/usr/bin/env python3
import json, math, pathlib
HERE=pathlib.Path(__file__).resolve().parent; ROOT=HERE.parent
def load_json(name):
    p=HERE/name; 
    if not p.exists(): p=ROOT/name
    return json.loads(p.read_text())
def is_sym(M,tol=1e-12):
    return all(abs(M[i][j]-M[j][i])<=tol for i in range(3) for j in range(3))
def matvec(M,v): return [sum(M[i][j]*v[j] for j in range(3)) for i in range(3)]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def eigen(M):
    try:
        import numpy as np
        w,V = np.linalg.eigh(np.array(M,dtype=float))
        evecs=[[V[i,k] for i in range(3)] for k in range(3)]
        return w.tolist(), evecs
    except Exception:
        from sympy import Matrix
        mat=Matrix(M); evects=mat.eigenvects(); pairs=[]
        import math as _m
        for ev,m,vecs in evects:
            for v in vecs:
                vv=[float(x) for x in v]; n=_m.sqrt(sum(x*x for x in vv)) or 1.0
                vv=[x/n for x in vv]; pairs.append((float(ev), vv))
        pairs.sort(key=lambda t:t[0]); return [p[0] for p in pairs],[p[1] for p in pairs]
if __name__=="__main__":
    pins=load_json("pins.json"); chi=[float(x) for x in pins["projector"]["chi"]]
    sig=float(pins["gate"]["sigma_chi"]); keq_norm=float(pins["gate"]["K_eq_norm_chi"])
    K=load_json("keq.json")["K_eq"]; 
    if not is_sym(K): K=[[0.5*(K[i][j]+K[j][i]) for j in range(3)] for i in range(3)]
    Kchi=matvec(K,chi); chi_normK=math.sqrt(dot(chi,Kchi))
    evals,evecs=eigen(K); v_soft=evecs[0]; n=math.sqrt(dot(v_soft,v_soft)) or 1.0; v_soft=[x/n for x in v_soft]
    chi_norm=math.sqrt(dot(chi,chi)); cos_th=abs(dot(chi,v_soft)/chi_norm) if chi_norm else float("nan")
    Lcalc=sig/chi_normK; Lpin=sig/keq_norm if keq_norm else float("inf")
    out={"K_eq":K,"eigvals_sorted":evals,"soft_index":0,"v_soft":v_soft,"chi":chi,"chi_norm_K":chi_normK,
         "chi_norm_K_pinned":keq_norm,"chi_norm_K_diff":chi_normK-keq_norm,"sigma_chi":sig,
         "Lambda_chi_calc":Lcalc,"Lambda_chi_from_pins":Lpin,"Lambda_chi_diff":Lcalc-Lpin,"alignment_cosine":cos_th}
    (ROOT/"metric_results.json").write_text(json.dumps(out,indent=2,sort_keys=True))
    lines=[
      "K_eq eigenvalues (asc): "+", ".join(f"{x:.7f}" for x in evals),
      "Soft-mode eigenvector: ("+", ".join(f"{x:.7f}" for x in v_soft)+")",
      f"||chi||_K (computed): {chi_normK:.6f}",
      f"||chi||_K (pinned) : {keq_norm:.6f}",
      f"Lambda_chi (calc) : {Lcalc:.6f}",
      f"Lambda_chi (pins) : {Lpin:.6f}",
      f"Lambda diff : {Lcalc-Lpin:.6e}",
      f"Alignment cos(theta): {cos_th:.7f}"
    ]
    s="\n".join(lines)+"\n"; print(s,end=""); open(ROOT/"stdout.txt","a").write(s)
