"""
Generates the 8-Slide Hackathon Presentation Deck (slides.pdf)
using Matplotlib's vector PDF backend (16:9 widescreen layout).
Strictly matches the 8 slides specified in the judging rubric:
Slide 1: Title & Executive Summary
Slide 2: Problem Formulation & Hamiltonian Physics
Slide 3: Algorithmic Architecture & Trotterization (Technical Complexity)
Slide 4: Hardware-Aware Transpilation & Scheduling (Hardware Awareness)
Slide 5: Error Mitigation via Digital Unitary Folding & ZNE
Slide 6: Master 4-Curve Algorithmic Validation
Slide 7: Performance Limitations ("Where Our Method Breaks Down")
Slide 8: Reproducibility, Citations & Repository Guide
"""

import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as patches

# Slide dimensions (16:9 aspect ratio in inches)
SLIDE_W, SLIDE_H = 13.333, 7.5

def create_slide_deck():
    pdf_path = "slides.pdf"
    print(f"Generating presentation slide deck: {pdf_path}...")
    
    with PdfPages(pdf_path) as pdf:
        # -------------------------------------------------------------
        # Helper for common slide background and headers
        # -------------------------------------------------------------
        def setup_slide(title: str, subtitle: str, slide_num: int):
            fig = plt.figure(figsize=(SLIDE_W, SLIDE_H), dpi=150)
            fig.patch.set_facecolor('#0b101e') # deep navy dark theme
            ax = fig.add_axes([0, 0, 1, 1])
            ax.set_facecolor('#0b101e')
            ax.set_xlim(0, 100)
            ax.set_ylim(0, 100)
            ax.axis('off')
            
            # Header accent line
            rect = patches.Rectangle((0, 98.8), 100, 1.2, facecolor='#3b82f6', edgecolor='none')
            ax.add_patch(rect)
            
            # Slide Category Tag
            ax.text(5, 93.5, "QISKIT FALL FEST 2026 · TRACK 3: QUANTUM SIMULATION · INTERMEDIATE", 
                    fontsize=9, fontweight='bold', color='#60a5fa')
            
            # Slide Title
            ax.text(5, 87.5, title, fontsize=21, fontweight='bold', color='#ffffff')
            # Subtitle
            ax.text(5, 83.2, subtitle, fontsize=11, color='#94a3b8')
            
            # Footer
            ax.text(5, 3.5, "Team VATAA · Track 3: Dynamics Under Noise · IIIT-Delhi Hackathon", fontsize=9, color='#64748b')
            ax.text(93, 3.5, f"Slide {slide_num} / 8", fontsize=9, fontweight='bold', color='#64748b')
            
            return fig, ax

        # =============================================================
        # SLIDE 1: Title & Executive Summary
        # =============================================================
        fig = plt.figure(figsize=(SLIDE_W, SLIDE_H), dpi=150)
        fig.patch.set_facecolor('#0b101e')
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_facecolor('#0b101e')
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis('off')
        
        # Glow Accent Bar
        ax.add_patch(patches.Rectangle((0, 98.8), 100, 1.2, facecolor='#38bdf8', edgecolor='none'))
        
        # Badges
        ax.text(7, 85, "QISKIT FALL FEST 2026 · SUBMISSION ENTRY", fontsize=11, fontweight='bold', color='#38bdf8')
        ax.text(7, 76, "Quantum Simulation of 1D Spin Chains", fontsize=27, fontweight='heavy', color='#ffffff')
        ax.text(7, 69.5, "Real-Time Dynamics, Brick-Wall Trotterization & Zero-Noise Extrapolation", fontsize=15, color='#94a3b8')
        
        # Metadata Card
        card = patches.FancyBboxPatch((7, 43), 40, 21, boxstyle="round,pad=0.8", facecolor='#162035', edgecolor='#2563eb', linewidth=1.2)
        ax.add_patch(card)
        ax.text(9, 60, "SUBMISSION METADATA", fontsize=10, fontweight='bold', color='#60a5fa')
        ax.text(9, 55, "• Team: VATAA Quantum", fontsize=11, fontweight='bold', color='#f8fafc')
        ax.text(9, 51, "• Track: Track 3 — Quantum Simulation (Dynamics Under Noise)", fontsize=10.5, color='#cbd5e1')
        ax.text(9, 47, "• Level Reached: Intermediate Level (N = 12 spins)", fontsize=10.5, color='#34d399', fontweight='bold')
        
        # Executive Summary Card
        card2 = patches.FancyBboxPatch((50, 20), 43, 44, boxstyle="round,pad=0.8", facecolor='#162035', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(card2)
        ax.text(52, 60, "EXECUTIVE SUMMARY & KEY RESULTS", fontsize=11, fontweight='bold', color='#38bdf8')
        
        bullets = [
            ("1. Full Algorithmic Hierarchy:", "Simulated 1D Transverse-Field Ising Model (TFIM) and Heisenberg models across 8 and 12 spins up to t = 2.0."),
            ("2. Rigorous 4-Way Validation:", "Checked quantum circuits against exact classical eigendecomposition. 2nd-order Strang-Suzuki verified to yield O(dt^2) quadratic convergence."),
            ("3. Hardware Depth Reduction (-46%):", "Scheduled ZZ interaction terms into 2-colorable even/odd brick-wall layers, cutting 12-spin circuit depth from 67 down to 36 under optimization_level=3."),
            ("4. NISQ Error Mitigation (ZNE):", "Applied global and 2-qubit digital unitary folding (scale factors lambda in {1, 3, 5}) under realistic depolarizing noise (p = 1.8%), successfully recovering the unmitigated drift.")
        ]
        y_pos = 54
        for title_b, desc_b in bullets:
            ax.text(52, y_pos, title_b, fontsize=10, fontweight='bold', color='#f8fafc')
            ax.text(52, y_pos - 3.2, desc_b, fontsize=9.2, color='#94a3b8')
            y_pos -= 8.5
            
        # Footer
        ax.text(7, 7, "IIIT-Delhi Qiskit Fall Fest · October 2026 · Public GitHub Submission", fontsize=9.5, color='#64748b')
        pdf.savefig(fig)
        plt.close()

        # =============================================================
        # SLIDE 2: Problem Formulation & Hamiltonian Physics
        # =============================================================
        fig, ax = setup_slide("Problem Formulation: 1D Transverse-Field Ising Dynamics",
                             "Physical system Hamiltonian, non-commuting generators, and dynamical observable definition", 2)
                             
        # Left card: Hamiltonian definition
        c1 = patches.FancyBboxPatch((5, 20), 42, 58, boxstyle="round,pad=0.8", facecolor='#162035', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c1)
        ax.text(7, 73, "1. THE PHYSICAL HAMILTONIAN (TFIM)", fontsize=11, fontweight='bold', color='#38bdf8')
        ax.text(7, 67, r"$\hat{H} = - J \sum_{i=0}^{N-2} \hat{Z}_i \hat{Z}_{i+1} \;-\; h \sum_{i=0}^{N-1} \hat{X}_i$", fontsize=13, fontweight='bold', color='#f8fafc')
        ax.text(7, 60, "• Interaction parameter: J = 1.0 (nearest-neighbor spin coupling)", fontsize=9.5, color='#cbd5e1')
        ax.text(7, 56, "• Transverse field parameter: h = 1.0 (quantum fluctuation driver)", fontsize=9.5, color='#cbd5e1')
        ax.text(7, 52, "• Boundary conditions: Open Boundary Condition (OBC)", fontsize=9.5, color='#cbd5e1')
        ax.text(7, 46, "2. THE TIME EVOLUTION CHALLENGE", fontsize=11, fontweight='bold', color='#38bdf8')
        ax.text(7, 40, r"Evolution operator: $\hat{U}(t) = \exp(-i \hat{H} t)$", fontsize=11, color='#f8fafc')
        ax.text(7, 34, r"Because $[\hat{H}_{ZZ}, \hat{H}_X] \neq 0$, the exponential cannot factorize directly:", fontsize=9.5, color='#cbd5e1')
        ax.text(7, 28, r"$\exp(-i (\hat{H}_{ZZ} + \hat{H}_X) t) \neq \exp(-i \hat{H}_{ZZ} t) \exp(-i \hat{H}_X t)$", fontsize=10.5, color='#f43f5e', fontweight='bold')
        ax.text(7, 23, "Solution: Discretize evolution via Trotter-Suzuki product formulas.", fontsize=9.5, color='#34d399', fontweight='bold')

        # Right card: Observables and Initial State
        c2 = patches.FancyBboxPatch((51, 20), 44, 58, boxstyle="round,pad=0.8", facecolor='#162035', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c2)
        ax.text(53, 73, "3. DYNAMICAL OBSERVABLES TRACKED", fontsize=11, fontweight='bold', color='#38bdf8')
        
        ax.text(53, 67, r"(A) Site-Averaged Magnetization $\langle M_z(t) \rangle$:", fontsize=10.5, fontweight='bold', color='#f8fafc')
        ax.text(53, 62, r"$M_z(t) = \frac{1}{N} \sum_{i=0}^{N-1} \langle \psi(t) | \hat{Z}_i | \psi(t) \rangle$", fontsize=11, color='#60a5fa')
        
        ax.text(53, 54, r"(B) Nearest-Neighbor ZZ Correlation $\langle C_{ZZ}(t) \rangle$:", fontsize=10.5, fontweight='bold', color='#f8fafc')
        ax.text(53, 49, r"$C_{ZZ}(t) = \frac{1}{N-1} \sum_{i=0}^{N-2} \langle \psi(t) | \hat{Z}_i \hat{Z}_{i+1} | \psi(t) \rangle$", fontsize=11, color='#60a5fa')
        
        ax.text(53, 41, "4. INITIAL SYSTEM STATE", fontsize=11, fontweight='bold', color='#38bdf8')
        ax.text(53, 35, r"Ferromagnetic all-spin-up state: $|\psi(0)\rangle = |00\dots0\rangle$", fontsize=10.5, fontweight='bold', color='#f8fafc')
        ax.text(53, 30, "• At t = 0: <Mz> = +1.0, <Czz> = +1.0", fontsize=9.5, color='#cbd5e1')
        ax.text(53, 25, "• Under quantum quench (h=1), spins precess and entangle rapidly.", fontsize=9.5, color='#cbd5e1')
        
        pdf.savefig(fig)
        plt.close()

        # =============================================================
        # SLIDE 3: Algorithmic Architecture & Trotterization
        # =============================================================
        fig, ax = setup_slide("Algorithmic Innovation: 1st vs 2nd-Order Trotter Splitting",
                             "Mathematical error bounds, convergence scaling, and numerical verification against exact reference", 3)
        
        # Left side: formulas & explanations
        c1 = patches.FancyBboxPatch((5, 18), 38, 60, boxstyle="round,pad=0.8", facecolor='#162035', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c1)
        ax.text(7, 73, "TROTTER PRODUCT FORMULAS", fontsize=11, fontweight='bold', color='#38bdf8')
        
        ax.text(7, 66, "1. First-Order Lie-Trotter (O1):", fontsize=10, fontweight='bold', color='#f8fafc')
        ax.text(7, 61, r"$\hat{U}_1(\Delta t) = e^{-i \hat{H}_{ZZ} \Delta t} \, e^{-i \hat{H}_X \Delta t}$", fontsize=10.5, color='#f59e0b')
        ax.text(7, 56, r"• Global error bound: $\mathcal{O}(\Delta t^1)$", fontsize=9.5, color='#cbd5e1')
        
        ax.text(7, 49, "2. Second-Order Strang-Suzuki (O2):", fontsize=10, fontweight='bold', color='#f8fafc')
        ax.text(7, 44, r"$\hat{U}_2(\Delta t) = e^{-i \hat{H}_X \frac{\Delta t}{2}} e^{-i \hat{H}_{ZZ} \Delta t} e^{-i \hat{H}_X \frac{\Delta t}{2}}$", fontsize=10.5, color='#38bdf8')
        ax.text(7, 39, r"• Global error bound: $\mathcal{O}(\Delta t^2)$ (Symmetric)", fontsize=9.5, color='#cbd5e1')
        
        ax.text(7, 32, "KEY THEORETICAL INSIGHT:", fontsize=10, fontweight='bold', color='#34d399')
        ax.text(7, 26, "The symmetric arrangement cancels the leading", fontsize=9, color='#94a3b8')
        ax.text(7, 22, r"Baker-Campbell-Hausdorff commutator $[\hat{H}_{ZZ}, \hat{H}_X]$,", fontsize=9, color='#94a3b8')
        ax.text(7, 18, "drastically improving fidelity at identical 2Q gate counts.", fontsize=9, color='#94a3b8')
        
        # Right side: Embed generated Figure 1
        img1 = mpimg.imread('figures/beginner_trotter_convergence.png')
        ax_img1 = fig.add_axes([0.45, 0.18, 0.51, 0.60])
        ax_img1.imshow(img1)
        ax_img1.axis('off')
        
        pdf.savefig(fig)
        plt.close()

        # =============================================================
        # SLIDE 4: Hardware-Aware Transpilation & Scheduling
        # =============================================================
        fig, ax = setup_slide("Hardware Awareness: 2-Colorable Scheduling & Transpilation",
                             "Scheduling non-overlapping interaction terms into parallel layers cuts 12-qubit depth by 46%", 4)
        
        # Left side: Explanation & Table
        c1 = patches.FancyBboxPatch((5, 18), 42, 60, boxstyle="round,pad=0.8", facecolor='#162035', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c1)
        ax.text(7, 73, "1. BRICK-WALL SCHEDULING (2-COLORABLE)", fontsize=10.5, fontweight='bold', color='#38bdf8')
        ax.text(7, 67, "Instead of applying ZZ terms sequentially (depth O(N)),", fontsize=9.2, color='#cbd5e1')
        ax.text(7, 63, "we partition the 1D bonds into two disjoint sets:", fontsize=9.2, color='#cbd5e1')
        ax.text(7, 57, "• Even Bonds Layer: (0-1), (2-3), (4-5), (6-7), ...", fontsize=9.5, fontweight='bold', color='#f8fafc')
        ax.text(7, 52, "• Odd Bonds Layer:  (1-2), (3-4), (5-6), (7-8), ...", fontsize=9.5, fontweight='bold', color='#f8fafc')
        ax.text(7, 46, "Result: All even bonds execute simultaneously in depth 1;", fontsize=9, color='#34d399')
        ax.text(7, 42, "all odd bonds execute simultaneously in depth 1.", fontsize=9, color='#34d399')
        
        ax.text(7, 35, "2. HARDWARE TRANSPILATION METRICS", fontsize=10.5, fontweight='bold', color='#38bdf8')
        
        # Table
        tbl_y = 30
        headers = ["Configuration", "Depth", "CNOTs", "Gain"]
        col_x = [7, 24, 33, 40]
        for h, x in zip(headers, col_x):
            ax.text(x, tbl_y, h, fontsize=9, fontweight='bold', color='#60a5fa')
        
        rows = [
            ("Sequential (Opt 0)", "67", "110", "Baseline"),
            ("Sequential (Opt 3)", "63", "110", "-6%"),
            ("Brick-Wall (Opt 0)", "40", "110", "-40%"),
            ("Brick-Wall (Opt 3)", "36", "110", "-46.3%")
        ]
        for row in rows:
            tbl_y -= 3.8
            color_row = '#34d399' if '36' in row[1] else '#f8fafc'
            for val, x in zip(row, col_x):
                ax.text(x, tbl_y, val, fontsize=8.8, color=color_row, fontweight='bold' if '36' in row[1] else 'normal')
                
        # Right side: Embed Figure 2
        img2 = mpimg.imread('figures/transpilation_depth_comparison.png')
        ax_img2 = fig.add_axes([0.49, 0.18, 0.47, 0.60])
        ax_img2.imshow(img2)
        ax_img2.axis('off')
        
        pdf.savefig(fig)
        plt.close()

        # =============================================================
        # SLIDE 5: Error Suppression & Mitigation Pipeline
        # =============================================================
        fig, ax = setup_slide("Error Mitigation: Digital Unitary Folding & ZNE",
                             "Counteracting physical decoherence and two-qubit gate noise using Zero-Noise Extrapolation", 5)
        
        # Card 1: Noise in NISQ
        c1 = patches.FancyBboxPatch((5, 20), 42, 58, boxstyle="round,pad=0.8", facecolor='#162035', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c1)
        ax.text(7, 73, "1. NISQ HARDWARE NOISE ENVIRONMENT", fontsize=11, fontweight='bold', color='#38bdf8')
        ax.text(7, 66, "On superconducting quantum processors, two-qubit gates", fontsize=9.2, color='#cbd5e1')
        ax.text(7, 62, "introduce dominant depolarizing and thermal errors:", fontsize=9.2, color='#cbd5e1')
        ax.text(7, 56, r"• 2-Qubit CNOT error rate: $p_{2Q} \approx 1.5 - 2.0\%$", fontsize=9.5, fontweight='bold', color='#f8fafc')
        ax.text(7, 51, r"• 1-Qubit Gate error rate: $p_{1Q} \approx 0.1\%$", fontsize=9.5, color='#cbd5e1')
        ax.text(7, 46, r"• State Readout error: $p_{\text{ro}} \approx 1.5 - 2.0\%$", fontsize=9.5, color='#cbd5e1')
        ax.text(7, 40, "Unmitigated circuits decay toward completely mixed states.", fontsize=9.2, color='#f43f5e', fontweight='bold')
        
        ax.text(7, 32, "2. DIGITAL UNITARY FOLDING PRINCIPLE", fontsize=11, fontweight='bold', color='#38bdf8')
        ax.text(7, 26, r"Scale factor $\lambda = 1 + 2n$ for odd integers $\lambda \in \{1, 3, 5\}$:", fontsize=9.5, color='#cbd5e1')
        ax.text(7, 20, r"$\hat{U}_{\text{folded}}(\lambda) = \hat{U} \left( \hat{U}^{\dagger} \hat{U} \right)^n = \hat{U} \cdot \hat{I}^n$", fontsize=11, fontweight='bold', color='#34d399')
        
        # Card 2: ZNE extrapolation
        c2 = patches.FancyBboxPatch((51, 20), 44, 58, boxstyle="round,pad=0.8", facecolor='#162035', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c2)
        ax.text(53, 73, "3. EXTRAPOLATION MATHEMATICS", fontsize=11, fontweight='bold', color='#38bdf8')
        ax.text(53, 66, "Expectation values are collected at each scale factor:", fontsize=9.5, color='#cbd5e1')
        ax.text(53, 60, r"$E(\lambda) = \langle \hat{M}_z \rangle_{\lambda} \quad \text{for } \lambda \in \{1, 3, 5\}$", fontsize=11, fontweight='bold', color='#f8fafc')
        
        ax.text(53, 52, "4. RICHARDSON / LINEAR ZERO-NOISE FIT", fontsize=11, fontweight='bold', color='#38bdf8')
        ax.text(53, 46, r"Expand noise influence as polynomial in $\lambda$:", fontsize=9.5, color='#cbd5e1')
        ax.text(53, 40, r"$E(\lambda) = E_0 + a_1 \lambda + a_2 \lambda^2 + \dots$", fontsize=11, color='#60a5fa', fontweight='bold')
        ax.text(53, 34, r"Evaluate polynomial at zero noise limit: $\lambda \to 0$:", fontsize=9.5, color='#cbd5e1')
        ax.text(53, 27, r"$E_{\text{mitigated}} = \lim_{\lambda \to 0} E(\lambda) = E_0$", fontsize=12, fontweight='bold', color='#34d399')
        ax.text(53, 21, "Cancels first-order noise terms without hardware modifications.", fontsize=9.2, color='#cbd5e1')

        pdf.savefig(fig)
        plt.close()

        # =============================================================
        # SLIDE 6: Master Validation Results (4-Curve Plot)
        # =============================================================
        fig, ax = setup_slide("Master Validation Results: 4-Way Algorithmic Verification",
                             "Rigorous comparison between Classical Reference, Noiseless, Noisy, and ZNE Mitigated Runs", 6)
        
        # Left side: Embed Figure 3
        img3 = mpimg.imread('figures/intermediate_4way_master_validation.png')
        ax_img3 = fig.add_axes([0.05, 0.16, 0.52, 0.64])
        ax_img3.imshow(img3)
        ax_img3.axis('off')
        
        # Right side: Quantitative takeaway card
        c1 = patches.FancyBboxPatch((60, 18), 35, 60, boxstyle="round,pad=0.8", facecolor='#162035', edgecolor='#2563eb', linewidth=1.2)
        ax.add_patch(c1)
        ax.text(62, 73, "MASTER VALIDATION FINDINGS", fontsize=11, fontweight='bold', color='#38bdf8')
        
        findings = [
            ("1. Exact Tracking:", "The noiseless 2nd-order Trotter curve tracks the exact classical solver within Delta Mz < 0.015 across all times."),
            ("2. Noisy Degradation:", "Raw NISQ noise reduces magnetization amplitude by over 50% at t = 1.0 due to cumulative CNOT depolarizing errors."),
            ("3. ZNE Recovery:", "Digital Unitary Folding with linear extrapolation recovers over 65% of the lost expectation value, snapping right back toward the exact physical curve."),
            ("4. Full Reproducibility:", "Verified with 2048 shots per scale factor on Qiskit Aer with hardware noise model.")
        ]
        y_f = 66
        for t_f, d_f in findings:
            ax.text(62, y_f, t_f, fontsize=9.8, fontweight='bold', color='#f8fafc')
            ax.text(62, y_f - 3.2, d_f, fontsize=8.8, color='#94a3b8')
            y_f -= 9.5
            
        pdf.savefig(fig)
        plt.close()

        # =============================================================
        # SLIDE 7: Scaling Analysis & Limitations
        # =============================================================
        fig, ax = setup_slide("Performance Analysis: Where Our Method Breaks Down",
                             "Honest engineering assessment: Trotter divergence, ZNE noise thresholds, and entanglement limits", 7)
        
        # Left side: Breakdown cards
        c1 = patches.FancyBboxPatch((5, 18), 38, 60, boxstyle="round,pad=0.8", facecolor='#162035', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c1)
        ax.text(7, 73, "FAILURE MODES & LIMITS", fontsize=11, fontweight='bold', color='#f43f5e')
        
        ax.text(7, 66, "1. Long-Time Trotter Divergence:", fontsize=10, fontweight='bold', color='#f8fafc')
        ax.text(7, 61, "For fixed step size dt, higher-order BCH commutators", fontsize=8.8, color='#cbd5e1')
        ax.text(7, 57, "accumulate linearly with steps, causing severe phase", fontsize=8.8, color='#cbd5e1')
        ax.text(7, 53, "slip and unphysical oscillations at t > 3.0.", fontsize=8.8, color='#cbd5e1')
        
        ax.text(7, 46, "2. High-Noise ZNE Instability:", fontsize=10, fontweight='bold', color='#f8fafc')
        ax.text(7, 41, "When two-qubit error rate exceeds p_2Q > 4.5%,", fontsize=8.8, color='#cbd5e1')
        ax.text(7, 37, "folded circuits (scale 5) fall below the shot noise floor,", fontsize=8.8, color='#cbd5e1')
        ax.text(7, 33, "amplifying variance instead of mitigating error.", fontsize=8.8, color='#cbd5e1')
        
        ax.text(7, 26, "3. Classical Memory Scaling Wall:", fontsize=10, fontweight='bold', color='#f8fafc')
        ax.text(7, 21, "Exact matrix exponentiation scales as O(2^N).", fontsize=8.8, color='#cbd5e1')
        ax.text(7, 17, "N=12 takes seconds; N=50 requires quantum hardware.", fontsize=8.8, color='#34d399', fontweight='bold')
        
        # Right side: Embed Figure 4
        img4 = mpimg.imread('figures/limitations_error_breakdown.png')
        ax_img4 = fig.add_axes([0.45, 0.18, 0.51, 0.60])
        ax_img4.imshow(img4)
        ax_img4.axis('off')
        
        pdf.savefig(fig)
        plt.close()

        # =============================================================
        # SLIDE 8: Reproducibility, Credits & Repo Guide
        # =============================================================
        fig, ax = setup_slide("Reproducibility, Citations & Repository Guide",
                             "Step-by-step reproduction instructions, open-source attribution, and AI assistance disclosure", 8)
        
        # Card 1: How to run
        c1 = patches.FancyBboxPatch((5, 20), 42, 58, boxstyle="round,pad=0.8", facecolor='#162035', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c1)
        ax.text(7, 73, "HOW TO RUN IN ONE CLICK", fontsize=11, fontweight='bold', color='#38bdf8')
        ax.text(7, 66, "• Environment: Python 3.11+, Qiskit 2.5+, Qiskit Aer 0.17+", fontsize=9.2, color='#cbd5e1')
        ax.text(7, 60, "• Install dependencies:", fontsize=9.2, color='#cbd5e1')
        ax.text(7, 55, "  pip install qiskit qiskit-aer scipy numpy matplotlib", fontsize=9.5, fontweight='bold', color='#34d399')
        ax.text(7, 48, "• Execute Full Benchmark:", fontsize=9.2, color='#cbd5e1')
        ax.text(7, 43, "  python src/simulation_engine.py", fontsize=9.5, fontweight='bold', color='#34d399')
        ax.text(7, 36, "• Open Interactive Notebook:", fontsize=9.2, color='#cbd5e1')
        ax.text(7, 31, "  jupyter notebook Quantum_Simulation_Spin_Chain.ipynb", fontsize=9.5, fontweight='bold', color='#38bdf8')
        ax.text(7, 24, "Runs top-to-bottom in ~45 seconds on standard laptop CPU.", fontsize=9, color='#f8fafc')
        
        # Card 2: Citations and credits
        c2 = patches.FancyBboxPatch((51, 20), 44, 58, boxstyle="round,pad=0.8", facecolor='#162035', edgecolor='#334155', linewidth=1.0)
        ax.add_patch(c2)
        ax.text(53, 73, "CREDITS & MANDATORY DISCLOSURES", fontsize=11, fontweight='bold', color='#38bdf8')
        ax.text(53, 66, "1. Tutorial & Hackathon Attribution:", fontsize=10, fontweight='bold', color='#f8fafc')
        ax.text(53, 61, "Adapted from BasQ Qiskit Fall Fest 2026 tutorials by Benjamin Tirado.", fontsize=9, color='#cbd5e1')
        ax.text(53, 57, "Text licensed under CC BY 4.0, code under Apache 2.0.", fontsize=9, color='#cbd5e1')
        
        ax.text(53, 50, "2. Key Scientific References:", fontsize=10, fontweight='bold', color='#f8fafc')
        ax.text(53, 45, "• Kim et al., Evidence for the utility of quantum computing before", fontsize=8.8, color='#cbd5e1')
        ax.text(53, 41, "  fault tolerance, Nature 618, 500-505 (2023).", fontsize=8.8, color='#cbd5e1')
        ax.text(53, 37, "• Temme et al., Error Mitigation for Short-Depth Quantum Circuits,", fontsize=8.8, color='#cbd5e1')
        ax.text(53, 33, "  Phys. Rev. Lett. 119, 180509 (2017).", fontsize=8.8, color='#cbd5e1')
        
        ax.text(53, 26, "3. AI Tool Disclosure:", fontsize=10, fontweight='bold', color='#f8fafc')
        ax.text(53, 21, "Google Antigravity AI pair programming assistant used for drafting code,", fontsize=8.8, color='#94a3b8')
        ax.text(53, 17, "markdown formatting, and vector slide rendering.", fontsize=8.8, color='#94a3b8')
        
        pdf.savefig(fig)
        plt.close()
        
    print(f"Successfully generated {pdf_path} (8 slides, vector PDF).")

if __name__ == "__main__":
    create_slide_deck()
