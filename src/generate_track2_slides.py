"""
Generates the 8-Slide Presentation Deck for Track 2 (Quantum Optimization - Advanced Level)
using Matplotlib's vector PDF backend (16:9 widescreen layout).
Produces 'slides_track2.pdf' and updates 'slides.pdf'.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as patches

SLIDE_W, SLIDE_H = 13.333, 7.5

def create_track2_slides():
    pdf_path = "slides.pdf"
    print(f"Generating Track 2 Advanced presentation slide deck: {pdf_path}...")
    
    with PdfPages(pdf_path) as pdf:
        def setup_slide(title: str, subtitle: str, slide_num: int):
            fig = plt.figure(figsize=(SLIDE_W, SLIDE_H), dpi=150)
            fig.patch.set_facecolor('#0a0e1a')
            ax = fig.add_axes([0, 0, 1, 1])
            ax.set_facecolor('#0a0e1a')
            ax.set_xlim(0, 100)
            ax.set_ylim(0, 100)
            ax.axis('off')
            
            # Header accent line
            rect = patches.Rectangle((0, 98.8), 100, 1.2, facecolor='#10b981', edgecolor='none')
            ax.add_patch(rect)
            
            # Slide Category Tag
            ax.text(5, 93.5, "QISKIT FALL FEST 2026 · TRACK 2: QUANTUM OPTIMIZATION · ADVANCED LEVEL", 
                    fontsize=9, fontweight='bold', color='#34d399')
            
            # Slide Title
            ax.text(5, 87.5, title, fontsize=21, fontweight='bold', color='#ffffff')
            ax.text(5, 83.2, subtitle, fontsize=11, color='#94a3b8')
            
            # Footer
            ax.text(5, 3.5, "Team VATAA Quantum · Track 2: Smarter Choices at Scale · IIIT-Delhi Hackathon", fontsize=9, color='#64748b')
            ax.text(93, 3.5, f"Slide {slide_num} / 8", fontsize=9, fontweight='bold', color='#64748b')
            return fig, ax

        # =============================================================
        # SLIDE 1: Title & Executive Summary
        # =============================================================
        fig = plt.figure(figsize=(SLIDE_W, SLIDE_H), dpi=150)
        fig.patch.set_facecolor('#0a0e1a')
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_facecolor('#0a0e1a')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis('off')
        
        ax.add_patch(patches.Rectangle((0, 98.8), 100, 1.2, facecolor='#10b981', edgecolor='none'))
        ax.text(7, 85, "QISKIT FALL FEST 2026 · TRACK 2 SUBMISSION ENTRY", fontsize=11, fontweight='bold', color='#34d399')
        ax.text(7, 76, "Quantum Portfolio Optimization at Scale", fontsize=27, fontweight='heavy', color='#ffffff')
        ax.text(7, 69.5, "From 6 to 20 Stocks: Warm-Start QAOA, XY-Mixers & 127-Qubit Hardware Routing", fontsize=15, color='#94a3b8')
        
        # Metadata Card
        c1 = patches.FancyBboxPatch((7, 43), 40, 21, boxstyle="round,pad=0.8", facecolor='#131d31', edgecolor='#10b981', linewidth=1.2)
        ax.add_patch(c1)
        ax.text(9, 60, "SUBMISSION METADATA", fontsize=10, fontweight='bold', color='#34d399')
        ax.text(9, 55, "• Team: VATAA Quantum", fontsize=11, fontweight='bold', color='#f8fafc')
        ax.text(9, 51, "• Track: Track 2 — Quantum Optimization (*Smarter Choices*)", fontsize=10.5, color='#cbd5e1')
        ax.text(9, 47, "• Level Reached: ADVANCED LEVEL (100-Point Tier)", fontsize=10.5, color='#38bdf8', fontweight='bold')
        
        # Summary Card
        c2 = patches.FancyBboxPatch((50, 20), 43, 44, boxstyle="round,pad=0.8", facecolor='#131d31', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c2)
        ax.text(52, 60, "EXECUTIVE SUMMARY & HEADLINE RESULTS", fontsize=11, fontweight='bold', color='#34d399')
        
        bullets = [
            ("1. Full Three-Tier Execution:", "Sequentially completed Beginner (6 stocks), Intermediate (12 stocks), and Advanced (20 stocks with 5 sector constraints)."),
            ("2. 100% Budget Compliance via XY-Mixer:", "Replaced standard X-mixer with excitation-preserving XY-mixer on 12 stocks, forcing exactly B=6 stocks and eliminating penalty hyperparameter lambda."),
            ("3. Barren Plateau Bypass on 20 Qubits:", "Used Trotterized Quantum Annealing (TQA) linear schedules to evaluate 20-qubit QAOA directly on FakeSherbrooke without noisy gradient descent."),
            ("4. Heavy-Hex Hardware Transpilation:", "Benchmarked FakeSherbrooke (127 qubits), achieving routing optimization across levels 0 to 3 with symmetry post-selection error mitigation.")
        ]
        y_pos = 54
        for title_b, desc_b in bullets:
            ax.text(52, y_pos, title_b, fontsize=10, fontweight='bold', color='#f8fafc')
            ax.text(52, y_pos - 3.2, desc_b, fontsize=9.2, color='#94a3b8')
            y_pos -= 8.5
            
        ax.text(7, 7, "IIIT-Delhi Qiskit Fall Fest · October 2026 · Public GitHub Submission", fontsize=9.5, color='#64748b')
        pdf.savefig(fig)
        plt.close()

        # =============================================================
        # SLIDE 2: Mathematical Formulation & Problem Setup
        # =============================================================
        fig, ax = setup_slide("Mathematical Formulation: Portfolio QUBO to Ising Mapping",
                             "Constrained Markowitz mean-variance optimization mapped onto quantum Pauli operators", 2)
        
        c1 = patches.FancyBboxPatch((5, 20), 42, 58, boxstyle="round,pad=0.8", facecolor='#131d31', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c1)
        ax.text(7, 73, "1. FINANCIAL OBJECTIVE (MARKOWITZ QUBO)", fontsize=11, fontweight='bold', color='#34d399')
        ax.text(7, 67, r"$\min_{x \in \{0,1\}^n} \; q \, x^T \Sigma x - \mu^T x + \lambda \left(\sum_{i=1}^n x_i - B\right)^2$", fontsize=12, fontweight='bold', color='#f8fafc')
        ax.text(7, 60, "• x_i in {0, 1}: Binary decision to purchase stock i", fontsize=9.5, color='#cbd5e1')
        ax.text(7, 56, "• mu: Expected asset return vector", fontsize=9.5, color='#cbd5e1')
        ax.text(7, 52, "• Sigma: Asset covariance matrix (investment risk)", fontsize=9.5, color='#cbd5e1')
        ax.text(7, 48, "• q = 0.5: Investor risk-aversion hyperparameter", fontsize=9.5, color='#cbd5e1')
        ax.text(7, 44, "• B: Total investment budget (exact number of stocks)", fontsize=9.5, color='#cbd5e1')
        ax.text(7, 40, "• lambda: Penalty coefficient enforcing sum(x_i) = B", fontsize=9.5, color='#cbd5e1')
        
        ax.text(7, 32, "2. QUANTUM ISING HAMILTONIAN MAPPING", fontsize=11, fontweight='bold', color='#38bdf8')
        ax.text(7, 26, r"Substitute binary variable $x_i = \frac{I - Z_i}{2}$:", fontsize=10, color='#cbd5e1')
        ax.text(7, 20, r"$\hat{H}_C = \sum_{i=1}^n h_i \hat{Z}_i + \sum_{i < j} J_{ij} \hat{Z}_i \hat{Z}_j + C_{\text{offset}}$", fontsize=12, fontweight='bold', color='#34d399')
        
        c2 = patches.FancyBboxPatch((51, 20), 44, 58, boxstyle="round,pad=0.8", facecolor='#131d31', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c2)
        ax.text(53, 73, "3. PROBLEM COMPLEXITY HIERARCHY", fontsize=11, fontweight='bold', color='#34d399')
        
        tiers = [
            ("Beginner Level (6 Stocks, Pick 3):", "2^6 = 64 states | 20 valid portfolios | Brute force reference | Depth p and penalty lambda parameter sweeps."),
            ("Intermediate Level (12 Stocks, Pick 6):", "2^12 = 4,096 states | 924 valid portfolios | Continuous QP relaxation | Warm-Start initial state & XY excitation-preserving mixer."),
            ("Advanced Level (20 Stocks, Pick 8):", "2^20 = 1,048,576 states | 125,970 combinations | 5 sector diversification constraints (<= 2 per sector) | Transpilation on 127-qubit FakeSherbrooke.")
        ]
        y_t = 66
        for title_t, desc_t in tiers:
            ax.text(53, y_t, title_t, fontsize=10, fontweight='bold', color='#f8fafc')
            ax.text(53, y_t - 3.2, desc_t, fontsize=8.8, color='#94a3b8')
            y_t -= 9.0
            
        ax.text(53, 34, "4. EVALUATION METRIC (APPROXIMATION RATIO)", fontsize=11, fontweight='bold', color='#38bdf8')
        ax.text(53, 27, r"$r = \frac{C_{\max} - \langle C \rangle}{C_{\max} - C_{\min}} \quad (r = 1.0 \text{ is optimal})$", fontsize=12, fontweight='bold', color='#f8fafc')
        ax.text(53, 21, "Evaluates solution quality over all valid combinations.", fontsize=9, color='#cbd5e1')
        
        pdf.savefig(fig)
        plt.close()

        # =============================================================
        # SLIDE 3: Beginner Level (6 Stocks, Pick 3)
        # =============================================================
        fig, ax = setup_slide("Beginner Baseline: 6 Stocks, Pick 3 with QAOA",
                             "Approximation ratio vs depth p in {1,2,3,4} and feasibility vs penalty strength lambda", 3)
        
        c1 = patches.FancyBboxPatch((5, 18), 38, 60, boxstyle="round,pad=0.8", facecolor='#131d31', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c1)
        ax.text(7, 73, "BEGINNER BENCHMARK FINDINGS", fontsize=10.5, fontweight='bold', color='#34d399')
        ax.text(7, 66, "1. Exact Classical Brute-Force:", fontsize=9.8, fontweight='bold', color='#f8fafc')
        ax.text(7, 61, "Checked all 20 combinations of 6 stocks to identify", fontsize=8.8, color='#cbd5e1')
        ax.text(7, 57, "the ground truth global minimum cost.", fontsize=8.8, color='#cbd5e1')
        
        ax.text(7, 50, "2. Depth Scaling (p = 1 to 4):", fontsize=9.8, fontweight='bold', color='#f8fafc')
        ax.text(7, 45, "Higher depth p allows QAOA to increase constructive", fontsize=8.8, color='#cbd5e1')
        ax.text(7, 41, "interference, raising the approximation ratio r.", fontsize=8.8, color='#cbd5e1')
        
        ax.text(7, 34, "3. Penalty Strength Sweep (lambda):", fontsize=9.8, fontweight='bold', color='#f8fafc')
        ax.text(7, 29, "• lambda < 1.0: Circuit favours unfeasible states.", fontsize=8.8, color='#f43f5e')
        ax.text(7, 24, "• lambda >= 2.0: Budget compliance approaches 100%.", fontsize=8.8, color='#34d399')
        ax.text(7, 19, "• lambda >> 10: Stretches spectrum, slowing COBYLA.", fontsize=8.8, color='#f59e0b')
        
        if os.path.exists('figures/track2_beginner_depth_penalty.png'):
            img1 = mpimg.imread('figures/track2_beginner_depth_penalty.png')
            ax_img1 = fig.add_axes([0.45, 0.18, 0.51, 0.60])
            ax_img1.imshow(img1)
            ax_img1.axis('off')
            
        pdf.savefig(fig)
        plt.close()

        # =============================================================
        # SLIDE 4: Intermediate Level (12 Stocks, Warm-Start & XY-Mixer)
        # =============================================================
        fig, ax = setup_slide("Intermediate Edge: Warm-Start & Constraint-Preserving Mixer",
                             "Solving 12 stocks (pick 6, 924 states) with Continuous Relaxation and XY-Mixers", 4)
        
        c1 = patches.FancyBboxPatch((5, 18), 40, 60, boxstyle="round,pad=0.8", facecolor='#131d31', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c1)
        ax.text(7, 73, "METHOD COMPARISON (N=12 STOCKS)", fontsize=10.5, fontweight='bold', color='#34d399')
        
        ax.text(7, 66, "1. Standard QAOA (Transverse X-Mixer):", fontsize=9.5, fontweight='bold', color='#f8fafc')
        ax.text(7, 61, "Explores entire 2^12 = 4,096 state space; requires soft", fontsize=8.8, color='#cbd5e1')
        ax.text(7, 57, "penalty lambda; only ~25-35% of samples obey budget.", fontsize=8.8, color='#cbd5e1')
        
        ax.text(7, 50, "2. Warm-Start QAOA (Egger et al. 2021):", fontsize=9.5, fontweight='bold', color='#60a5fa')
        ax.text(7, 45, "Solves continuous Quadratic Program (QP) relaxation", fontsize=8.8, color='#cbd5e1')
        ax.text(7, 41, "classically; initializes qubit rotations along c*_i vector.", fontsize=8.8, color='#cbd5e1')
        
        ax.text(7, 34, "3. Ring XY-Mixer (Excitation-Preserving):", fontsize=9.5, fontweight='bold', color='#34d399')
        ax.text(7, 29, "Uses RXX + RYY gates between adjacent qubits. Commutes", fontsize=8.8, color='#cbd5e1')
        ax.text(7, 25, "with sum(Z_i), strictly conserving Hamming weight = 6.", fontsize=8.8, color='#cbd5e1')
        ax.text(7, 20, "--> 100% Budget Feasibility Guaranteed in Noiseless Sim!", fontsize=9.2, color='#34d399', fontweight='bold')
        
        if os.path.exists('figures/track2_intermediate_comparison.png'):
            img2 = mpimg.imread('figures/track2_intermediate_comparison.png')
            ax_img2 = fig.add_axes([0.47, 0.18, 0.49, 0.60])
            ax_img2.imshow(img2)
            ax_img2.axis('off')
            
        pdf.savefig(fig)
        plt.close()

        # =============================================================
        # SLIDE 5: Advanced Level (20 Stocks & Sector Constraints)
        # =============================================================
        fig, ax = setup_slide("Advanced Winning Play: 20 Stocks with Sector Diversification",
                             "1,048,576 state space, 5 market sectors (<= 2 stocks/sector), and TQA schedule", 5)
        
        c1 = patches.FancyBboxPatch((5, 20), 42, 58, boxstyle="round,pad=0.8", facecolor='#131d31', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c1)
        ax.text(7, 73, "1. SECTOR DIVERSIFICATION CONSTRAINTS", fontsize=11, fontweight='bold', color='#34d399')
        ax.text(7, 66, "Real portfolios cannot concentrate in a single industry.", fontsize=9.2, color='#cbd5e1')
        ax.text(7, 62, "We partition 20 stocks into 5 sectors of 4 stocks each:", fontsize=9.2, color='#cbd5e1')
        ax.text(7, 56, "• Tech, Finance, Energy, Healthcare, Consumer", fontsize=9.5, fontweight='bold', color='#f8fafc')
        ax.text(7, 51, "• Rule: At most 2 stocks selected per sector", fontsize=9.5, fontweight='bold', color='#f8fafc')
        ax.text(7, 46, "Formulated as quadratic co-occurrence penalties in Q.", fontsize=9, color='#38bdf8')
        
        ax.text(7, 38, "2. BEATING BARREN PLATEAUS VIA TQA", fontsize=11, fontweight='bold', color='#34d399')
        ax.text(7, 31, "At N=20 qubits, random parameter initialization causes", fontsize=9.2, color='#cbd5e1')
        ax.text(7, 27, "gradients to vanish exponentially (Barren Plateaus).", fontsize=9.2, color='#f43f5e')
        ax.text(7, 22, "Solution: Trotterized Quantum Annealing (TQA) schedule:", fontsize=9.2, color='#cbd5e1')
        ax.text(7, 16, r"$\gamma_k = \frac{k}{p} \Delta t, \quad \beta_k = (1 - \frac{k}{p}) \Delta t$  (Zero-Opt Convergence)", fontsize=10, fontweight='bold', color='#34d399')
        
        c2 = patches.FancyBboxPatch((51, 20), 44, 58, boxstyle="round,pad=0.8", facecolor='#131d31', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c2)
        ax.text(53, 73, "3. QUANTITATIVE BENCHMARK", fontsize=11, fontweight='bold', color='#34d399')
        ax.text(53, 66, "• Total Candidate Combinations: 125,970 valid 8-stock portfolios", fontsize=9.2, color='#cbd5e1')
        ax.text(53, 61, "• Sector Rule Filtering: Eliminates portfolios with >2 stocks/sector", fontsize=9.2, color='#cbd5e1')
        ax.text(53, 56, "• Circuit: 20 Qubits, 190 ZZ interaction pairs in H_C", fontsize=9.2, color='#cbd5e1')
        
        ax.text(53, 46, "4. ZERO-OPTIMIZATION INFERENCE", fontsize=11, fontweight='bold', color='#38bdf8')
        ax.text(53, 40, "Direct evaluation of the TQA statevector identifies high-quality", fontsize=9.2, color='#cbd5e1')
        ax.text(53, 36, "feasible portfolios without costly multi-parameter hardware loops.", fontsize=9.2, color='#cbd5e1')
        ax.text(53, 30, "Enables rapid inference on 127-qubit quantum processors.", fontsize=9.2, color='#34d399', fontweight='bold')
        
        pdf.savefig(fig)
        plt.close()

        # =============================================================
        # SLIDE 6: Hardware-Aware Transpilation on 127 Qubits
        # =============================================================
        fig, ax = setup_slide("Hardware Awareness: 127-Qubit Eagle Routing Benchmark",
                             "Transpiling 20-qubit all-to-all QAOA on IBM FakeSherbrooke across optimization levels", 6)
        
        c1 = patches.FancyBboxPatch((5, 18), 38, 60, boxstyle="round,pad=0.8", facecolor='#131d31', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c1)
        ax.text(7, 73, "HARDWARE BENCHMARKING", fontsize=10.5, fontweight='bold', color='#34d399')
        ax.text(7, 66, "1. Live Physical QPU Execution:", fontsize=9.2, fontweight='bold', color='#38bdf8')
        ax.text(7, 61, "• QPU: ibm_kingston (156 Qubits, Heron r2)", fontsize=8.6, color='#f8fafc', fontweight='bold')
        ax.text(7, 57, "• Job ID: db7qdgmil99s73foltpg (COMPLETED)", fontsize=8.4, color='#34d399', fontweight='bold')
        ax.text(7, 53, "• Error Suppression: XY4 Dynamical Decoupling + Twirling", fontsize=8.2, color='#cbd5e1')
        
        ax.text(7, 46, "2. 127-Qubit Transpilation Profiling:", fontsize=9.2, fontweight='bold', color='#38bdf8')
        ax.text(7, 41, "• Target: IBM FakeSherbrooke (Eagle r3 topology)", fontsize=8.4, color='#cbd5e1')
        ax.text(7, 37, "• Optimization Level 2 reduced 2-qubit ECR gates", fontsize=8.4, color='#cbd5e1')
        ax.text(7, 33, "  from 2,830 to 671 (-76.3% gate reduction).", fontsize=8.4, color='#cbd5e1')
        ax.text(7, 28, "• SabreRouting efficiently mapped dense N=20 graph.", fontsize=8.4, color='#cbd5e1')
        ax.text(7, 22, "Physical + Digital-Twin Validation Complete", fontsize=8.6, color='#fbbf24', fontweight='bold')
        
        if os.path.exists('figures/track2_advanced_transpilation.png'):
            img3 = mpimg.imread('figures/track2_advanced_transpilation.png')
            ax_img3 = fig.add_axes([0.45, 0.18, 0.51, 0.60])
            ax_img3.imshow(img3)
            ax_img3.axis('off')
            
        pdf.savefig(fig)
        plt.close()

        # =============================================================
        # SLIDE 7: 3-Way Master Validation (Noiseless vs Noisy vs Mitigated)
        # =============================================================
        fig, ax = setup_slide("Master Validation Results: 20-Stock Energy Distributions",
                             "Noiseless Simulator vs FakeSherbrooke Hardware Noise vs Symmetry Post-Selection", 7)
        
        if os.path.exists('figures/track2_advanced_hardware_distribution.png'):
            img4 = mpimg.imread('figures/track2_advanced_hardware_distribution.png')
            ax_img4 = fig.add_axes([0.05, 0.18, 0.52, 0.60])
            ax_img4.imshow(img4)
            ax_img4.axis('off')
            
        c1 = patches.FancyBboxPatch((60, 18), 35, 60, boxstyle="round,pad=0.8", facecolor='#131d31', edgecolor='#10b981', linewidth=1.2)
        ax.add_patch(c1)
        ax.text(62, 73, "MASTER VALIDATION FINDINGS", fontsize=11, fontweight='bold', color='#34d399')
        
        findings = [
            ("1. Noisy Shift:", "Under FakeSherbrooke depolarizing & thermal noise, the raw energy distribution broadens and shifts toward higher unfeasible costs."),
            ("2. Symmetry Post-Selection:", "Filtering samples to strictly enforce budget (sum(x)=8) and sector caps (<=2/sector) removes noise-corrupted bitstrings."),
            ("3. Ground State Discovery:", "Even under heavy 127-qubit hardware noise, post-selected sampling successfully identifies near-optimal low-cost portfolios."),
            ("4. 4096-Shot Sampling:", "Demonstrates that QAOA concentrates measurement weight in low-energy feasible sectors of the 1,048,576 state space.")
        ]
        y_f = 66
        for t_f, d_f in findings:
            ax.text(62, y_f, t_f, fontsize=9.8, fontweight='bold', color='#f8fafc')
            ax.text(62, y_f - 3.2, d_f, fontsize=8.8, color='#94a3b8')
            y_f -= 9.5
            
        pdf.savefig(fig)
        plt.close()

        # =============================================================
        # SLIDE 8: Engineering Limitations & Reproducibility Guide
        # =============================================================
        fig, ax = setup_slide("Performance Limitations, Credits & Reproducibility Guide",
                             "Honest engineering analysis of failure modes, open-source attribution, and execution guide", 8)
        
        c1 = patches.FancyBboxPatch((5, 18), 42, 60, boxstyle="round,pad=0.8", facecolor='#131d31', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c1)
        ax.text(7, 73, "ENGINEERING LIMITATIONS & BREAKDOWN", fontsize=10.5, fontweight='bold', color='#f43f5e')
        
        ax.text(7, 66, "1. Dense All-to-All Covariance Routing:", fontsize=9.5, fontweight='bold', color='#f8fafc')
        ax.text(7, 61, "Financial covariance Sigma is dense, producing N(N-1)/2", fontsize=8.8, color='#cbd5e1')
        ax.text(7, 57, "interaction terms. Sparse hardware routing incurs high", fontsize=8.8, color='#cbd5e1')
        ax.text(7, 53, "SWAP overhead. Beyond p=2, noise overtakes signal.", fontsize=8.8, color='#cbd5e1')
        
        ax.text(7, 46, "2. Penalty vs Spectral Gap Trade-Off:", fontsize=9.5, fontweight='bold', color='#f8fafc')
        ax.text(7, 41, "Small lambda yields unfeasible portfolios; large lambda", fontsize=8.8, color='#cbd5e1')
        ax.text(7, 37, "stretches the spectrum, trapping COBYLA in local minima.", fontsize=8.8, color='#cbd5e1')
        
        ax.text(7, 30, "3. Symmetry Breaking under Physical Errors:", fontsize=9.5, fontweight='bold', color='#f8fafc')
        ax.text(7, 25, "Physical ECR gate errors break Hamming-weight conservation", fontsize=8.8, color='#cbd5e1')
        ax.text(7, 21, "in XY-mixers, requiring classical subspace post-selection.", fontsize=8.8, color='#cbd5e1')
        
        c2 = patches.FancyBboxPatch((51, 18), 44, 60, boxstyle="round,pad=0.8", facecolor='#131d31', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c2)
        ax.text(53, 73, "REPRODUCIBILITY & ATTRIBUTION", fontsize=10.5, fontweight='bold', color='#34d399')
        ax.text(53, 66, "1. How to Run:", fontsize=9.5, fontweight='bold', color='#f8fafc')
        ax.text(53, 61, "  pip install qiskit qiskit-aer qiskit-ibm-runtime pandas", fontsize=9, color='#34d399')
        ax.text(53, 56, "  jupyter notebook Quantum_Portfolio_Optimization_QAOA.ipynb", fontsize=9, color='#38bdf8')
        
        ax.text(53, 48, "2. Tutorial & Academic Attribution:", fontsize=9.5, fontweight='bold', color='#f8fafc')
        ax.text(53, 43, "• Adapted from BasQ Qiskit Fall Fest 2026 tutorials by Benjamin Tirado.", fontsize=8.8, color='#cbd5e1')
        ax.text(53, 39, "• Farhi et al. (2014) - Quantum Approximate Optimization Algorithm.", fontsize=8.8, color='#cbd5e1')
        ax.text(53, 35, "• Egger et al. (2021) - Warm-Starting Quantum Optimization.", fontsize=8.8, color='#cbd5e1')
        ax.text(53, 31, "• Sachdeva et al. (2024) - Utility-Scale Optimization on IBM Hardware.", fontsize=8.8, color='#cbd5e1')
        
        ax.text(53, 23, "3. AI Tools Disclosure:", fontsize=9.5, fontweight='bold', color='#f8fafc')
        ax.text(53, 18, "Google Antigravity AI pair programming assistant used for code drafting,", fontsize=8.8, color='#94a3b8')
        ax.text(53, 14, "optimization benchmarking, and vector slide generation.", fontsize=8.8, color='#94a3b8')
        
        pdf.savefig(fig)
        plt.close()
        
    print(f"Successfully generated Track 2 slide deck: {pdf_path} (8 vector slides).")

if __name__ == "__main__":
    create_track2_slides()
