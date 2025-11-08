from __future__ import annotations
import json
from pathlib import Path

RES = Path("results")
RES.mkdir(exist_ok=True)

def _load_json(p: Path):
    try:
        return json.loads(p.read_text())
    except Exception:
        return None

def _try_import_matplotlib():
    try:
        import matplotlib.pyplot as plt  # local, optional
        return plt
    except Exception:
        return None

def demo_plot():
    demo = _load_json(RES/"summary.json")
    if not demo:
        print("No results/summary.json found; skipping demo plot.")
        return
    plt = _try_import_matplotlib()
    keys = ["lambda_hat","p0_hat","parity_even_frac","alr_survivor_rate_upper_bound"]
    vals = [demo.get(k, float("nan")) for k in keys]
    if plt is None:
        # Text fallback
        (RES/"dashboard_demo.txt").write_text(
            "Demo stats\n" + "\n".join(f"{k}: {v}" for k,v in zip(keys, vals)),
            encoding="utf-8"
        )
        print("Matplotlib not available; wrote results/dashboard_demo.txt")
        return
    # Plot
    plt.figure()
    plt.bar(range(len(keys)), vals)
    plt.xticks(range(len(keys)), keys, rotation=20)
    plt.title("Demo stats")
    plt.ylabel("value")
    plt.tight_layout()
    plt.savefig(RES/"dashboard_demo.png")
    plt.close()

def panel_plot():
    summaries = []
    for p in RES.glob("panel_summary_*_L*_N*.json"):
        js = _load_json(p)
        if js: summaries.append(js)
    if not summaries:
        print("No panel summaries found; skipping panel plot.")
        return
    # group by length
    by_length = {}
    for row in summaries:
        L = row.get("length")
        by_length.setdefault(L, []).append(row)

    for L, rows in by_length.items():
        rows.sort(key=lambda r: r.get("mode",""))
        modes = [r.get("mode","") for r in rows]
        surv  = [r.get("survivor_frac", 0.0) for r in rows]

        plt = _try_import_matplotlib()
        if plt is None:
            # Text fallback
            lines = [f"Panel summary (L={L})"] + [f"{m}: survivor_frac={s}" for m,s in zip(modes, surv)]
            (RES/f"dashboard_survivor_L{L}.txt").write_text("\n".join(lines), encoding="utf-8")
            print(f"Matplotlib not available; wrote results/dashboard_survivor_L{L}.txt")
            continue

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
    print("Dashboard complete (PNG if matplotlib available; else .txt summaries).")
