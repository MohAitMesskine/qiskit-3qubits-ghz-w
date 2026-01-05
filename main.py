from __future__ import annotations

import argparse
from dotenv import load_dotenv

from src.circuits import ghz_3qubits, w_3qubits
from src.runners import run_local_aer, run_ibm_runtime_sampler_v2
from src.analysis import compare_to_theory, ideal_entanglement_report
from src.plotting import save_histogram


def parse_args():
    p = argparse.ArgumentParser(description="GHZ & W (3 qubits) with Qiskit + IBM Cloud Runtime")
    p.add_argument("--runner", choices=["local", "ibm"], default="local", help="where to run")
    p.add_argument("--state", choices=["ghz", "w", "all"], default="all", help="which state to prepare")
    p.add_argument("--shots", type=int, default=4096)
    p.add_argument("--real", action="store_true", help="IBM: use real QPU (otherwise cloud simulator)")
    p.add_argument("--backend-name", type=str, default=None, help="IBM: force a specific backend name")
    p.add_argument("--outdir", type=str, default="results", help="output folder")
    return p.parse_args()


def run_one(label: str, make_circuit_fn, args):
    qc_meas = make_circuit_fn(measure=True)
    qc_nom = make_circuit_fn(measure=False)

    if args.runner == "local":
        counts = run_local_aer(qc_meas, shots=args.shots)
        backend_used = "local_aer"
    else:
        counts, backend_used = run_ibm_runtime_sampler_v2(
            qc_meas,
            shots=args.shots,
            simulator=not args.real,
            backend_name=args.backend_name,
        )

    save_histogram(
        counts,
        title=f"{label.upper()} | backend={backend_used} | shots={args.shots}",
        out_path=f"{args.outdir}/{label}_{args.runner}_{backend_used}.png",
    )

    comp = compare_to_theory(label, counts)
    ent = ideal_entanglement_report(qc_nom)

    print("=" * 80)
    print(f"STATE: {label.upper()} | runner={args.runner} | backend={backend_used} | shots={args.shots}")
    print("Counts:", counts)
    print("Measured probabilities:", {k: round(v, 4) for k, v in comp.measured_probs.items()})
    print("Expected probabilities:", {k: round(v, 4) for k, v in comp.expected_probs.items()})
    print("Total Variation Distance (TVD):", round(comp.tv_distance, 6))
    print("Ideal entanglement (Von Neumann entropy, base 2):", {k: round(v, 6) for k, v in ent.items()})
    print(f"Histogram saved to: {args.outdir}/{label}_{args.runner}_{backend_used}.png")


def main():
    load_dotenv()
    args = parse_args()

    if args.state in ("ghz", "all"):
        run_one("ghz", ghz_3qubits, args)
    if args.state in ("w", "all"):
        run_one("w", w_3qubits, args)


if __name__ == "__main__":
    main()
