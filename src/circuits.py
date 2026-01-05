from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import StatePreparation


def ghz_3qubits(measure: bool = True) -> QuantumCircuit:
    """|GHZ> = (|000> + |111>)/sqrt(2)"""
    qc = QuantumCircuit(3, 3, name="GHZ_3")
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(1, 2)

    if measure:
        qc.barrier()
        qc.measure([0, 1, 2], [0, 1, 2])

    return qc


def w_3qubits(measure: bool = True) -> QuantumCircuit:
    """|W> = (|001> + |010> + |100>)/sqrt(3)"""
    amp = np.zeros(8, dtype=complex)
    amp[1] = 1 / np.sqrt(3)  # |001>
    amp[2] = 1 / np.sqrt(3)  # |010>
    amp[4] = 1 / np.sqrt(3)  # |100>

    prep = StatePreparation(amp)

    qc = QuantumCircuit(3, 3, name="W_3")
    qc.append(prep, [0, 1, 2])

    if measure:
        qc.barrier()
        qc.measure([0, 1, 2], [0, 1, 2])

    return qc
