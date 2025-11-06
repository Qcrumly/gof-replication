from __future__ import annotations
import json
from pathlib import Path
import matplotlib.pyplot as plt

RES = Path("results")
RES.mkdir(exist_ok=True)

def _load_json(p: Path):
    try:
        return json.loads(p.read_text())
    except Exception:
        return None

def demo_plot():
    demo = _load_json(RES/"summary.json")
    if not demo:
        print("No results/summary.json found; skipping demo plot.")
        return
    keys = ["lambda_hat","p0_hat","parity_even_frac","alr_survivor_rate_upper_bound"]
    vals = [demo.get(k, float("nan")) for k in keys]
    plt.figure()
    plt.bar(range(len(keys)), vals)
    plt.xticks(range(len(keys)), keys, rotation=20)
    plt.title("Demo stats")
    plt.ylabel("value")
    plt.tight_layout()
    plt.savefig(RES/"dashboard_demo.png")
    plt.close()

def panel_plot():
    # Gather all panel_summary_*.json files
    summaries = []
    for p in RES.glob("panel_summary_*_L*_N*.json"):
        js = _load_json(p)
        if js:
            summaries.append(js)
    if not summaries:
        print("No panel summaries found; skipping panel plot.")
        return
    # Group by length and plot survivor_frac by mode
    by_length = {}
    for row in summaries:
        L = row.get("length")
        by_length.setdefault(L, []).append(row)

    for L, rows in by_length.items():
        # sort by mode for stable order
        rows.sort(key=lambda r: r.get("mode",""))
        modes = [r.get("mode","") for r in rows]
        surv  = [r.get("survivor_frac", 0.0) for r in rows]
        plt.figure()
        plt.bar(range(len(modes)), surv)
        plt.xticks(range(len(modes)), modes)
        plt.title(f"Survivor fraction by mode (L={L})")
        plt.ylabel("survivor_frac")
        plt.tight_layout()
        plt.savefig(RES/f"dashboard_survivor_L{L}.png")
        plt.close()

if __name__=="__main__":
    demo_plot()
    panel_plot()
    print("Dashboard images saved to results/*.png")
