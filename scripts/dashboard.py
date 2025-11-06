from __future__ import annotations
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)


def _load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def build_demo_plot():
    data = _load_json(RESULTS_DIR / "summary.json")
    if not data:
        print("No summary.json available; skipping demo plot")
        return
    keys = ["lambda_hat", "p0_hat", "parity_even_frac", "alr_survivor_rate_upper_bound"]
    values = [data.get(k, float("nan")) for k in keys]
    plt.figure()
    plt.bar(keys, values)
    plt.ylabel("value")
    plt.title("Demo statistics")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(RESULTS_DIR / "dashboard_demo.png")
    plt.close()


def build_panel_plots():
    rows = []
    for path in RESULTS_DIR.glob("panel_summary_*_L*_N*.json"):
        js = _load_json(path)
        if js:
            rows.append(js)
    if not rows:
        print("No panel summaries found; skipping panel plots")
        return
    df = pd.DataFrame(rows)
    for length, subset in df.groupby("length"):
        plt.figure()
        sub_sorted = subset.sort_values("mode")
        plt.bar(sub_sorted["mode"], sub_sorted["survivor_frac"])
        plt.ylabel("survivor_frac")
        plt.title(f"Survivor fraction by mode (L={length})")
        plt.tight_layout()
        plt.savefig(RESULTS_DIR / f"dashboard_survivor_L{length}.png")
        plt.close()


if __name__ == "__main__":
    build_demo_plot()
    build_panel_plots()
    print("Dashboard images written to results/ directory")
