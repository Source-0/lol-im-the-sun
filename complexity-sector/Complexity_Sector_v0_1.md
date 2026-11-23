# Universal Mechanics — Complexity Sector

Working paper v0.1 · 2026-11-23 · companion to Universal Mechanics v3.0

**Scope.** An attempt to decide P versus NP using the objects of Universal Mechanics v3.0. Labels follow §1.2 of v3.0: [T] theorem, [A] axiom, [D] definition, [C] conditional theorem, [P] proposal, [O] open. "Established" marks a published theorem used without proof. Those are listed in §10 and were cited from memory, with no lookup, so each should be checked against its source before reuse.

---

## 0. Outcome

**No proof of P = NP or of P ≠ NP was obtained.** The work produced four things.

1. **Exact embedding.** Four statements about framework objects, each proved equivalent to P = NP (T2, T3, T6a, T10), and one proved equivalent to NP = RP (T6b).
2. **One structural theorem.** A parent whose contractions yield every sector has an NP-complete selection problem. A parent with a replica-fusion symmetry has a polynomial-time selector and provably cannot yield every sector (T9, T10).
3. **Seven closed routes.** For each theorem-grade tool of v3.0, a proof that it cannot decide the question in either direction (N1–N7).
4. **One residual statement**, RS in §7, equivalent to P ≠ NP, with five necessary conditions that any proof of it must meet. No tool currently in the framework meets them.

---

## 1. Definitions [D]

**D1. Regulated local history theory.** For an instance string w of length n:

- history space H_w = {0,1}^m with m ≤ poly(n);
- local action S_w(x) = Σ_c s_c(x restricted to I_c), with |I_c| ≤ k for a fixed k, polynomially many terms, and nonnegative rational values of polynomial bit length;
- reference law Π_w(x) = exp(−S_w(x)) / Z_w, the finite-alphabet form of eqs. (22)–(23);
- coarse observable O_w : H_w → Q^d with d ≤ poly(n), computable in polynomial time;
- the map w ↦ (S_w, O_w) is computable in polynomial time.

**D2. Generator and rate.** As in eqs. (98)–(99), contracted onto the observable:

    Ψ_w[J] = log Σ_x Π_w(x) exp⟨J, O_w(x)⟩,        Γ_w[o] = sup_J { ⟨J, o⟩ − Ψ_w[J] }.

**D3. Problems.**

- FIN: given (w, o), is Γ_w[o] finite?
- SEL: given w, output a minimizer of S_w. This is eq. (8) for a sharp event.
- GEN: given (w, J) with exp(J) rational, output Ψ_w[J] to poly(n) bits.
- TILT: given w and a weight exp(S_obs) computed by a polynomial-size circuit with values in [2^(−p(n)), 1], output a sample within total-variation distance 1/4 of Π_w^obs ∝ exp(S_obs) Π_w. This is eqs. (35) and (105).

**D4. Causal theory.** A regulated theory is causal if H = H^0 × … × H^T with T ≤ poly(n) and

    Π(x) = π_0(x^0) · K_1(x^0, x^1) · … · K_T(x^(T−1), x^T),

where π_0 is a product law and each K_t is a product of local stochastic kernels. This is the Markov sector of §9 and §19.3 with a single, past boundary condition, as in eq. (9). Sampling from causal theories is exactly randomized polynomial-time computation: a causal theory is a probabilistic circuit, and every probabilistic circuit is one.

**D5. Languages, sectors, fusions.**

- A Boolean language L is a finite set of relations R ⊆ {0,1}^r. It always contains the pins {0} and {1}, which play the role of the boundary data B in eq. (8), and equality.
- An L-action is S(x) = Σ_c [x restricted to I_c is not in R_c], with each R_c in L.
- The sharp contraction onto visible variables y is Γ(y) = min_z S(y, z), the zero-temperature form of eqs. (3)–(6).
- A sector of L is any relation of the form { y : Γ(y) = 0 }.
- L is contraction-universal if every Boolean relation is a sector of L.
- A fusion symmetry of L is an operation f : {0,1}^k → {0,1} such that, for every R in L, applying f coordinatewise to any k tuples of R gives a tuple of R. It acts on k replicas of a history, the replicated ensemble of §19.1. The pins force f(a, …, a) = a.
- ZERO(L): given an L-action, is min S = 0?
- The four basic fusions are AND, OR, MAJ (majority of three) and MIN (x ⊕ y ⊕ z).

---

## 2. Embedding theorems

**T1 [T]. Variational form.** Γ_w[o] = min { D(r ‖ Π_w) : r a law on H_w with E_r[O_w] = o }, and +∞ if no such r exists. Hence Γ_w[o] is finite exactly when o lies in M_w = conv O_w(H_w).

*Proof.* The Gibbs variational principle gives Ψ[J] = max_r { ⟨J, E_r O⟩ − D(r ‖ Π) }. So Ψ = G*, where G(o) is the stated minimum. G is convex because D is convex in r and the constraint is linear. G is lower semicontinuous because the simplex is compact and D(· ‖ Π) is continuous on it when Π > 0. Fenchel–Moreau gives Γ = Ψ* = G** = G. Since Π > 0, D(r ‖ Π) is finite for every r, so G(o) is finite exactly when some r has mean o. ∎

**T2 [T]. FIN is NP-complete.**

*In NP.* By Carathéodory, o ∈ M_w exactly when o is a convex combination of at most d + 1 points O_w(x_i). The witness is the list of histories x_i. The verifier computes each O_w(x_i) and solves a linear feasibility problem of polynomial size.

*NP-hard.* Let φ be a 3-CNF formula on n variables. Take the theory T_φ with H = {0,1}^n, S ≡ 0 (uniform Π) and O(x) = V_φ(x), the number of clauses x violates, which is a sum of 3-local terms. Since V_φ ≥ 0, the point o = 0 lies in conv V_φ(H) exactly when some x has V_φ(x) = 0. ∎

*Value.* By T1 the minimizing r is uniform on the solutions, so

    Γ_φ[0] = n ln 2 − ln #SAT(φ).

**Corollary.** P = NP if and only if FIN is in P.

*Remark.* Planar 3-SAT is NP-complete (established), so restricting the action to nearest-neighbour terms on a two-dimensional lattice does not remove the hardness.

**T3 [T].** P = NP if and only if SEL is computable in polynomial time.

*Proof.* If SEL is polynomial, apply it to S = V_φ and check whether the output satisfies φ. Conversely SEL is computable in polynomial time with an NP oracle: binary search on the minimum value, then fix variables one at a time. If P = NP the oracle is free. ∎

**T4 [T]. GEN is #P-hard.** For the theory T_φ,

    #SAT(φ) = floor( 2^n · exp Ψ_φ[ −(n+1) ln 2 ] ).

*Proof.* Let N_k be the number of assignments violating exactly k clauses. Then 2^n exp Ψ_φ[J] = Σ_k N_k exp(Jk). At exp(J) = 2^(−(n+1)) the terms with k ≥ 1 sum to at most 2^n · 2^(−(n+1)) = 1/2. ∎

**Summary.** The three primitive objects of §3 of v3.0 sit at three different levels: the effective domain of Γ is NP-complete, the selector (8) is equivalent to NP search, and the generator (1) is #P-hard.

---

## 3. Terminal conditioning: the observer tilt as a Doob transform

**T5 [T]. Doob transform of the fair-coin history.** Take the causal theory of n independent fair bits x_1, …, x_n and condition on the terminal event "φ(x) is true". This is the limit of the tilt (35) in which S_obs → −∞ off the solutions. Define

    h(x_1 … x_k) = Pr[ φ(x) true | x_1 … x_k ] = #SAT(φ restricted by the prefix) / 2^(n−k).

If h(∅) > 0, the conditioned law is uniform on the solutions and is Markov in k with kernel

    K^h(prefix ; b) = h(prefix b) / (2 h(prefix)).

h is harmonic: h(p) = [h(p0) + h(p1)] / 2. Deciding h > 0 is NP-complete and evaluating h is #P-complete.

*Proof.* Direct computation; the product of the kernels along a solution telescopes to 1 / (2^n h(∅)) = 1 / #SAT(φ). ∎

**T6 [T]. Compiling the tilt.**

(a) P = NP if and only if there is a polynomial-time map σ(φ, prefix) ∈ {0,1} with h(prefix σ) > 0 whenever h(prefix) > 0. Such a σ is a deterministic, support-preserving stand-in for the Doob kernel.

(b) TILT is solvable in randomized polynomial time for all regulated local theories if and only if NP = RP.

*Proof of (a).* If P = NP, set σ = 0 when φ restricted by (prefix, 0) is satisfiable, else 1. Conversely, run σ from the empty prefix n times and test the result. If φ is satisfiable the invariant h > 0 holds at every step, so the result satisfies φ. ∎

*Proof of (b).* Forward direction: given φ, use uniform Π and the weight 2^(−(n+2) V_φ(x)). If φ is satisfiable, non-solutions carry at most 2^n · 2^(−(n+2)) = 1/4 of the tilted mass, so a TILT sampler returns a solution with probability at least 1/2, and a returned solution can be verified. So SAT is in RP. Reverse direction: if NP = RP then NP ⊆ BPP. Almost-uniform generation of witnesses reduces to approximate counting (established, Jerrum–Valiant–Vazirani), and approximate counting is in randomized polynomial time with an NP oracle (established, Stockmeyer). The oracle is then simulated in BPP with exponentially small error. Weights are handled by sampling pairs (x, y) with y uniform below a rounded integer multiple of the weight of x, which is an NP witness relation. ∎

**Reading.** Equation (9) fixes one boundary, the past. A theory with only that boundary is causal and has exactly the power of randomized polynomial time (D4). The tilt (35) and the causal weight in eq. (90) add a condition on the future. By T6, P versus NP is the question of whether a two-boundary local history theory can always be recompiled into a one-boundary theory at polynomial cost. The object that must be computed to do so is the harmonic function h.

---

## 4. Entropy production and search

Fix a cost V on {0,1}^n with solution set Sol = { V = 0 }, assumed nonempty. An annealing protocol consists of inverse temperatures 0 = β_0, β_1, …, β_T and kernels K_t reversible with respect to π_t ∝ exp(−β_t V).

- Forward law P_F: x_0 uniform, then x_t drawn from K_t(x_(t−1), ·).
- Reverse law P_R: x_T drawn from π_T, then x_(t−1) drawn from K_t(x_t, ·).
- Work W = Σ_s (β_(s+1) − β_s) V(x_s), free-energy change ΔF = −ln(Z_T / Z_0), entropy production Σ = W − ΔF.

Write p = Pr_F[x_T ∈ Sol], q = π_T(Sol), ⟨Σ⟩_F = D(P_F ‖ P_R), ⟨Σ⟩_R = D(P_R ‖ P_F).

**T7 [T]. Dissipation–search inequalities.**

(a) Σ = ln(P_F / P_R) on every path, so ⟨exp(−Σ)⟩_F = 1 and ⟨Σ⟩_F ≥ 0. This is eqs. (31) and (34).

(b) p ≥ q − sqrt( ⟨Σ⟩_F / 2 ).

(c) ln(1/p) ≤ ( ⟨Σ⟩_R + ln 2 ) / q.

(d) With β_T = (n+2) ln 2, q ≥ 4/5.

*Proof.* (a) Detailed balance gives K_t(y, x) = K_t(x, y) π_t(x) / π_t(y). Substituting into P_R and summing by parts gives ln(P_F / P_R) = Σ_s (β_(s+1) − β_s) V(x_s) + ln(Z_T / Z_0). (b) The time-T marginals of P_F and P_R are the protocol output law μ_T and π_T. Data processing gives D(μ_T ‖ π_T) ≤ ⟨Σ⟩_F, and Pinsker bounds the total-variation distance by sqrt(⟨Σ⟩_F / 2). (c) Data processing in the other order gives ⟨Σ⟩_R ≥ D(π_T ‖ μ_T) ≥ q ln(q/p) + (1−q) ln((1−q)/(1−p)) ≥ q ln(1/p) − ln 2. (d) Non-solutions carry weight at most 2^n · 2^(−(n+2)) = 1/4 against at least 1 for the solutions. ∎

**Instant quench.** For T = 1 the identity in (a) reads ⟨exp(−W)⟩ = Σ_k N_k exp(−β_1 k) / 2^n. With T4 this makes the Jarzynski average a #P-hard number: the rare trajectories that dominate it are the solutions.

**Corollary [C]. A computational second law, conditional on NP ≠ RP.** If NP ≠ RP, then for every family of polynomial-length protocols with polynomial-time kernels and every constant c, there are satisfiable instances on which ⟨Σ⟩_R > c ln n.

*Proof.* Otherwise (c) and (d) give p ≥ n^(−5c/4) / 2^(5/4) on all satisfiable instances. Polynomially many repetitions then put SAT in RP. ∎

What T7 does and does not give: near-reversible annealing finds solutions (b), and success probability is controlled by the reverse entropy production (c). Neither statement bounds ⟨Σ⟩ from below without assuming NP ≠ RP. See N3.

---

## 5. Universality and fusion symmetry

**T8 [T]. Sectors inherit fusions, and conversely.**

(a) Every sector of L is invariant under every fusion symmetry of L.

(b) Established (Geiger; Bodnarchuk, Kaluzhnin, Kotov and Romov): every relation invariant under all fusion symmetries of L is a sector of L.

*Proof of (a).* Let y^1, …, y^k lie in the sector, with hidden completions z^1, …, z^k of zero action. Each constraint relation is closed under f, so (f(y), f(z)) violates no constraint, and f(y) is in the sector. ∎

So contraction and fusion symmetry are dual: the set of sectors reachable from a parent is exactly the set of relations its fusion symmetries preserve.

**T9 [T]. Dichotomy.** For a Boolean language L (pins included), exactly one of the following holds.

(i) L has one of the fusions AND, OR, MAJ, MIN. Then L is not contraction-universal and ZERO(L) is in P.

(ii) L has none of them. Then L is contraction-universal and ZERO(L) is NP-complete.

*Proof.* (i) AND-closed relations are Horn-definable and solved by unit propagation; OR is the dual case; MAJ-closed relations are 2-CNF-definable; MIN-closed relations are affine over GF(2) and solved by Gaussian elimination. By T8(a) the 1-in-3 relation, which has none of the four fusions, is not a sector. (ii) The fusion symmetries of L are closed under composition and idempotent. An idempotent composition-closed set of Boolean operations containing a non-projection contains one of the four basic fusions (established, Post). So L has only projections, and by T8(b) every relation is a sector. In particular the eight 3-clause relations are sectors with fixed-size gadgets, which reduces 3-SAT to ZERO(L). ∎

This is Schaefer's dichotomy theorem stated in the vocabulary of contraction.

**T10 [T]. Universality forces hardness, with an explicit universal parent.** Let R be the 1-in-3 relation. The language {R, pins, equality} is contraction-universal, and ZERO for it is NP-complete. Consequently:

    P = NP  if and only if  one (equivalently every) contraction-universal parent has a polynomial-time selector.

*Proof without T8(b).* Negation: x' = ¬x is the sector ∃f [ f = 0 and R(x, x', f) ]. Clause: (x ∨ y ∨ z) is the sector ∃a,b,c,d [ R(¬x, a, b) and R(b, y, c) and R(c, d, ¬z) ]. Other sign patterns follow by negation. Longer clauses split as (ℓ_1 ∨ … ∨ ℓ_k) = ∃u [ (ℓ_1 ∨ ℓ_2 ∨ u) and (¬u ∨ ℓ_3 ∨ … ∨ ℓ_k) ]. Every relation is the conjunction of the clauses that exclude its non-members. Both gadgets were verified by enumeration (§9). ∎

**Consequence for Axiom 3.1.** Axiom 3.1 asks for one parent whose contractions yield every sector functional. In the regulated Boolean model that requirement is contraction-universality. By T9 and T10 it is the same property as having no fusion symmetry, and it makes the selection principle (8) NP-complete. A parent simple enough to have a provably efficient selector is, by T9(i), too symmetric to produce all sectors.

**Weighted actions (established, Thapper–Živný).** For finite-valued local actions the tractable class is characterized by a fractional fusion inequality, of which submodularity, S(x ∧ y) + S(x ∨ y) ≤ S(x) + S(y), is the basic case. It holds exactly when the linear program over locally consistent marginals is exact; otherwise the problem is NP-hard. So the convexity that makes selection tractable is a property of the action on replicated histories. It is not the convexity of Γ, which always holds. The local-versus-global gap is the gap in §3.4 between local specifications and a global measure.

---

## 6. Closed routes

### Route A: P ≠ NP from monotonicity, data processing or the second law

**N1 [T]. Law invariance.** Ψ and Γ depend on a theory only through the law of O under Π. For a formula φ with violation counts N_0, …, N_M, define the twin theory T'_φ: uniform Π on {0,1}^n and O'(x) = least k such that the integer value of x is below N_0 + … + N_k. Then T_φ and T'_φ have the same law of observables, hence identical Ψ and Γ, but 0^n minimizes O' for every instance. So no condition on the law of the observables — no inequality among entropies, rate functions, cumulants or fluctuation statistics — implies that selection is hard. The computational content lies in the map φ ↦ (N_0, …, N_M), which is #P-hard by T4 and is not an object of the framework.

**N2 [T]. Relativization.** Allow O to query an oracle A. T1–T7 hold verbatim relative to every A, because their proofs use only identities valid for arbitrary measures and generic simulations. FIN relative to A is complete for NP relative to A: for a verifier R^A(w, y), take histories y, observable 1 − R^A(w, y) and o = 0. There is an oracle A with P^A = NP^A and an oracle B with P^B ≠ NP^B (established, Baker–Gill–Solovay). So no argument valid for arbitrary (Π, O) decides whether FIN is in P. A proof must use the locality of the action in a way that fails for oracle observables.

**N3 [T]. Thermodynamic blindness.** Every computation of time T and space S has a logically reversible simulation of time O(T^(1+ε)) and space O(S log T) (established, Bennett). A logically reversible computation has no positive lower bound on dissipation. So the minimal entropy production for computing X*(w) is zero whether or not P = NP, polynomial time stays polynomial under reversibility, and bounds such as eq. (96) constrain erasure, not time. The inequality ⟨Σ⟩ ≥ 0 cannot yield a time lower bound.

### Route B: P = NP from convexity

**N4 [T]. Duality circularity.** Let Ψ_∞[J] = lim Ψ[λJ] / λ as λ → ∞. Then Ψ_∞[J] = max_x ⟨J, O(x)⟩, the support function of M_w. Deciding Ψ_∞[J] ≥ t is NP-complete (take T_φ, J = −1, t = 0). Membership in M_w and evaluation of Ψ_∞ are polynomially equivalent (established, Grötschel–Lovász–Schrijver). The Legendre transform therefore maps one NP-hard problem onto another. Convexity of Γ supplies no algorithm, because neither Γ nor its domain has an efficient oracle.

**N5 [T, established]. No small convex parent.** For pairwise observables O(x) = (x_i x_j), M is the correlation polytope. It is not the linear image of any polytope with fewer than 2^(Ω(n)) facets (Fiorini, Massar, Pokutta, Tiwary and de Wolf), and no polynomial-size semidefinite lift exists either (Lee, Raghavendra and Steurer). In framework terms: dom Γ is not the linear contraction of any polynomial-size convex parent. This closes the route unconditionally. It does not prove P ≠ NP, because the matching polytope has the same property (Rothvoss) although matching is in P.

### Route C: P = NP from flows and relaxation

**N6 [T].** By D4, regulated flows are causal theories and causal theories are exactly randomized polynomial-time computations. "Some flow reaches X* in polynomial time" is therefore the statement that SEL is in randomized polynomial time: the question restated. A Lyapunov functional guarantees only a stationary point. Finding a stationary point of a descent process is in the class CLS (established), which is NP-hard only if NP = coNP. The monotone quantities of v3.0 — ν_GYM along the flow of §10, relative entropy under restriction — supply local selection, not the global minimum in (8).

### Route D: P ≠ NP from landscape geometry

**N7 [T]. The affine counterexample.** Take parity-check actions S(x) = number of violated checks of an expander low-density parity-check code (established existence, Sipser–Spielman): each check involves a bounded number of bits, the code has 2^(Ω(n)) codewords at pairwise distance above αn, and any x within distance αn of a codeword c violates at least (γ/2)·dist(x, c) checks. Then:

- there are 2^(Ω(n)) ground histories, pairwise Ω(n) apart;
- every single-flip path between two of them crosses action at least γαn/4;
- for β above a constant, any single-flip reversible dynamics has relaxation time exp(Ω(n)), by the bottleneck bound on the Hamming ball of radius αn/2;
- yet ZERO is in P, because the language has the MIN fusion and Gaussian elimination applies.

So every hardness criterion built from cluster separation, barrier height, mixing time or the entropy production of local dynamics is satisfied by a polynomial-time family. Landscape geometry cannot prove hardness. By T9 the property that actually separates this family from 3-SAT is the fusion symmetry MIN, which no entropic or geometric functional of v3.0 detects.

### Route E: the gravitational sector

The complexity–geometry relations (decoding cost exponential in a generalized-entropy difference, complexity as volume) are type [P]. A chain containing a [P] arrow is not a proof. They are consistent with RS and assume statements at least as strong.

---

## 7. Residual statement

**RS [O].** For the universal parent of T10, no deterministic causal theory of polynomial size compiles the terminal condition: there is no polynomial-time support selector σ as in T6(a).

By T6(a) and T10, RS is equivalent to P ≠ NP. Its negation is equivalent to P = NP.

**Necessary conditions on any proof of RS.**

| | Requirement | Source |
|---|---|---|
| R1 | Must use locality of the action in a way that fails for oracle observables | N2 |
| R2 | Must depend on more than the law of the observables | N1 |
| R3 | Must distinguish 3-SAT from parity constraints, that is, must use the absence of fusion symmetry | T9, N7 |
| R4 | Must not rest on a property that is efficiently checkable and holds for most actions, unless pseudorandom functions do not exist | established, Razborov–Rudich |
| R5 | Must not survive algebraic extension of oracles | established, Aaronson–Wigderson |

**Status of the framework's tools against R1–R5.**

| Tool of v3.0 | Fails |
|---|---|
| Data processing, relative-entropy monotonicity | R1, R2 |
| Convex duality, contraction principle | R1, R2 (N4), and N5 for polynomial-size linear or semidefinite parents |
| Fluctuation relations, second law | R1, R2, and N3 |
| Lyapunov monotonicity of flows | R3 (N6, N7) |
| Gibbs consistency, local specifications | R3: exact for fusion-symmetric actions only |

No theorem-grade tool of v3.0 meets R1–R3 together, so the framework as it stands can prove neither RS nor its negation.

**What would have to be added.** The only object introduced here that meets R3 is the fusion-symmetry ledger of §5. T9 shows the tractability boundary is algebraic: it is fixed by which coordinatewise operations preserve the ground set. A proof of RS would have to show that the absence of fusion symmetry rules out every polynomial-time selector, not only those built from the fusion. That implication is currently known only as an equivalence with RS itself. In the algebraic analogue, where the question is whether the generator of an interacting local theory can be written as a polynomial-size determinant (a free-field representation), the best unconditional lower bound is quadratic (established, Mignon–Ressayre).

**Typing if the framework adopts the statement.** RS can enter Universal Mechanics only as an axiom:

> **Axiom C [A] — no compilation of terminal conditions.** No polynomial-size causal theory compiles the terminal conditioning of a contraction-universal parent.

Consequences already proved from it: FIN, SEL and the support selector are not polynomial (T2, T3, T6a); assuming also P = BPP, the tilt (35) is not realizable by any causal theory (T6b) and every polynomial annealing family has reverse entropy production growing faster than log n on some instances (T7 corollary). Under Axiom C the grand reading of §18.1 cannot be realized by relaxation; selection must come from the tilt, which is conditioning and not dynamics.

---

## 8. Typed chain for the sector

    regulated local theory (S_w, O_w) [D]  ⟹  Ψ_w, Γ_w [D]
    Γ_w[o] finite  ⟺  o ∈ conv O_w(H_w) [T];   Γ_φ[0] = n ln 2 − ln #SAT(φ) [T]
    FIN NP-complete [T];   SEL ≡ NP search [T];   GEN #P-hard [T]
    P = NP  ⟺  FIN ∈ P  ⟺  SEL polynomial  ⟺  Doob support selector exists
            ⟺  a universal parent has a polynomial selector [T]
    NP = RP  ⟺  the tilt (35) compiles into a causal theory [T]
    contraction-universal  ⟺  no fusion symmetry [T, established]  ⟹  NP-complete selection [T]
    fusion symmetry  ⟹  polynomial selection and non-universality [T]
    ⟨Σ⟩_F small  ⟹  search succeeds [T];   NP ≠ RP  ⟹  ⟨Σ⟩_R not O(log n) [C]
    data processing, duality, fluctuation relations, Lyapunov monotonicity
            decide neither FIN ∈ P nor FIN ∉ P [T: N1–N7]
    RS [O];   Axiom C [A] if adopted

---

## 9. Finite verification

Script: `verify.py` in this directory (numpy only, exact enumeration). All checks pass.

| Claim | Check | Result |
|---|---|---|
| T2 | Γ_φ[0] versus n ln 2 − ln #SAT on random 3-CNF, n = 8 to 12 | Agreement to 6 decimals on all four instances |
| T4 | #SAT recovered from one evaluation of Ψ | 9, 8, 4, 1 recovered exactly |
| T5 | Doob kernel product on every solution, n = 10 | Law equals 1/#SAT exactly; total mass 1 |
| T7(a) | ⟨exp(−Σ)⟩ on exact path measures, T = 1 to 1024 | 1.0000000000 in every case |
| T7(b), (c) | Both inequalities over 18 Metropolis protocols, n = 8 | Minimum slack 0.517 and 0.971, both nonnegative |
| T9 | Fusions of each language | 3-SAT none; 1-in-3 none; XOR has MIN; Horn has AND; 2-clause has MAJ |
| T10 | Negation and 3-clause gadgets from 1-in-3 | Both correct on all inputs |
| T8 | Three-variable sectors reachable by contraction, against relations invariant under the fusion | 1-in-3: 256 of 256. XOR: 52 against 52. Horn: 122 against 122. 2-clause: 166 against 166 |

The T8 check uses a four-variable workspace, so one hidden variable is available at a time. Within that limit the reachable sets coincide exactly with the invariant sets.

Dissipation data for one instance (n = 8, linear schedule, q = 0.995):

| Steps T | ⟨Σ⟩_F | ⟨Σ⟩_R | Success probability p |
|---|---|---|---|
| 1 | 21.15 | 4.81 | 0.015 |
| 16 | 10.02 | 3.89 | 0.214 |
| 64 | 4.84 | 2.46 | 0.488 |
| 256 | 2.23 | 1.16 | 0.673 |
| 1024 | 0.87 | 0.46 | 0.854 |

---

## 10. Established results used without proof

Cited from memory; verify before reuse.

- Cook 1971, Levin 1973: NP-completeness of satisfiability. Lichtenstein 1982: planar 3-SAT.
- Carathéodory's theorem; Fenchel–Moreau theorem; Gibbs variational principle; Pinsker's inequality.
- Khachiyan 1979: linear programming in polynomial time.
- Valiant 1979: #P-completeness of counting satisfying assignments.
- Stockmeyer 1983: approximate counting with an NP oracle. Jerrum, Valiant and Vazirani 1986: generation reduces to approximate counting. Ko 1982: NP ⊆ BPP implies NP = RP.
- Post 1941: lattice of Boolean clones. Geiger 1968; Bodnarchuk, Kaluzhnin, Kotov and Romov 1969: Galois correspondence between operations and relations. Schaefer 1978: dichotomy for Boolean constraint satisfaction.
- Thapper and Živný 2016: complexity of finite-valued constraint satisfaction.
- Baker, Gill and Solovay 1975: relativization. Razborov and Rudich 1997: natural proofs. Aaronson and Wigderson 2009: algebrization.
- Bennett 1973, 1989: reversible simulation and its time–space cost.
- Grötschel, Lovász and Schrijver 1981: equivalence of separation and optimization.
- Fiorini, Massar, Pokutta, Tiwary and de Wolf 2012: extension complexity of the correlation polytope. Lee, Raghavendra and Steurer 2015: semidefinite lifts. Rothvoss 2014: matching polytope.
- Megiddo and Papadimitriou 1991: total search problems are NP-hard only if NP = coNP. Fearnley, Goldberg, Hollender and Savani 2021: complexity of gradient descent.
- Sipser and Spielman 1996: expander codes.
- Mignon and Ressayre 2004: quadratic lower bound on the determinantal complexity of the permanent.
- Crooks 1999, Jarzynski 1997: references [36], [37] of v3.0.
