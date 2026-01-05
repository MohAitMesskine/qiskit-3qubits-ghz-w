from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace, entropy


Counts = Dict[str, int]


@dataclass(frozen=True)
class Comparison:
    expected_probs: Dict[str, float]
    measured_probs: Dict[str, float]
    tv_distance: float  # total variation distance


def counts_to_probs(counts: Counts) -> Dict[str, float]:
    total = sum(counts.values())
    if total == 0:
        return {}
    return {k: v / total for k, v in counts.items()}


def expected_distribution(state: str) -> Dict[str, float]:
    state = state.lower()
    if state == "ghz":
        return {"000": 0.5, "111": 0.5}
    if state == "w":
        return {"001": 1 / 3, "010": 1 / 3, "100": 1 / 3}
    raise ValueError("state must be 'ghz' or 'w'")


def total_variation_distance(p: Dict[str, float], q: Dict[str, float]) -> float:
    keys = set(p) | set(q)
    return 0.5 * sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in keys)


def compare_to_theory(state: str, counts: Counts) -> Comparison:
    exp = expected_distribution(state)
    meas = counts_to_probs(counts)
    tvd = total_variation_distance(exp, meas)
    return Comparison(expected_probs=exp, measured_probs=meas, tv_distance=tvd)


def ideal_entanglement_report(circuit_without_measure: QuantumCircuit) -> Dict[str, float]:
    """Bonus: von Neumann entropy S(rho_qubit_i) for each single qubit."""
    sv = Statevector.from_instruction(circuit_without_measure)
    dm = DensityMatrix(sv)

    entropies = {}
    for i in range(3):
        reduced = partial_trace(dm, [q for q in range(3) if q != i])
        entropies[f"S(qubit_{i})"] = float(entropy(reduced, base=2))
    return entropies
