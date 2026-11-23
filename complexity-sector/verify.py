"""Finite checks for the complexity-sector theorems (numpy only, exact enumeration)."""
import itertools, math
import numpy as np

rng = np.random.default_rng(7)
LN2 = math.log(2.0)

def random_3cnf(n, m):
    cls = []
    for _ in range(m):
        vs = rng.choice(n, 3, replace=False)
        sg = rng.integers(0, 2, 3)          # literal is true when x[v] == sg
        cls.append((vs, sg))
    return cls

def violations(n, cls):
    X = ((np.arange(2 ** n)[:, None] >> np.arange(n)) & 1)
    V = np.zeros(2 ** n, dtype=int)
    for vs, sg in cls:
        V += np.all(X[:, vs] != sg, axis=1)
    return X, V

def logsumexp(a):
    m = a.max(); return m + math.log(np.exp(a - m).sum())

print("== T2/T4: rate function and generator versus brute-force counting ==")
for n, m in [(8, 30), (10, 40), (12, 50), (12, 62)]:
    cls = random_3cnf(n, m); X, V = violations(n, cls)
    nsat = int((V == 0).sum())
    psi = lambda J: logsumexp(J * V) - n * LN2            # eq. (98) with uniform reference law
    gamma0 = -psi(-200.0)                                 # sup_J {J*0 - Psi[J]} is reached as J -> -inf
    exact = n * LN2 - math.log(nsat) if nsat else float("inf")
    J1 = -(n + 1) * LN2
    recovered = math.floor(2 ** n * math.exp(psi(J1)) + 1e-9)
    print(f"n={n} m={m} #SAT={nsat:5d}  Gamma[0]={gamma0:.6f}  n ln2 - ln#SAT={exact:.6f}  "
          f"#SAT from one Psi evaluation={recovered}")

print("\n== T5: Doob transform of the fair-coin history is the uniform law on solutions ==")
n, m = 10, 38
cls = random_3cnf(n, m); X, V = violations(n, cls); sol = (V == 0)
h = {}
def hval(prefix):                                          # Pr[satisfied | prefix]
    k = len(prefix)
    if prefix not in h:
        mask = np.ones(2 ** n, bool)
        for i, b in enumerate(prefix): mask &= (X[:, i] == b)
        h[prefix] = sol[mask].mean()
    return h[prefix]
law = np.zeros(2 ** n)
for idx in np.flatnonzero(sol):
    bits = tuple(int(b) for b in X[idx]); p = 1.0
    for k in range(n):
        p *= hval(bits[:k + 1]) / (2 * hval(bits[:k]))
    law[idx] = p
print(f"#SAT={sol.sum()}  total mass={law.sum():.12f}  max|law - 1/#SAT|={np.abs(law[sol] - 1 / sol.sum()).max():.2e}")

print("\n== T7: dissipation-search inequalities on exact path measures ==")
def metropolis(n, V, beta):
    N = 2 ** n; K = np.zeros((N, N)); idx = np.arange(N)
    for i in range(n):
        j = idx ^ (1 << i)
        acc = np.minimum(1.0, np.exp(-beta * (V[j] - V[idx]))) / n
        K[idx, j] = acc
    K[idx, idx] = 1.0 - K.sum(axis=1)
    return K
n, m = 8, 30
while True:
    cls = random_3cnf(n, m); X, V = violations(n, cls)
    if (V == 0).sum() >= 1: break
sol = (V == 0); bT = (n + 2) * LN2
worst_f, worst_r = float("inf"), float("inf")
for T in [1, 4, 16, 64, 256, 1024]:
    for shape in [1.0, 2.0, 0.5]:
        betas = bT * (np.arange(T + 1) / T) ** shape
        logZ = [logsumexp(-b * V) for b in betas]
        dF = -(logZ[-1] - logZ[0])
        mu = np.full(2 ** n, 2.0 ** -n); w = mu.copy(); EW_f = 0.0
        Ks = [metropolis(n, V, b) for b in betas[1:]]
        for s in range(T):
            db = betas[s + 1] - betas[s]
            EW_f += db * (mu @ V)
            w = (w * np.exp(-db * V)) @ Ks[s]
            mu = mu @ Ks[s]
        piT = np.exp(-bT * V - logZ[-1])
        nu = piT.copy(); EW_r = 0.0
        for s in range(T - 1, -1, -1):
            nu = nu @ Ks[s]
            EW_r += (betas[s + 1] - betas[s]) * (nu @ V)
        sig_f, sig_r = EW_f - dF, dF - EW_r
        p, q = mu[sol].sum(), piT[sol].sum()
        slack_f = p - (q - math.sqrt(max(sig_f, 0) / 2))
        slack_r = (sig_r + LN2) / q - math.log(1 / p)
        worst_f, worst_r = min(worst_f, slack_f), min(worst_r, slack_r)
        if shape == 1.0:
            print(f"T={T:5d}  <e^-Sigma>={w.sum() / math.exp(-dF):.10f}  Sigma_F={sig_f:8.4f}  Sigma_R={sig_r:8.4f}  "
                  f"p_success={p:.4f}  pi_T(Sol)={q:.4f}")
print(f"minimum slack over all protocols: forward bound {worst_f:.4f}, reverse bound {worst_r:.4f} (both must be >= 0)")

print("\n== T8/T9: fusion symmetries and contraction universality ==")
def rel(arity, pred): return frozenset(t for t in itertools.product((0, 1), repeat=arity) if pred(*t))
OR3 = rel(3, lambda x, y, z: x | y | z); ONE3 = rel(3, lambda x, y, z: x + y + z == 1)
XOR0 = rel(3, lambda x, y, z: (x ^ y ^ z) == 0); HORN = rel(3, lambda x, y, z: (not (x and y)) or z)
TWO = rel(2, lambda x, y: x | y)
ops = {"AND": (2, lambda a, b: a & b), "OR": (2, lambda a, b: a | b),
       "MAJ": (3, lambda a, b, c: (a & b) | (a & c) | (b & c)), "MIN": (3, lambda a, b, c: a ^ b ^ c)}
def preserved(R, k, f):
    return all(tuple(f(*col) for col in zip(*ts)) in R for ts in itertools.product(R, repeat=k))
SAT3 = [rel(3, lambda x, y, z, s=s: (x == s[0]) or (y == s[1]) or (z == s[2])) for s in itertools.product((0, 1), repeat=3)]
for name, L in [("3-SAT (all 8 sign patterns)", SAT3), ("1-in-3", [ONE3]), ("XOR", [XOR0]), ("Horn clause", [HORN]), ("2-clause", [TWO])]:
    found = [nm for nm, (k, f) in ops.items() if all(preserved(R, k, f) for R in L)]
    print(f"{name:28s} fusions: " + (", ".join(found) if found else "none"))
allrel = [frozenset(t for i, t in enumerate(itertools.product((0, 1), repeat=3)) if (msk >> i) & 1) for msk in range(256)]
print("three-variable relations invariant under each fusion: " +
      ", ".join(f"{nm}={sum(preserved(R, k, f) for R in allrel)}" for nm, (k, f) in ops.items()))

ok_neg = all(((xp == 1 - x) == any(((x, xp, f) in ONE3) and f == 0 for f in (0, 1))) for x in (0, 1) for xp in (0, 1))
ok_or = all(((x | y | z) == 1) == any(((1 - x, a, b) in ONE3) and ((b, y, c) in ONE3) and ((c, d, 1 - z) in ONE3)
            for a, b, c, d in itertools.product((0, 1), repeat=4)) for x, y, z in itertools.product((0, 1), repeat=3))
print(f"negation gadget from 1-in-3 + pinned 0: {ok_neg};  3-clause gadget from 1-in-3: {ok_or}")

# contraction closure inside a four-variable workspace (relations = 16-bit masks)
A = np.arange(65536, dtype=np.uint32)
def table(src_to_dst):
    t = np.zeros(65536, dtype=np.uint32)
    for i in range(16): t |= ((A >> i) & 1) << src_to_dst[i]
    return t
perm_tabs = []
for p in itertools.permutations(range(4)):
    mp = [sum(((i >> c) & 1) << p[c] for c in range(4)) for i in range(16)]
    perm_tabs.append(table(mp))
flip_tabs = [table([i ^ (1 << c) for i in range(16)]) for c in range(4)]
def mask(pred): return sum(1 << i for i in range(16) if pred(*[(i >> c) & 1 for c in range(4)]))
def closure(seeds):
    mark = np.zeros(65536, bool); mark[list(seeds)] = True; mark[65535] = True
    frontier = np.flatnonzero(mark).astype(np.uint32)
    while frontier.size:
        before = mark.copy()
        for t in perm_tabs: mark[t[frontier]] = True
        for t in flip_tabs: mark[frontier | t[frontier]] = True          # contraction over one hidden variable
        S = np.flatnonzero(mark).astype(np.uint32)
        F = np.flatnonzero(mark & ~before).astype(np.uint32); F = np.union1d(F, frontier)
        for i in range(0, F.size, 256):
            mark[np.bitwise_and.outer(F[i:i + 256], S).ravel()] = True   # conjunction of constraints
        frontier = np.flatnonzero(mark & ~before).astype(np.uint32)
        if mark.all(): break
    S = np.flatnonzero(mark).astype(np.uint32)
    ternary = int((flip_tabs[3][S] == S).sum())                          # relations not depending on variable 4
    return int(mark.sum()), ternary
common = [mask(lambda a, b, c, d: a == 0), mask(lambda a, b, c, d: a == 1), mask(lambda a, b, c, d: a == b)]
for name, seeds in [("1-in-3 parent", [mask(lambda a, b, c, d: a + b + c == 1)]),
                    ("XOR parent", [mask(lambda a, b, c, d: (a ^ b ^ c) == 0), mask(lambda a, b, c, d: (a ^ b ^ c) == 1)]),
                    ("Horn parent", [mask(lambda a, b, c, d: (not (a and b)) or c)]),
                    ("2-clause parent", [mask(lambda a, b, c, d: a | b), mask(lambda a, b, c, d: (1 - a) | b), mask(lambda a, b, c, d: (1 - a) | (1 - b))])]:
    tot, ter = closure(seeds + common)
    print(f"{name:16s} sectors reachable by contraction: {tot:5d} of 65536 four-variable relations, {ter:3d} of 256 three-variable relations")
