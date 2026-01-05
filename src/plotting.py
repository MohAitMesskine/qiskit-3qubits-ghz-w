from __future__ import annotations

import os
from typing import Dict

import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram


Counts = Dict[str, int]


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def save_histogram(counts: Counts, title: str, out_path: str) -> None:
    ensure_dir(os.path.dirname(out_path))
    fig = plot_histogram(counts, title=title)
    fig.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
