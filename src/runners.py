from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from qiskit import QuantumCircuit, transpile

# Local simulator
from qiskit_aer import AerSimulator

# IBM Cloud Runtime (V2 primitives)
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


Counts = Dict[str, int]


@dataclass(frozen=True)
class IBMConfig:
    channel: str
    token: str
    instance: str | None = None
    region: str | None = None


def run_local_aer(circuit: QuantumCircuit, shots: int = 4096, seed: int = 1234) -> Counts:
    backend = AerSimulator(seed_simulator=seed)
    tcirc = transpile(circuit, backend)
    job = backend.run(tcirc, shots=shots)
    result = job.result()
    return result.get_counts()


def _load_ibm_config_from_env() -> IBMConfig:
    channel = os.getenv("IBM_QUANTUM_CHANNEL", "ibm_quantum_platform").strip()
    token = os.getenv("IBM_QUANTUM_TOKEN", "").strip()
    instance = os.getenv("IBM_QUANTUM_INSTANCE", "").strip() or None
    region = os.getenv("IBM_QUANTUM_REGION", "").strip() or None

    if not token:
        raise RuntimeError(
            "IBM_QUANTUM_TOKEN is empty. Put your IBM Cloud API key in .env "
            "(or use QiskitRuntimeService.save_account())."
        )

    return IBMConfig(channel=channel, token=token, instance=instance, region=region)


def _init_ibm_service(cfg: IBMConfig) -> QiskitRuntimeService:
    kwargs = {"channel": cfg.channel, "token": cfg.token}
    if cfg.instance:
        kwargs["instance"] = cfg.instance
    if cfg.region:
        kwargs["region"] = cfg.region
    return QiskitRuntimeService(**kwargs)


def pick_ibm_backend(
    service: QiskitRuntimeService,
    simulator: bool = True,
    backend_name: Optional[str] = None,
    min_num_qubits: int = 3,
):
    if backend_name:
        return service.backend(backend_name)

    # Auto pick least busy backend matching criteria
    try:
        return service.least_busy(
            operational=True,
            simulator=simulator,
            min_num_qubits=min_num_qubits,
        )
    except Exception:
        # Fallback: try without simulator constraint, or get any available backend
        print(f"Warning: No backend found with simulator={simulator}. Trying fallback...")
        try:
            # Try getting available backends without simulator filter
            backends = service.backends(operational=True, min_num_qubits=min_num_qubits)
            if backends:
                backend = backends[0]
                print(f"Using fallback backend: {backend.name}")
                return backend
        except Exception:
            pass
        
        # Last resort: get any backend that's available
        all_backends = service.backends()
        if all_backends:
            backend = all_backends[0]
            print(f"Using last resort backend: {backend.name}")
            return backend
        
        raise RuntimeError(
            "No backends available. Check your IBM Quantum account and instance. "
            "You may need to specify a backend name with --backend-name option."
        )


def run_ibm_runtime_sampler_v2(
    circuit: QuantumCircuit,
    shots: int = 4096,
    simulator: bool = True,
    backend_name: Optional[str] = None,
) -> Tuple[Counts, str]:
    """Run on IBM Quantum Platform via Qiskit Runtime (SamplerV2)."""
    cfg = _load_ibm_config_from_env()
    service = _init_ibm_service(cfg)

    backend = pick_ibm_backend(
        service=service,
        simulator=simulator,
        backend_name=backend_name,
        min_num_qubits=3,
    )

    # Transpile to the backend's ISA using preset pass manager
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pm.run(circuit)

    sampler = Sampler(backend)
    job = sampler.run([isa_circuit], shots=shots)
    result = job.result()
    pub_result = result[0]

    # Extract counts from the first classical register found with get_counts()
    data_obj = pub_result.data
    reg_names = [name for name in dir(data_obj) if not name.startswith("_")]
    for name in reg_names:
        maybe = getattr(data_obj, name, None)
        if hasattr(maybe, "get_counts"):
            counts = maybe.get_counts()
            return counts, backend.name

    raise RuntimeError(
        "Could not extract counts from SamplerV2 result. "
        "Ensure the circuit contains measurements and a classical register."
    )
