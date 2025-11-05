#!/usr/bin/env python3
import hashlib, os
def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''): h.update(chunk)
    return h.hexdigest()
if __name__=="__main__":
    outs=[p for p in ["results.json","metric_results.json","stdout.txt"] if os.path.exists(p)]
    with open("SHA256SUMS.txt","w") as f:
        for p in outs:
            s=f"{sha256(p)} {p}"; print(s); f.write(s+"\n")
