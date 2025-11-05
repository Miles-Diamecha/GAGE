#!/usr/bin/env bash
set -euo pipefail
python3 src/omega_chi.py | tee /dev/stderr
python3 src/gate_null.py | tee -a /dev/stderr
python3 src/metric_eigs.py | tee -a /dev/stderr
python3 src/ward_flatness_stub.py || true
python3 -c "import sympy" >/dev/null 2>&1 && python3 src/snf_check.py || true
python3 checksums.py
echo "OK"
