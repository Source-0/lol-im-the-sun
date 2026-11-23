# Check the document's zeta/RH argument on p.13: does Z(Phi_n) on the imaginary axis
# say anything about the zeros of the completed zeta Xi?
import numpy as np, math

def divisors(n):
    return [d for d in range(1, n+1) if n % d == 0]

def Phi_sum(n, z):            # Sum_{d|n} d^z  (the finite divisor exponential sum)
    return sum(complex(d) ** z for d in divisors(n))

# (A) Finite claim: zeros of Sum_{d|n} d^z lie on Re z = 0.  Scan a grid, report where |.| is tiny.
for n in [12, 30, 36]:
    re = np.linspace(-3, 3, 61); im = np.linspace(0.1, 25, 400)
    best = []
    for x in re:
        col = np.array([abs(Phi_sum(n, complex(x, y))) for y in im])
        # local minima below a small threshold
        for k in range(1, len(col)-1):
            if col[k] < col[k-1] and col[k] < col[k+1] and col[k] < 1e-6:
                best.append((round(x,3), round(im[k],2)))
    # analytic roots for n = p^A: z = 2πi k /((A+1) ln p)
    print(f"n={n}: numeric near-zeros (Re z, Im z) -> {sorted(set(best))[:6]}")

# analytic root check for n = 2^2 = 4 : Sum = 1 + 2^z + 4^z = (8^z -1)/(2^z -1)? no: geometric in 2^z
# roots: (2^z)^3 = 1, 2^z != 1  => z = 2πi k/(3 ln2)
k = np.arange(1,4)
roots = 2j*np.pi*k/(3*np.log(2))
print("n=4 analytic roots z =", [f"{r.real:.3f}+{r.imag:.3f}i" for r in roots],
      "-> |Sum| =", [f"{abs(1+2**r+4**r):.2e}" for r in roots])

# (B) The transfer step. Hurwitz's theorem: zero-sets pass to a limit only under
# locally-uniform convergence to a non-identically-zero limit. Does Phi_n -> zeta that way?
# The document's limit is n -> "prod p^infinity". Show the normalized finite sums do NOT
# converge locally uniformly off the axis: evaluate at a fixed z and grow n through factorials.
z0 = 2.0 + 6.0j                       # a generic point, Re z0 = 2 (off the axis)
vals = [abs(Phi_sum(math.factorial(m), z0)) / (math.factorial(m) ** (z0.real/2))
        for m in range(2, 9)]
print("normalized |Phi_{m!}(z0)| for m=2..8 at z0=2+6i:", [f"{v:.3g}" for v in vals])
print("-> sequence diverges/oscillates; no locally-uniform limit, so Hurwitz does not transfer zeros.")

# First nontrivial zeta zero (textbook constant): s = 1/2 + 14.134725 i, i.e. z = s-1/2 = 14.1347 i
print("First Riemann zero in z=s-1/2 coord: Re z = 0, Im z = 14.1347 (this is WHERE RH lives; unproven).")
