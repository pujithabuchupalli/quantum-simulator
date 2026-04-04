"""Quantum backend operations for bit-flip error correction"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from config import DEFAULT_SHOTS


def run_bitflip_qec(logical_state="0", error_qubit=None, shots=DEFAULT_SHOTS):
    """
    Run bit-flip quantum error correction simulation
    
    Args:
        logical_state (str): Initial logical state ("0" or "1")
        error_qubit (int): Which qubit to introduce error to (0, 1, 2, or None)
        shots (int): Number of simulation shots
        
    Returns:
        tuple: (qc_encode, qc_error, qc_full, counts, fidelity, error_info)
    """
    # Encoding circuit
    qc_encode = QuantumCircuit(3, 1)
    if logical_state == "1":
        qc_encode.x(0)
    qc_encode.cx(0, 1)
    qc_encode.cx(0, 2)

    # Error circuit
    qc_error = qc_encode.copy()
    error_info = "No error introduced"
    if error_qubit in [0, 1, 2]:
        qc_error.x(error_qubit)
        error_info = f"Bit-flip error in qubit {error_qubit}"

    # Full correction circuit
    qc_full = qc_error.copy()
    qc_full.cx(0, 1)
    qc_full.cx(0, 2)
    qc_full.ccx(1, 2, 0)
    qc_full.measure(0, 0)

    # Simulation
    simulator = AerSimulator()
    compiled = transpile(qc_full, simulator)
    result = simulator.run(compiled, shots=shots).result()
    counts = result.get_counts()
    fidelity = counts.get("0", 0) / shots if logical_state == "0" else counts.get("1", 0) / shots

    return qc_encode, qc_error, qc_full, counts, fidelity, error_info


def calculate_fidelity(counts, logical_state, shots):
    """
    Calculate the fidelity of the quantum operation
    
    Args:
        counts (dict): Measurement counts from simulation
        logical_state (str): Expected logical state ("0" or "1")
        shots (int): Total number of shots
        
    Returns:
        float: Fidelity value between 0 and 1
    """
    expected_state = "0" if logical_state == "0" else "1"
    return counts.get(expected_state, 0) / shots
