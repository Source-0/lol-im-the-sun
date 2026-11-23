"""Three candidate polynomial-time selectors built from the framework, and the level each one needs.

C1  affine lift      : contraction of a MIN-symmetric (linear over GF(2)) parent of degree d
C2  diamond consistency: local compatibility on all variable sets of size <= k   (section 3.4 of v3.0)
C3  annealing        : near-reversible entropy-production protocol               (T7 of the working paper)

A clause is a tuple of (variable, sign); the literal is true when x[variable] == sign.
numpy only; every instance is certified by exhaustive enumeration.
"""
import itertools, math, sys, time
import numpy as np

rng = np.random.default_rng(11)
LN2 = math.log(2.0)

def violations(n, cls):
    X = ((np.arange(2 ** n)[:, None] >> np.arange(n)) & 1).astype(np.int8)
    V = np.zeros(2 ** n, dtype=np.int64)
    for c in cls:
        bad = np.ones(2 ** n, bool)
        for v, s in c: bad &= (X[:, v] != s)
        V += bad
    return V

# ---------------------------------------------------------------- instance families
def rand_3sat(n, ratio=5.0):
    out = []
    for _ in range(round(ratio * n)):
        vs = rng.choice(n, 3, replace=False)
        out.append(tuple((int(v), int(rng.integers(2))) for v in vs))
    return out

def rand_xor(n, ratio=1.0):
    out = []
    for _ in range(round(ratio * n)):
        vs = [int(v) for v in rng.choice(n, 3, replace=False)]; b = int(rng.integers(2))
        for a in itertools.product((0, 1), repeat=3):
            if sum(a) % 2 != b:                               # forbid this local assignment
                out.append(tuple((v, 1 - ai) for v, ai in zip(vs, a)))
    return out

def rand_horn(n, ratio=1.5):
    out = [((int(v), 1),) for v in rng.choice(n, 2, replace=False)]                       # facts
    for _ in range(round(ratio * n)):
        a, b, c = (int(v) for v in rng.choice(n, 3, replace=False))
        out.append(((a, 0), (b, 0), (c, 1)))                                              # a and b imply c
    for _ in range(2):
        a, b = (int(v) for v in rng.choice(n, 2, replace=False))
        out.append(((a, 0), (b, 0)))                                                      # goals
    return out

def rand_2sat(n, ratio=2.0):
    out = []
    for _ in range(round(ratio * n)):
        vs = rng.choice(n, 2, replace=False)
        out.append(tuple((int(v), int(rng.integers(2))) for v in vs))
    return out

def sample(gen, n, want_sat, count, **kw):
    got = []
    while len(got) < count:
        cls = gen(n, **kw)
        if ((violations(n, cls) == 0).any()) == want_sat: got.append(cls)
    return got

# ---------------------------------------------------------------- C1: affine lift of degree d
def affine_lift_refutes(n, cls, d, budget=None):
    """True iff 1 = sum_c g_c q_c over GF(2) with every product of degree <= d (static Nullstellensatz)."""
    idx = {}
    for j in range(d + 1):
        for comb in itertools.combinations(range(n), j):
            idx[sum(1 << v for v in comb)] = len(idx)        # the constant monomial gets index 0
    basis = {}; t0 = time.time()
    for j in range(0, d + 1):                                # multipliers by increasing degree
        for c in cls:
            w = len(c)
            if j > d - w: continue
            cm = sum(1 << v for v, _ in c)
            neg = sum(1 << v for v, s in c if s == 0); pos = [v for v, s in c if s == 1]
            terms = [neg | sum(1 << v for v in U) for r in range(len(pos) + 1) for U in itertools.combinations(pos, r)]
            others = [v for v in range(n) if not (cm >> v) & 1]
            for comb in itertools.combinations(others, j):
                mm = sum(1 << v for v in comb); row = 0
                for t in terms: row ^= 1 << idx[t | mm]
                while row:
                    hb = row.bit_length() - 1
                    if hb == 0: return True
                    b = basis.get(hb)
                    if b is None: basis[hb] = row; break
                    row ^= b
            if budget and time.time() - t0 > budget: return None
    return False

# ---------------------------------------------------------------- C2: diamond consistency of level k
def consistency_refutes(n, cls, k, budget=None):
    """True iff the family of locally compatible partial histories on sets of size <= k collapses."""
    t0 = time.time(); F = {}
    for j in range(k + 1):
        for comb in itertools.combinations(range(n), j):
            F[sum(1 << v for v in comb)] = np.ones((2,) * j, dtype=bool)
    for c in cls:
        cm = sum(1 << v for v, _ in c); others = [v for v in range(n) if not (cm >> v) & 1]
        for j in range(0, k - len(c) + 1):
            for comb in itertools.combinations(others, j):
                S = cm | sum(1 << v for v in comb)
                sl = [slice(None)] * (len(c) + j)
                for v, s in c: sl[bin(S & ((1 << v) - 1)).count("1")] = 1 - s
                F[S][tuple(sl)] = False
    pairs = []
    for S, arr in F.items():
        if arr.ndim < k:
            for v in range(n):
                if not (S >> v) & 1:
                    T = S | (1 << v); pairs.append((F[S], F[T], bin(T & ((1 << v) - 1)).count("1")))
    total = sum(int(a.sum()) for a in F.values())
    while True:
        for FS, FT, p in pairs:
            np.logical_and(FT, np.expand_dims(FS, p), out=FT)      # restriction of a compatible history is compatible
            np.logical_and(FS, FT.any(axis=p), out=FS)            # a compatible history extends to every further variable
        if not F[0]: return True
        new = sum(int(a.sum()) for a in F.values())
        if new == total: return False
        total = new
        if budget and time.time() - t0 > budget: return None

def min_level(test, n, cls, lo, hi, budget):
    for lev in range(lo, hi + 1):
        r = test(n, cls, lev, budget)
        if r is None: return f">{lev - 1}*"
        if r: return lev
    return f">{hi}"

# ---------------------------------------------------------------- C3: annealing
def anneal_success(n, V, T):
    N = 2 ** n; idx = np.arange(N); bT = (n + 2) * LN2
    flips = [idx ^ (1 << i) for i in range(n)]
    up = [np.maximum(V[f] - V, 0) for f in flips]; top = int(max(u.max() for u in up))
    mu = np.full(N, 1.0 / N); sigma_f = 0.0
    logZ = lambda b: math.log(np.exp(-b * V).sum())
    for t in range(1, T + 1):
        beta = bT * t / T
        sigma_f += (bT / T) * float(mu @ V)                      # work increment at the pre-step state
        tab = np.exp(-beta * np.arange(top + 1)) / n
        out = np.zeros(N); stay = np.ones(N)
        for i in range(n):
            a = tab[up[i]]; out += (mu * a)[flips[i]]; stay -= a
        mu = out + mu * stay
    sigma_f += logZ(bT) - logZ(0.0)                              # Sigma_F = <W> - dF, dF = -(logZ_T - logZ_0)
    return float(mu[V == 0].sum()), sigma_f

if __name__ == "__main__":
    quick = "--quick" in sys.argv
    sizes = [6, 8, 10] if quick else [6, 8, 10, 12, 14]
    reps = 3 if quick else 5
    print("== soundness: neither lift ever refutes a satisfiable instance ==")
    bad = 0
    for gen, kw in [(rand_3sat, dict(ratio=3.5)), (rand_xor, dict(ratio=0.7)), (rand_horn, {}), (rand_2sat, dict(ratio=0.8))]:
        for cls in sample(gen, 8, True, 3, **kw):
            bad += bool(affine_lift_refutes(8, cls, 5)) + bool(consistency_refutes(8, cls, 5))
    print(f"false refutations on 12 satisfiable instances at levels d=5, k=5: {bad}")

    print("\n== minimal level that refutes an unsatisfiable instance (median [min..max]) ==")
    print(f"{'family':10s} {'n':>3s}  {'C1 affine degree d':24s} {'C2 consistency level k':24s}")
    fams = [("3-SAT", rand_3sat, dict(ratio=4.5)), ("parity", rand_xor, dict(ratio=1.0)),
            ("Horn", rand_horn, {}), ("2-CNF", rand_2sat, dict(ratio=2.0))]
    def summary(vals):
        nums = [v for v in vals if isinstance(v, int)]; caps = [v for v in vals if not isinstance(v, int)]
        if not nums: return ",".join(sorted(set(caps)))
        s = f"{int(np.median(nums))} [{min(nums)}..{max(nums)}]"
        return s + (f" +{len(caps)} capped {sorted(set(caps))[0]}" if caps else "")
    for name, gen, kw in fams:
        for n in sizes:
            hi = min(n, 8 if n <= 12 else 7); budget = 150 if n >= 14 else 90
            D, K = [], []
            for cls in sample(gen, n, False, reps if n < 14 else 3, **kw):
                w = min(len(c) for c in cls)
                D.append(min_level(affine_lift_refutes, n, cls, w, hi, budget))
                K.append(min_level(consistency_refutes, n, cls, 2, hi, budget))
            print(f"{name:10s} {n:3d}  {summary(D):24s} {summary(K):24s}", flush=True)

    print("\n== C3: shortest linear anneal with success probability >= 1/2 (one-solution 3-SAT, ratio 4.5) ==")
    print(f"{'n':>3s} {'instances':>9s}  {'T_half median [min..max]':28s} {'Sigma_F at T_half (median)':>26s}")
    for n in ([6, 8, 10] if quick else [6, 8, 10, 12, 14]):
        Ts, Ss = [], []
        for _ in range(3 if n >= 14 else 5):
            while True:
                cls = rand_3sat(n, ratio=4.5); V = violations(n, cls)
                if (V == 0).sum() == 1: break
            T = 1
            while True:
                p, s = anneal_success(n, V, T)
                if p >= 0.5 or T >= 2 ** 16: break
                T *= 2
            Ts.append(T if p >= 0.5 else 2 ** 17); Ss.append(s)
        print(f"{n:3d} {len(Ts):9d}  {int(np.median(Ts)):8d} [{min(Ts)}..{max(Ts)}]{'':10s} {np.median(Ss):26.3f}", flush=True)
