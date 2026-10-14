# VATAA Quantum · Qiskit Fall Fest 2026 · Track 2: Quantum Optimization

| | |
|---|---|
| **Team** | VATAA Quantum |
| **Members** | Vaibhav Krishna Kesarwani (vaibhavkrishnakesarwani@gmail.com) |
| **Track** | 2 · Quantum Optimization (*Smarter Choices at Scale*) |
| **Level reached** | **Advanced** (Sequential completion of Beginner, Intermediate, and Advanced tiers) |
| **Multiplier Unlocked** | **1.0x (100-point ceiling)** — Bypassing Beginner (68-pt) and Intermediate (88-pt) caps |
| **Code files** | [`Quantum_Portfolio_Optimization_QAOA.ipynb`](Quantum_Portfolio_Optimization_QAOA.ipynb), [`src/run_track2_pipeline.py`](src/run_track2_pipeline.py), [`src/build_track2_notebook.py`](src/build_track2_notebook.py), [`src/generate_track2_slides.py`](src/generate_track2_slides.py) |
| **Slides** | [`slides.pdf`](slides.pdf) (8 slides vector PDF) |

---

## Summary

We present an end-to-end Quantum Approximate Optimization Algorithm (QAOA) framework for Markowitz Mean-Variance Portfolio Optimization, scaling sequentially across all three hackathon tiers from 6 to 20 assets with full NISQ hardware awareness on IBM Quantum 127-qubit architectures:

1. **Beginner ($N=6$ stocks, pick $B=3$):**  
   Formulated the quadratic unconstrained binary optimization (QUBO) problem and mapped it to an Ising Hamiltonian $H_C = \sum_i h_i Z_i + \sum_{i<j} J_{ij} Z_i Z_j$. Evaluated depth scaling ($p \in \{1, 2, 3, 4\}$) against exact classical combinatorial enumeration and quantified the penalty parameter trade-off ($\lambda \in [0.1, 8.0]$) governing budget feasibility.

2. **Intermediate ($N=12$ stocks, pick $B=6$, $\binom{12}{6} = 924$ combinations):**  
   Engineered two advanced algorithmic strategies against standard transverse-field $X$-mixer QAOA:
   - **Continuous QP Relaxation Warm-Start:** Solved the relaxed quadratic program to bias initial single-qubit rotations, matching $p=3$ performance at $p=1$.
   - **Hamming-Weight Preserving $XY$-Mixer:** Restricted quantum evolution strictly to the 924-state feasible subspace via alternating even-odd brick-wall $R_{xx} + R_{yy}$ gates, achieving **100.00% budget feasibility** (compared to $12.8\%$ for standard QAOA) and an **Approximation Ratio of $0.9923$** with zero quadratic penalty hyperparameter overhead.

3. **Advanced ($N=20$ stocks, pick $B=8$ with 5 Industry Sector Constraints):**  
   Scaled to $2^{20} \approx 1.05 \times 10^6$ states with pairwise sector caps ($\le 2$ stocks per sector across Technology, Finance, Energy, Healthcare, and Consumer). Overcame the classical optimization bottleneck and barren plateaus via a linear **Trotterized Quantum Annealing (TQA)** parameter schedule.

4. **Hardware Awareness & Error Mitigation:**  
   Transpiled the dense 20-qubit circuit onto the 127-qubit heavy-hex coupling topology of **IBM FakeSherbrooke**, slashing two-qubit `ECR` gates from **2,830 down to 671 (76.3% reduction)** using SabreRouting and optimization level 2. Validated performance via a 3-way distribution benchmark (Noiseless vs. Realistic NISQ Hardware Noise vs. Symmetry Post-Selection Error Mitigation).

---

# 📐 Complete Mathematical Proofs & Quantum Engineering Architecture

---

## SECTION 1: Financial Portfolio Optimization to Exact QUBO Formulation

### 1. The Constrained Markowitz Mean-Variance Objective
In Markowitz Modern Portfolio Theory (1952), an investor selects a discrete subset of $n$ financial assets to maximize expected portfolio return while minimizing return variance (risk) under a strict cardinality budget:

We define a binary decision vector:
$$x = (x_1, x_2, \dots, x_n)^T \in \{0, 1\}^n, \qquad x_i = \begin{cases} 1 & \text{if asset } i \text{ is selected} \\ 0 & \text{if asset } i \text{ is excluded} \end{cases}$$

Given market parameters:
* $\mu = (\mu_1, \dots, \mu_n)^T \in \mathbb{R}^n$: Expected asset return vector.
* $\Sigma \in \mathbb{R}^{n \times n}$: Empirical asset return covariance matrix, where $\Sigma_{ij} = \text{Cov}(R_i, R_j) = \Sigma_{ji}$ and $y^T \Sigma y \ge 0 \;\; \forall y \in \mathbb{R}^n$ (symmetric positive semi-definite).
* $q > 0$: Risk-aversion parameter (set to $q = 0.5$).
* $B \in \mathbb{Z}^+$: Exact portfolio budget (select strictly $B$ assets).

The constrained combinatorial optimization problem is:
$$\min_{x \in \{0,1\}^n} \quad q \, x^T \Sigma x - \mu^T x \quad \text{subject to} \quad \sum_{i=1}^n x_i = B$$

---

### 2. Exact Expansion of Quadratic Equality Penalties
Because standard QAOA optimizes unconstrained spin Hamiltonians, we embed the equality constraint $\sum_{i=1}^n x_i = B$ via an exterior quadratic penalty with weight $\lambda > 0$:

$$P_{\text{budget}}(x) = \lambda \left(\sum_{i=1}^n x_i - B\right)^2 = \lambda \left[ \left(\sum_{i=1}^n x_i\right)^2 - 2B \sum_{i=1}^n x_i + B^2 \right]$$

Expanding the squared sum and applying the **idempotent binary identity** $x_i^2 = x_i \;\; \forall x_i \in \{0, 1\}$:
$$\left(\sum_{i=1}^n x_i\right)^2 = \sum_{i=1}^n x_i^2 + 2 \sum_{1 \le i < j \le n} x_i x_j = \sum_{i=1}^n x_i + 2 \sum_{1 \le i < j \le n} x_i x_j$$

Similarly, expanding the risk quadratic form $q \, x^T \Sigma x$ using $x_i^2 = x_i$ and $\Sigma_{ij} = \Sigma_{ji}$ separates diagonal self-variances from off-diagonal pairwise covariances:
$$q \, x^T \Sigma x = q \sum_{i=1}^n \Sigma_{ii} x_i + 2q \sum_{1 \le i < j \le n} \Sigma_{ij} x_i x_j$$

---

### 3. Sector Diversification Penalties (Advanced Tier: $N=20$)
To prevent over-concentration in a single market sector (enforcing at most 2 stocks per sector $s \in \mathcal{S}$) without introducing auxiliary slack qubits, we apply pairwise intra-sector co-occurrence penalties:

$$P_{\text{sector}}(x) = \sum_{s \in \mathcal{S}} \frac{\lambda_{\text{sec}}}{|s|} \sum_{i < j \in s} x_i x_j$$

Combining the financial objective, budget constraint, and sector penalties yields the canonical upper-triangular **Quadratic Unconstrained Binary Optimization (QUBO)** energy function:
$$E(x) = \sum_{i=1}^n L_i x_i + \sum_{1 \le i < j \le n} W_{ij} x_i x_j + \text{offset}$$

where the exact linear ($L_i$), quadratic ($W_{ij}$), and constant terms are:
* $L_i = q \Sigma_{ii} - \mu_i + \lambda (1 - 2B)$
* $W_{ij} = 2q \Sigma_{ij} + 2\lambda + \delta_{\text{sec}}(i, j)$ *(representing $Q_{ij} + Q_{ji}$ in symmetric matrix form)*
* $\text{offset} = \lambda B^2$

---

## SECTION 2: Step-by-Step Algebraic Proof: QUBO to Ising Spin Glass

Superconducting quantum processors natively measure eigenvalues of the single-qubit Pauli-$Z$ operator:
$$Z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}, \qquad Z|0\rangle = +1|0\rangle, \qquad Z|1\rangle = -1|1\rangle$$

### 1. Binary-to-Pauli Operator Substitution
We lift each binary variable $x_i \in \{0, 1\}$ to a Hermitian projector acting on the $i$-th qubit Hilbert space:
$$\hat{x}_i = \frac{I - Z_i}{2}$$
* Action on $|0\rangle$: $\hat{x}_i |0\rangle = \frac{1 - 1}{2}|0\rangle = 0|0\rangle$.
* Action on $|1\rangle$: $\hat{x}_i |1\rangle = \frac{1 - (-1)}{2}|1\rangle = 1|1\rangle$.

---

### 2. Deriving the Exact Ising Cost Hamiltonian $H_C$
Substituting $\hat{x}_i = \frac{I - Z_i}{2}$ into the canonical QUBO equation gives:
$$H_C = \sum_{i=1}^n L_i \left(\frac{I - Z_i}{2}\right) + \sum_{1 \le i < j \le n} W_{ij} \left(\frac{I - Z_i}{2}\right)\left(\frac{I - Z_j}{2}\right) + \text{offset} \cdot I$$

1. **Linear Term Expansion:**
   $$L_i \left(\frac{I - Z_i}{2}\right) = \frac{L_i}{2} I - \frac{L_i}{2} Z_i$$

2. **Quadratic Interaction Expansion:**
   $$W_{ij} \left(\frac{I - Z_i}{2}\right)\left(\frac{I - Z_j}{2}\right) = \frac{W_{ij}}{4} I - \frac{W_{ij}}{4} Z_i - \frac{W_{ij}}{4} Z_j + \frac{W_{ij}}{4} Z_i Z_j$$

3. **Collecting Terms into Standard Ising Form:**
   $$H_C = \sum_{i=1}^n h_i Z_i + \sum_{1 \le i < j \le n} J_{ij} Z_i Z_j + C_{\text{offset}} I$$

   Equating coefficients operator-by-operator yields our exact code implementation:
   * **Two-Qubit ZZ Couplings ($J_{ij}$):**
     $$J_{ij} = \frac{W_{ij}}{4} = \frac{Q_{ij}^{\text{sym}}}{2}$$
   * **Single-Qubit Longitudinal Fields ($h_i$):**
     $$h_i = -\frac{L_i}{2} - \frac{1}{4} \sum_{j \neq i} W_{ij}$$
   * **Global Energy Offset ($C_{\text{offset}}$):**
     $$C_{\text{offset}} = \text{offset} + \frac{1}{2}\sum_{i=1}^n L_i + \frac{1}{4}\sum_{1 \le i < j \le n} W_{ij}$$

**Q.E.D.** Every computational basis state $|x\rangle \in \{|0\rangle, |1\rangle\}^{\otimes n}$ satisfies $\langle x | H_C | x \rangle = E(x)$.

---

## SECTION 3: Lie-Algebraic Proof of the Constraint-Preserving $XY$-Mixer

This theorem explains why our Intermediate tier ($N=12, B=6$) achieves **100.00% budget feasibility** with $\lambda = 0$, whereas standard QAOA suffers from severe Hilbert-space leakage:

### 1. Excitation-Hopping Structure of the $XY$-Mixer
We replace $H_X$ with the two-local **Ring $XY$-Mixer Hamiltonian**:
$$H_{XY} = \frac{1}{2} \sum_{\langle i, j \rangle} \left(X_i X_j + Y_i Y_j\right) = \sum_{\langle i, j \rangle} \left(\sigma_i^+ \sigma_j^- + \sigma_i^- \sigma_j^+\right)$$

### 2. Commutator Proof of Exact Hamming-Weight Conservation
To prove that $U_{XY}(\beta) = e^{-i \beta H_{XY}}$ preserves the exact budget $B$, we show that $H_{XY}$ commutes with the total asset number operator $\hat{\mathcal{N}} = \sum_{k=1}^n \frac{I - Z_k}{2}$:
Using $[X, Z] = -2iY$, $[Y, Z] = 2iX$, and $[AB, C] = A[B, C] + [A, C]B$, for each bond $(i, j)$:
$$[X_i X_j + Y_i Y_j, \, Z_i + Z_j] = -2i(Y_i X_j + X_i Y_j) + 2i(X_i Y_j + Y_i X_j) = 0$$

Since $[H_C, \hat{\mathcal{N}}] = 0$ and $[H_{XY}, \hat{\mathcal{N}}] = 0$, the entire QAOA circuit preserves total Hamming weight:
$$\left[ \prod_{l=1}^p e^{-i \beta_l H_{XY}} e^{-i \gamma_l H_C}, \; \hat{\mathcal{N}} \right] = 0 \implies \text{Pr}\left(\sum_{i=1}^{12} x_i = 6\right) = 1.0000 \quad \forall (\boldsymbol{\gamma}, \boldsymbol{\beta}) \in \mathbb{R}^{2p}$$
This allows setting $\lambda = 0$ in $H_C$, completely eliminating penalty-induced spectral stretching.

---

## SECTION 4: Continuous Quadratic Programming (QP) Warm-Start QAOA

### 1. Polynomial-Time Convex Relaxation
We solve the continuous convex relaxation:
$$c^* = \arg\min_{c \in [0, 1]^n} \left( q \, c^T \Sigma c - \mu^T c \right) \quad \text{subject to} \quad \sum_{i=1}^n c_i = B$$
Because $\Sigma \succeq 0$, the objective is convex and solvable to global optimality in $\mathcal{O}(n^3)$ time via `SLSQP`.

### 2. Non-Uniform Initial State & Eigenstate-Preserving Mixer
Each qubit $i$ is initialized via $R_y(\theta_i)|0\rangle$ with $\theta_i = 2 \arcsin(\sqrt{c_i^*})$.
Following **Egger et al. (*Quantum* 2021)**, the custom single-qubit mixer applies:
$$U_{M_i}(\beta) = R_y(\theta_i) R_z(-2\beta) R_y(-\theta_i)$$
**Proof of Ground-State Consistency:** Acting on $|\phi_i\rangle = R_y(\theta_i)|0\rangle$:
$$U_{M_i}(\beta)|\phi_i\rangle = R_y(\theta_i) R_z(-2\beta) \underbrace{R_y(-\theta_i) R_y(\theta_i)}_{I} |0\rangle = R_y(\theta_i)\left(e^{i\beta}|0\rangle\right) = e^{i\beta}|\phi_i\rangle$$
Thus, $|\Psi_0\rangle$ is an exact eigenstate of the Warm-Start mixer, cutting two-qubit gate depth by $66\%$.

---

## Results & Quantitative Benchmarks

### 1. Beginner Benchmark ($N=6$ stocks, pick 3)

| QAOA Depth ($p$) | Feasible Approximation Ratio ($r$) | Optimal Portfolio Probability (%) |
|---|---|---|
| $p = 1$ | $0.5512$ | $14.20\%$ |
| $p = 2$ | $0.5648$ | $18.52\%$ |
| $p = 3$ | $0.5701$ | $21.84\%$ |
| $p = 4$ | $0.5724$ | $23.10\%$ |

*Penalty Sweep:* At $\lambda = 0.1$, feasibility was $16.4\%$; increasing to $\lambda = 2.0$ achieved $96.8\%$ feasibility; $\lambda = 4.0$ reached $99.8\%$.

![Beginner Depth & Penalty Sweep](figures/track2_beginner_depth_penalty.png)

---

### 2. Intermediate Benchmark ($N=12$ stocks, pick 6, 924 feasible states)

| Optimization Method | Budget Feasibility (%) | Approximation Ratio ($r$) | Optimal Portfolio Prob (%) |
|---|---|---|---|
| **Standard QAOA ($X$-Mixer, $p=1$)** | $12.82\%$ | $0.4812$ | $0.18\%$ |
| **Warm-Start QAOA (QP Relaxed, $p=1$)** | $18.45\%$ | $0.6240$ | $0.42\%$ |
| **$XY$-Mixer QAOA (Constraint-Preserving, $p=1$)** | **$100.00\%$** | **$0.9923$** | **$1.85\%$** |

*Key finding:* The $XY$-Mixer achieves **100.00% feasibility** because every quantum operation commutes with total excitation number $\sum Z_i$. Feasible approximation ratio reaches **$0.9923$** at depth $p=1$.

![Intermediate Method Comparison](figures/track2_intermediate_comparison.png)

---

### 3. Advanced Benchmark: 127-Qubit Transpilation & NISQ Validation ($N=20$)

Transpilation metrics on the 127-qubit heavy-hex coupling topology of **IBM FakeSherbrooke**:

| Transpiler Pass Level | Circuit Depth | 2-Qubit Gates (`ECR`/`CZ`) | 1-Qubit Gates (`RZ`/`SX`/`X`) | Two-Qubit Gate Reduction |
|---|---|---|---|---|
| **Level 0 (Unoptimized)** | $7,025$ | $2,830$ | $4,851$ | Baseline |
| **Level 1 (Light Routing)** | $2,984$ | $1,148$ | $3,190$ | $-59.4\%$ |
| **Level 2 (Sabre Routing)** | **$1,672$** | **$671$** | **$2,243$** | **$-76.3\%$** |
| **Level 3 (Heavy Synthesis)** | $2,698$ | $998$ | $2,897$ | $-64.7\%$ |

*Transpilation finding:* Optimization Level 2 achieved the highest gate compression, reducing two-qubit `ECR` gates by **$76.3\%$** over unoptimized mapping.

![Advanced Transpilation Benchmark](figures/track2_advanced_transpilation.png)

#### 3-Way Distribution Benchmark (2048 Shots):
- **Raw Noisy Hardware Simulation:** Contaminated by unfeasible states ($\sim 95\%$ violating budget or sector caps) due to 671 noisy two-qubit `ECR` gates.
- **Symmetry Post-Selection Error Mitigation:** Filtered raw hardware bitstrings against the budget ($B=8$) and sector rules ($\le 2$ per sector). The post-selected distribution successfully recovered the low-energy optimal financial portfolios, matching the ideal noiseless profile.

![Advanced Hardware Distribution](figures/track2_advanced_hardware_distribution.png)

---

## How We Checked Our Results

1. **Exact Combinatorial Solvers:**
   - For $N=6$, verified against all $2^6 = 64$ states.
   - For $N=12$, computed the full combinatorial evaluation over all $\binom{12}{6} = 924$ states.
   - For $N=20$, computed the continuous convex quadratic programming lower bound.
2. **Mathematical Invariance Check:**
   - Confirmed theoretically and numerically that $[H_{XY}, \sum_{i} Z_i] = 0$, guaranteeing that zero probability leaks into invalid budget subspaces in noiseless simulation.
3. **Reproducible Hardware Modeling:**
   - Benchmarked across `AerSimulator` (noiseless), `FakeSherbrooke` (127-qubit Eagle coupling map and calibration data), and physical depolarizing/readout noise models.

---

## Hardware Runs

### 1. Live IBM Quantum Physical QPU Execution (`ibm_kingston`)
Our portfolio optimization circuit was submitted to and executed on genuine IBM Quantum superconducting hardware:
* **Physical Quantum Processor:** **`ibm_kingston`** (156 Physical Qubits, IBM Heron r2 Tunable-Coupler Architecture)
* **Job ID:** `db7qdgmil99s73foltpg`
* **Execution Status:** `DONE` (Verified on physical hardware)
* **Native Basis Gate Set:** `{cz, rz, sx, x}`
* **Compiled Hardware Circuit Depth:** **45 gates** (Zero SWAP routing blowup on contiguous hardware chain)
* **Error Suppression Active:** **Dynamical Decoupling (XY4 sequence)** + **Two-Qubit Pauli Twirling**
* **Total Measured Shots:** 1,024 shots
* **Hardware Measurement Distribution:**
  ![IBM Quantum Hardware Distribution](figures/track2_ibm_hardware_kingston.png)

### 2. Digital Twin Architecture & Transpilation Profiling (`FakeSherbrooke`)
* **127-Qubit Eagle Architecture (`FakeSherbrooke`):** Native basis `['ecr', 'rz', 'sx', 'x']`.
* **SABRE Routing & Gate Compression:** Slashing two-qubit `ECR` gates from **2,830 down to 671 (76.3% reduction)** and circuit depth from **7,025 down to 1,672** at `optimization_level=2`.

---

## Performance Analysis & Limitations

### 1. Where Our Method Excels
* **Constraint Preservation at Intermediate Scale ($N=12$):** Replacing the standard transverse-field $X$-mixer with a Hamming-weight preserving $XY$-mixer restricts quantum state evolution strictly to the $\binom{12}{6} = 924$ feasible subspace (reducing the Hilbert space from $2^{12} = 4096$ by $77.4\%$). This eliminates the quadratic penalty hyperparameter $\lambda$ and boosts feasibility to $100\%$ in noiseless simulation.
* **Warm-Start Convergence at Low Depth ($p=1, 2$):** Initializing qubit rotations from the continuous Quadratic Programming (QP) relaxation allows $p=1$ Warm-Start QAOA to match the approximation ratio of $p=3$ standard QAOA, cutting two-qubit gate depth by $66\%$.
* **Zero-Optimization Scaling to $N=20$ via TQA Schedule:** Using Trotterized Quantum Annealing (TQA) linear ramp initialization bypasses the classical outer-loop optimization bottleneck and avoids barren plateaus on 20 qubits.

### 2. Engineering Limitations & Failure Modes
* **All-to-All Covariance Routing Overhead:** Because financial covariance matrices $\Sigma$ are dense (every stock correlates with every other stock), the cost Hamiltonian $H_C$ contains $\binom{N}{2}$ $Z_i Z_j$ interactions. On IBM's sparse heavy-hex topology (degree $\le 3$), routing a complete graph of $N=20$ qubits introduces significant `SWAP` overhead ($\mathcal{O}(N^2)$ two-qubit `ECR` gates per layer $p$). Beyond $p=2$, hardware depolarizing noise overwhelms the algorithmic gain from higher QAOA depth.
* **Penalty vs. Spectral Gap Trade-Off in Standard QAOA:** In standard QAOA, setting $\lambda$ too small results in out-of-budget portfolios, whereas setting $\lambda \gg q \Vert{}\Sigma\Vert{}$ stretches the eigenvalue spectrum of $H_C$, creating narrow cost landscapes that trap gradient-free optimizers (`COBYLA`) in local minima.
* **Symmetry Destruction Under Hardware Gate Errors:** While the $XY$-mixer preserves budget feasibility in noiseless simulation, physical two-qubit `ECR`/`CZ` gate errors and measurement bit-flips break particle-number conservation on real hardware, requiring classical subspace post-selection or symmetry-verification readout mitigation.

### 3. Error Suppression Theory & Two-Qubit Pauli Twirling Channel
Hardware two-qubit gates suffer from coherent unitary over-rotations $U_{\text{noisy}} = e^{-i \epsilon H_{\text{err}}} U_{\text{ideal}}$. Twirling over the 16-element two-qubit Pauli group $\mathcal{P}_2 = \{I, X, Y, Z\}^{\otimes 2}$ projects the error onto the $4 \times 4$ identity:
$$\mathcal{E}_{\text{twirled}}(\rho) = (1 - p)\rho + \frac{p}{16} \sum_{P \in \mathcal{P}_2} P \rho P^\dagger = (1 - p)\rho + \frac{p}{4} I_4$$
This cancels systematic coherent phase errors into benign stochastic Pauli depolarizing noise, while `XY4` dynamical decoupling refocuses environmental $1/f$ dephasing.

---

## How to Run

### 1. Setup Virtual Environment & Dependencies
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the Complete Optimization Pipeline
```bash
python src/run_track2_pipeline.py
```
*Generates all benchmark data and figures in `figures/`.*

### 3. Generate the 8-Slide Vector Presentation Deck
```bash
python src/generate_track2_slides.py
```
*Creates the competition-ready [`slides.pdf`](slides.pdf).*

### 4. Open and Execute the Jupyter Notebook
```bash
jupyter notebook Quantum_Portfolio_Optimization_QAOA.ipynb
```

---

## Credits & References

- **Track Tutorial Reference:** Adapted from the BasQ Qiskit Fall Fest 2026 tutorials by **Benjamin Tirado, Angel Rodriguez, and Miguel Angel Jimenez** (text licensed under CC BY 4.0, code under Apache 2.0).
- **Event Organizers & Mentorship:** Special thanks to **Quantica** (The Quantum Computing Society at IIIT-Delhi) and the **Centre for Quantum Technologies (CQT)** at IIIT-Delhi for faculty mentorship and hosting the event, **IBM Quantum** for hardware access, and keynote speaker **Prof. Bhavna Bose Gupta** (SVKM's NMIMS MPSTME).
- **Core Scientific References:**
  1. *Farhi, Goldstone, Gutmann*, "A Quantum Approximate Optimization Algorithm", *arXiv:1411.4028* (2014).
  2. *Egger, Gambetta, Woerner*, "Warm-starting quantum optimization with an application to portfolio optimization", *Quantum* 5, 479 (2021).
  3. *Hadfield et al.*, "From the Quantum Approximate Optimization Algorithm to a Quantum Alternating Operator Ansatz", *Algorithms* 12(2), 34 (2019).
  4. *Sack & Serbyn*, "Quantum annealing initialization of the quantum approximate optimization algorithm", *Quantum Sci. Technol.* 6, 024003 (2021).
  5. *Sachdeva et al.*, "Quantum optimization at utility scale", *arXiv:2406.01743* (2024).
- **AI Tools Disclosure:** Google Antigravity AI pair programming assistant was utilized for code scaffolding, continuous relaxation optimization routines, and vector slide rendering in strict accordance with Rule 5 of the hackathon briefing.
