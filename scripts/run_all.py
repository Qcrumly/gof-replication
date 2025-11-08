from pathlib import Path
import argparse, json
from src.gof_validations import run_demo

parser = argparse.ArgumentParser()
parser.add_argument("--seed", type=int, default=123)
args = parser.parse_args()

res = run_demo(seed=args.seed)
out = Path("results"); out.mkdir(exist_ok=True)
Path("results/summary.json").write_text(json.dumps(res, indent=2))
print("Wrote results/summary.json")
