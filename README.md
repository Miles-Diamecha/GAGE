# Gauge-Aligned Gravity Emergence (GAGE)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17537647.svg)](https://doi.org/10.5281/zenodo.17537647)

This repository contains the **reproducibility package** for  
**“Gauge-Aligned Gravity Emergence (GAGE): SM-derived gravitational coupling G(Q)”**,  
submitted to *Physical Review Letters* (2025).

All results in the Letter and Supplemental Material are generated deterministically from pinned inputs,  
with no stochastic or external dependencies. Rebuilding the full dataset reproduces  
every numeric table and figure in the manuscript.

---

GAGE_repo (deterministic, ASCII)

Purpose:
Recompute Omega_chi, alphaG_pp, closure Omega_chi/alphaG_pp, leave-one-out alpha_s*(MZ),
the lab quadratic null DeltaG/G ~= (DeltaXi/sigma_chi)^2, and the kinetic-metric
diagnostics: eigens of K_eq, ||chi||_K, alignment cos(theta), and Lambda_gate.

Quickstart:
1) Save these files as shown (flat folder, keep names).
2a) macOS/Linux:   bash build.sh
2b) Windows (PS):  .\build_win.bat
3) Inspect results.json, metric_results.json, stdout.txt, SHA256SUMS.txt

Determinism:
- No RNG, no network calls
- All constants pinned in pins.json and keq.json
- Checksums recorded in SHA256SUMS.txt

Outputs:
- results.json            # Omega_chi, alphaG_pp, closure, alpha_s* (LOO), Lambda_gate
- metric_results.json     # eigvals/evecs(K_eq), ||chi||_K, Lambda_gate(calc), alignment
- stdout.txt              # human-readable summaries (appended)
- SHA256SUMS.txt          # SHA-256 over the above artifacts

Run individually (PowerShell):
python src\omega_chi.py
python src\gate_null.py
python src\metric_eigs.py
python src\snf_check.py           # optional, needs sympy
python checksums.py

Optional:
- src/snf_check.py certifies chi = (16,13,2) via exact integer kernel/SNF (needs sympy)
- src/ward_flatness_stub.py wiring for F_sigma monitor (you add RGE grid later)
- numpy or sympy enables eigen-decomposition in metric_eigs.py (numpy preferred)
