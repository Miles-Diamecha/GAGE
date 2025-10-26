# snf_check.py — exact-integer SNF + primitive kernel for ΔW_EM (version-robust)

from sympy import Matrix, ilcm, igcd, ZZ

A = Matrix([[8, 8, 224],
            [0, 1,  18]])  # ΔW_EM in (SU3, SU2, EM)

U = D = V = None

# 1) Try Matrix method (newer SymPy)
if hasattr(Matrix([[1]]), "smith_normal_form"):
    try:
        U, D, V = A.smith_normal_form()  # U*A*V = D
    except Exception:
        U = D = V = None

# 2) Fallback: module function (older SymPy), normalize return signatures
if D is None:
    try:
        from sympy.matrices.normalforms import smith_normal_form as snf_func
        try:
            out = snf_func(A, domain=ZZ, calc_transform=True)
        except TypeError:
            out = snf_func(A, domain=ZZ)

        # Normalize various return signatures
        if isinstance(out, tuple):
            if len(out) == 3:  # could be (D,U,V) or (U,D,V)
                for Dm, Um, Vm in [(out[0], out[1], out[2]),
                                   (out[1], out[0], out[2]),
                                   (out[2], out[0], out[1])]:
                    try:
                        if Um*A*Vm == Dm:
                            D, U, V = Dm, Um, Vm
                            break
                    except Exception:
                        pass
            elif len(out) == 2 and isinstance(out[1], tuple) and len(out[1]) == 2:
                D, (U, V) = out
        else:
            D = out  # D only
    except Exception:
        pass

# --- Validate SNF if available ---
m, n = A.shape
if D is not None:
    assert D.shape == (m, n)
    # rank = number of nonzero diagonal entries
    r = sum(1 for i in range(min(m, n)) if D[i, i] != 0)
    assert r == 2, f"Expected rank 2; got {r}"
    # columns beyond rank must be all zeros (here: the 3rd column)
    for j in range(r, n):
        assert all(D[i, j] == 0 for i in range(m)), "Trailing column not zero in D"
else:
    r = 2  # expected for this A; continue without D/U/V assertions

# --- Kernel from SNF if V present (preferred) ---
chiZ_snf = None
if V is not None and D is not None:
    chiZ_snf = V[:, -1]  # last column spans ker_Z(A) since n - r = 1
    if chiZ_snf[-1] < 0:
        chiZ_snf = -chiZ_snf

# --- Fallback: rational nullspace → integerize → primitive ---
chiQ = A.nullspace()[0]          # rational kernel
den = 1
for q in chiQ:
    den = ilcm(den, getattr(q, 'q', 1))   # LCM of denominators
chiZ_rat = den * chiQ                      # integer entries now
g = abs(int(igcd(*[int(v) for v in chiZ_rat])))
chiZ_rat = chiZ_rat.applyfunc(lambda v: v // g)  # elementwise integer divide
if chiZ_rat[-1] < 0:
    chiZ_rat = -chiZ_rat

# Choose kernel (prefer SNF path if available)
chiZ = chiZ_snf if chiZ_snf is not None else chiZ_rat

# Checks
assert A*chiZ == Matrix([0, 0])
assert tuple(chiZ) == (-10, -18, 1)  # EM-basis primitive kernel

# Unimodular transport to (αs, α2, α)
M = Matrix([[-5, -3, -2],
            [ 2,  1,  1],
            [ 2,  1,  0]])
assert M.det() in (1, -1)
chi_gauge = M.T * chiZ
assert tuple(chi_gauge) == (16, 13, 2)

# Report
if D is not None:
    diag_list = [D[i, i] for i in range(min(m, n)) if D[i, i] != 0]
    print("SNF invariant factors (diagonal):", diag_list)  # expected [1, 8]
else:
    print("SNF transform matrices not available in this SymPy build; used rational nullspace path.")
print("Primitive kernel in (SU3,SU2,EM):", tuple(chiZ))
print("Transported kernel in (αs,α2,α): ", tuple(chi_gauge))
print("All checks passed.")
