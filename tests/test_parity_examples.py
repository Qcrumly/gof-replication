from src.gof_validations import State, compute_journey, journey_parity

def test_example_parity():
    # e1 * e2 * e4 → -1 with parity 1
    toks, st = compute_journey(State.unit(1), [2,4])
    assert st.kind=="scalar" and st.sign==-1
    assert journey_parity(toks, State.unit(1))==1
