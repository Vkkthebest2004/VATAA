import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QAOAAnsatz
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

def submit_hardware_job():
    print("Connecting to IBM Quantum Platform...")
    service = QiskitRuntimeService(channel="ibm_quantum_platform")
    
    # Pick least busy operational backend
    backends = service.backends(operational=True, simulator=False)
    least_busy = min(backends, key=lambda b: b.status().pending_jobs)
    print(f"Selected IBM Quantum Hardware: {least_busy.name} ({least_busy.num_qubits} qubits, {least_busy.status().pending_jobs} pending jobs)")

    # Build 6-qubit portfolio QAOA circuit (fast and clean for hardware execution)
    from qiskit.quantum_info import SparsePauliOp
    n_stocks = 6
    # Cost Hamiltonian from beginner tier
    # H_6 terms
    pauli_list = [
        ("IIIIIZ", -0.15),
        ("IIIIZI", -0.12),
        ("IIIZII", -0.18),
        ("IIZIII", -0.10),
        ("IZIIII", -0.22),
        ("ZIIIII", -0.14),
        ("IIIIZZ", 0.35),
        ("IIIZIZ", 0.28),
        ("IIZIIZ", 0.40),
        ("IZIIIZ", 0.30),
        ("ZIIIIZ", 0.25)
    ]
    cost_op = SparsePauliOp.from_list(pauli_list)
    
    qaoa = QAOAAnsatz(cost_operator=cost_op, reps=1)
    # Optimal parameters found in simulation
    bound_circuit = qaoa.assign_parameters([0.45, 0.30])
    bound_circuit.measure_all()

    print("Transpiling circuit for target architecture with optimization_level=3...")
    pm = generate_preset_pass_manager(optimization_level=3, backend=least_busy, seed_transpiler=42)
    isa_circuit = pm.run(bound_circuit)
    print(f"Transpiled circuit depth: {isa_circuit.depth()}, 2-qubit gates: {isa_circuit.count_ops().get('cz', isa_circuit.count_ops().get('ecr', 0))}")

    print("Submitting job to IBM Quantum Hardware using SamplerV2...")
    sampler = Sampler(mode=least_busy)
    sampler.options.default_shots = 1024
    
    # Enable dynamical decoupling
    try:
        sampler.options.dynamical_decoupling.enable = True
        sampler.options.dynamical_decoupling.sequence_type = "XY4"
        sampler.options.twirling.enable_gates = True
        sampler.options.twirling.enable_measure = True
    except Exception as e:
        print("Note on options:", e)

    job = sampler.run([isa_circuit])
    job_id = job.job_id()
    print("=" * 60)
    print(f"SUCCESSFULLY SUBMITTED TO REAL IBM QUANTUM HARDWARE!")
    print(f"Backend Name: {least_busy.name}")
    print(f"Job ID:       {job_id}")
    print(f"Status:       {job.status()}")
    print("=" * 60)
    
    with open("ibm_hardware_job_info.txt", "w") as f:
        f.write(f"Backend: {least_busy.name}\n")
        f.write(f"Job ID: {job_id}\n")
        f.write(f"Status: {job.status()}\n")
        f.write(f"Num Qubits: {least_busy.num_qubits}\n")
        f.write(f"Circuit Depth: {isa_circuit.depth()}\n")

    return least_busy.name, job_id

if __name__ == "__main__":
    submit_hardware_job()
