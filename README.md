# GHZ & W (3 qubits) with Qiskit + IBM Quantum (Cloud Simulation via API)

This ready-to-run project creates **GHZ** and **W** states on **3 qubits** and runs them on:
- Local simulator (Qiskit Aer)
- IBM Cloud simulator (Qiskit Runtime / SamplerV2)
- Optional: Real IBM QPU (same script, use `--real`)

## 1) Setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# edit .env and paste your IBM API key into IBM_QUANTUM_TOKEN
```

## 2) Run locally

```bash
python main.py --runner local --state all --shots 4096
```

Outputs:
- prints counts + TV distance vs theory
- saves histograms under `results/`

## 3) Run on IBM Cloud simulator (API)

```bash
python main.py --runner ibm --state all --shots 4096
```

## 4) Run on a real IBM Quantum device

```bash
python main.py --runner ibm --real --state ghz --shots 4096
```

## Notes
- If you want to force a backend: `--backend-name <backend_name>`
- Ensure your account has access to IBM Quantum / Runtime and the API key is correct.
