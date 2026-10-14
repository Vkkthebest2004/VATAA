"""
Hamiltonian definitions for 1D Quantum Spin Chains:
1. Transverse-Field Ising Model (TFIM):
   H = - J * sum_{i=0}^{N-2} (Z_i Z_{i+1}) - h * sum_{i=0}^{N-1} X_i
2. Heisenberg XXZ Spin Chain:
   H = J * sum_{i=0}^{N-2} (X_i X_{i+1} + Y_i Y_{i+1} + Delta * Z_i Z_{i+1}) + h * sum_{i=0}^{N-1} Z_i
"""

import numpy as np
from typing import List, Tuple
from qiskit.quantum_info import SparsePauliOp, Pauli

def get_tfim_pauli_op(num_spins: int, J: float = 1.0, h: float = 1.0, periodic: bool = False) -> SparsePauliOp:
    """
    Constructs the 1D Transverse-Field Ising Model Hamiltonian as a SparsePauliOp:
    H = - J * sum(Z_i Z_{i+1}) - h * sum(X_i)
    
    Qiskit ordering convention: qubit 0 is rightmost in the Pauli string.
    """
    pauli_list: List[Tuple[str, complex]] = []
    
    # Interaction terms: - J * Z_i Z_{i+1}
    num_interactions = num_spins if periodic else num_spins - 1
    for i in range(num_interactions):
        j = (i + 1) % num_spins
        pauli_chars = ['I'] * num_spins
        pauli_chars[i] = 'Z'
        pauli_chars[j] = 'Z'
        # Reverse string to match Qiskit's qubit ordering (qubit 0 at index -1)
        pauli_str = "".join(reversed(pauli_chars))
        pauli_list.append((pauli_str, -J))
        
    # Transverse field terms: - h * X_i
    for i in range(num_spins):
        pauli_chars = ['I'] * num_spins
        pauli_chars[i] = 'X'
        pauli_str = "".join(reversed(pauli_chars))
        pauli_list.append((pauli_str, -h))
        
    return SparsePauliOp.from_list(pauli_list).simplify()

def get_heisenberg_pauli_op(num_spins: int, J: float = 1.0, delta: float = 1.0, h: float = 0.5, periodic: bool = False) -> SparsePauliOp:
    """
    Constructs the 1D Heisenberg XXZ Spin Chain Hamiltonian:
    H = J * sum(X_i X_{i+1} + Y_i Y_{i+1} + delta * Z_i Z_{i+1}) + h * sum(Z_i)
    """
    pauli_list: List[Tuple[str, complex]] = []
    num_interactions = num_spins if periodic else num_spins - 1
    
    for i in range(num_interactions):
        j = (i + 1) % num_spins
        for term, coeff in [('X', J), ('Y', J), ('Z', J * delta)]:
            pauli_chars = ['I'] * num_spins
            pauli_chars[i] = term
            pauli_chars[j] = term
            pauli_str = "".join(reversed(pauli_chars))
            pauli_list.append((pauli_str, coeff))
            
    # Longitudinal field: h * Z_i
    for i in range(num_spins):
        pauli_chars = ['I'] * num_spins
        pauli_chars[i] = 'Z'
        pauli_str = "".join(reversed(pauli_chars))
        pauli_list.append((pauli_str, h))
        
    return SparsePauliOp.from_list(pauli_list).simplify()

def get_magnetization_ops(num_spins: int) -> List[SparsePauliOp]:
    """Returns local Z observable for each spin: <Z_i>"""
    ops = []
    for i in range(num_spins):
        chars = ['I'] * num_spins
        chars[i] = 'Z'
        pauli_str = "".join(reversed(chars))
        ops.append(SparsePauliOp.from_list([(pauli_str, 1.0)]))
    return ops

def get_correlation_ops(num_spins: int) -> List[SparsePauliOp]:
    """Returns nearest-neighbor correlation observables: <Z_i Z_{i+1}>"""
    ops = []
    for i in range(num_spins - 1):
        chars = ['I'] * num_spins
        chars[i] = 'Z'
        chars[i + 1] = 'Z'
        pauli_str = "".join(reversed(chars))
        ops.append(SparsePauliOp.from_list([(pauli_str, 1.0)]))
    return ops
