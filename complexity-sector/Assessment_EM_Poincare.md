# Assessment: "The Intrinsic Geometry of Electromagnetism Is the Poincaré Homology Sphere"

Companion note to the complexity sector · 2026-11-23 · off-web, first-principles read

## Question asked
Does this document provide a route to a proof of P = NP?

## Finding
No. The document contains no complexity-theoretic content: no NP, no
polynomial-time bound, no reduction, no circuit model, no hardness notion.
It therefore cannot bear on the P vs NP separation, which is a statement about
computation time. This is decisive and independent of whether the document's
own claims are correct.

## Sound scaffolding (standard mathematics, used correctly)
- S³/I* is the Poincaré homology sphere Σ(2,3,5); left-invariant Beltrami
  frames on S³ give source-free Maxwell solutions (p. 1).
- Vol(S³/I*) = π²a³/60 = (ζ(2)/10)a³ via ζ(2) = π²/6 (p. 5).
- Milnor link of x²+y³+z⁵=0: μ = (2−1)(3−1)(5−1) = 8, intersection form −E8 (p. 5).
- Sieve characterization of primes; ζ functional equation (pp. 12–13).

## The characteristic error (local/finite truth asserted as global/limit truth)
Page 13 claims the Riemann Hypothesis (Z(Ξ) ⊂ iℝ) follows.
- TRUE and trivial: the finite divisor sum Φ_n(z) = Σ_{d|n} d^z has all zeros
  on Re z = 0 (cyclotomic; for n=4 roots at z = 2πik/(3 ln2), verified to 1e−16
  in rh_check.py).
- FALSE step: letting n → "∏ p^∞" does not transfer the zero locus to Ξ.
  Zero-sets pass to a limit only under locally-uniform convergence to a nonzero
  limit (Hurwitz). The normalized sums diverge off the axis
  (|Φ_{m!}(2+6i)| normalized = 1.79, 5.94, 23.1, 111, 671, 4.76e3, 3.81e4 for
  m=2..8), so there is no such limit and no transfer. RH is the unproven
  statement Z(Ξ) ⊂ iℝ; first nontrivial zero at Im z = 14.1347.
The particle-mass table (p. 2) is the same move: post-hoc matching of a computed
sequence to nearest known masses, with deviations up to tens of percent.

## Relation to the prior closure results
The new objects (Poincaré sphere, zeta, primes, the modal "Setspace") are
subject to the closure results N1–N7 of Complexity_Sector_v0_1.md. None of them
is a statement about computation time, so none meets necessary conditions R1–R3
that any proof of RS (≡ P ≠ NP) or its negation must meet. No P = NP proof
follows, and none is asserted here.

## The one genuine complexity seam
The algebraic fusion-symmetry dichotomy (T9–T10): the tractability boundary is
fixed by which coordinatewise operations preserve a constraint's solution set
(3-SAT hard = no fusion; parity easy = MIN fusion). This is where real
separation questions live. Unconditional lower bounds there are currently only
quadratic (Mignon–Ressayre). It is the honest frontier; this document does not
advance it.

## Verification
`rh_check.py` in this directory (numpy only). Confirms the finite-sum zero
locus and the failure of the limit transfer.
