"""
Trotter-Suzuki product formula circuit construction for 1D spin chain evolution.
Implements:
1. 1st-Order Lie-Trotter Product Formula
2. 2nd-Order Symmetric Strang-Suzuki Splitting
3. General PauliEvolutionGate Qiskit synthesizer mapping
4. Digital Unitary Folding for Zero-Noise Extrapolation (ZNE)
"""

import numpy as np
from typing import Optional, List
from qiskit import QuantumCircuit
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.synthesis import LieTrotter, SuzukiTrotter
from qiskit.quantum_info import SparsePauliOp

def build_tfim_trotter_circuit_custom(
    num_spins: int,
    total_time: float,
    num_steps: int,
    J: float = 1.0,
    h: float = 1.0,
    order: int = 2,
    initial_state_prep: Optional[QuantumCircuit] = None,
    periodic: bool = False
) -> QuantumCircuit:
    """
    Constructs an explicit gate-level quantum circuit for TFIM time evolution
    using native CNOT, RZ, and RX gates.
    
    H = - J * sum(Z_i Z_{i+1}) - h * sum(X_i)
    Evolution operator: e^{-i H t} = (e^{-i H dt})^r with dt = t / r.
    
    - ZZ interaction: e^{-i (-J dt) Z_i Z_{i+1}} = e^{i J dt Z_i Z_{i+1}}
      Implementation: CNOT(i, j) -> RZ(-2 * J * dt, j) -> CNOT(i, j)
    - X transverse field: e^{-i (-h dt) X_i} = e^{i h dt X_i}
      Implementation: RX(-2 * h * dt, i)
    """
    dt = total_time / num_steps if num_steps > 0 else 0.0
    qc = QuantumCircuit(num_spins, name=f"TFIM_Trotter_O{order}")
    
    # 1. State preparation
    if initial_state_prep is not None:
        qc.compose(initial_state_prep, inplace=True)
    
    if num_steps == 0:
        return qc
        
    num_interactions = num_spins if periodic else num_spins - 1

    def apply_zz(sub_dt: float):
        # Even-odd coloring to allow parallelization on physical hardware
        # Even bonds (0-1, 2-3, ...)
        for i in range(0, num_interactions, 2):
            j = (i + 1) % num_spins
            qc.cx(i, j)
            qc.rz(-2.0 * J * sub_dt, j)
            qc.cx(i, j)
        # Odd bonds (1-2, 3-4, ...)
        for i in range(1, num_interactions, 2):
            j = (i + 1) % num_spins
            qc.cx(i, j)
            qc.rz(-2.0 * J * sub_dt, j)
            qc.cx(i, j)

    def apply_x(sub_dt: float):
        for i in range(num_spins):
            qc.rx(-2.0 * h * sub_dt, i)

    # Trotter steps
    for step in range(num_steps):
        if order == 1:
            # 1st-order: e^{-i H dt} ~ e^{-i H_ZZ dt} e^{-i H_X dt}
            apply_zz(dt)
            apply_x(dt)
        elif order == 2:
            # 2nd-order (Symmetric): e^{-i H_X dt/2} e^{-i H_ZZ dt} e^{-i H_X dt/2}
            apply_x(dt / 2.0)
            apply_zz(dt)
            apply_x(dt / 2.0)
        else:
            raise ValueError(f"Unsupported Trotter order: {order}. Choose 1 or 2.")
            
    return qc

def build_qiskit_synthesis_circuit(
    hamiltonian_op: SparsePauliOp,
    total_time: float,
    num_steps: int,
    order: int = 2,
    initial_state_prep: Optional[QuantumCircuit] = None
) -> QuantumCircuit:
    """
    Constructs a Trotter circuit using Qiskit's built-in PauliEvolutionGate
    and LieTrotter (order 1) or SuzukiTrotter (order 2).
    """
    num_qubits = hamiltonian_op.num_qubits
    qc = QuantumCircuit(num_qubits, name=f"Qiskit_Synth_O{order}")
    
    if initial_state_prep is not None:
        qc.compose(initial_state_prep, inplace=True)
        
    if num_steps > 0:
        synth = LieTrotter(reps=num_steps) if order == 1 else SuzukiTrotter(order=2, reps=num_steps)
        evo_gate = PauliEvolutionGate(hamiltonian_op, time=total_time, synthesis=synth)
        qc.append(evo_gate, range(num_qubits))
        
    return qc

def fold_circuit_globally(circuit: QuantumCircuit, scale_factor: int) -> QuantumCircuit:
    """
    Performs global digital unitary folding for Zero-Noise Extrapolation (ZNE).
    Given scale factor lambda = 1 + 2n (e.g. 1, 3, 5), transforms circuit U into:
    U_folded = U (U^dagger U)^n.
    
    Preserves exact ideal unitary evolution (since U^dagger U = I),
    but scales effective hardware noise/gate count by lambda.
    """
    if scale_factor % 2 == 0 or scale_factor < 1:
        raise ValueError(f"Scale factor must be an odd positive integer (1, 3, 5, ...), got {scale_factor}")
        
    num_folds = (scale_factor - 1) // 2
    if num_folds == 0:
        return circuit.copy()
        
    inv_circuit = circuit.inverse()
    folded_qc = circuit.copy()
    for _ in range(num_folds):
        folded_qc.compose(inv_circuit, inplace=True)
        folded_qc.compose(circuit, inplace=True)
        
    folded_qc.name = f"{circuit.name}_folded_scale_{scale_factor}"
    return folded_qc

def fold_two_qubit_gates(circuit: QuantumCircuit, scale_factor: int) -> QuantumCircuit:
    """
    Performs local gate folding on two-qubit CNOT gates (the primary noise source on NISQ hardware).
    For each CNOT gate, replaces CNOT -> CNOT (CNOT CNOT)^n.
    """
    if scale_factor % 2 == 0 or scale_factor < 1:
        raise ValueError(f"Scale factor must be an odd positive integer, got {scale_factor}")
    num_folds = (scale_factor - 1) // 2
    if num_folds == 0:
        return circuit.copy()
        
    folded = QuantumCircuit(circuit.num_qubits, circuit.num_clbits)
    for instruction in circuit.data:
        folded.append(instruction)
        if instruction.operation.name == 'cx':
            q_ctrl, q_tgt = instruction.qubits
            for _ in range(num_folds):
                folded.cx(q_ctrl, q_tgt)
                folded.cx(q_ctrl, q_tgt)
                
    folded.name = f"{circuit.name}_cx_folded_scale_{scale_factor}"
    return folded
