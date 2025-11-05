@echo off
python src\omega_chi.py
python src\gate_null.py
python src\metric_eigs.py
python src\ward_flatness_stub.py
python -c "import sympy" >nul 2>&1 && python src\snf_check.py
python checksums.py
echo OK
