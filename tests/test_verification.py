"""Run verification scripts as tests."""
import subprocess
import sys

def test_exact_formula_check():
    result = subprocess.run([sys.executable, "verification/exact_formula_check.py"], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr

def test_associator_check():
    result = subprocess.run([sys.executable, "verification/associator_check.py"], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr

def test_replay_logs():
    result = subprocess.run([sys.executable, "verification/replay_logs.py"], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr

# NOTE: exact_formula_verify.py is NOT included here because it's exhaustive
# and takes a long time (7^8 = 5.7M chains). Run it manually:
#   python verification/exact_formula_verify.py
