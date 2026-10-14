"""
Exact classical diagonalization and matrix exponential solver for 1D spin chains.
Provides the ground truth baseline for quantum simulation validation.
"""

import numpy as np
import scipy.linalg as la
from typing import List, Dict, Tuple
from qiskit.quantum_info import SparsePauliOp, Statevector

class ExactSpinChainSolver:
    def __init__(self, hamiltonian_op: SparsePauliOp, initial_state: Statevector):
        """
        hamiltonian_op: SparsePauliOp representing the spin chain Hamiltonian.
        initial_state: Initial state |psi(0)> as a Qiskit Statevector.
        """
        self.op = hamiltonian_op
        self.num_qubits = hamiltonian_op.num_qubits
        self.H_matrix = hamiltonian_op.to_matrix()
        self.psi0 = np.array(initial_state.data, dtype=complex)
        
        # Eigendecomposition for ultra-fast time evolution
        self.energies, self.eigenvectors = la.eigh(self.H_matrix)
        self.c0 = self.eigenvectors.conj().T @ self.psi0

    def state_at(self, t: float) -> np.ndarray:
        """Computes exact |psi(t)> = sum_k c_k e^{-i E_k t} |E_k>."""
        phases = np.exp(-1j * self.energies * t)
        psi_t = self.eigenvectors @ (self.c0 * phases)
        return psi_t

    def expectation_value(self, observable_op: SparsePauliOp, t: float) -> float:
        """Computes <psi(t)| O |psi(t)> exactly."""
        psi_t = self.state_at(t)
        O_mat = observable_op.to_matrix()
        val = np.vdot(psi_t, O_mat @ psi_t)
        return float(np.real(val))

    def time_evolve_observable(self, observable_op: SparsePauliOp, time_grid: np.ndarray) -> np.ndarray:
        """Evaluates expectation value across an entire time array."""
        return np.array([self.expectation_value(observable_op, t) for t in time_grid])

    def compute_fidelity(self, quantum_state: Statevector, t: float) -> float:
        """Computes state fidelity |<psi_exact(t) | psi_quantum(t)>|^2."""
        psi_exact = self.state_at(t)
        psi_q = np.array(quantum_state.data, dtype=complex)
        overlap = np.vdot(psi_exact, psi_q)
        return float(np.abs(overlap)**2)
