from src.gof_validations import build_tables, multiply_units

def test_basics():
    D,R,S = build_tables()
    assert D[1][1]==0 and R[0][1][1]==0 and S[0][1][1]==-1
    assert D[1][2]==D[2][1]==1
    assert R[1][1][2]==R[1][2][1]==4
    assert S[1][1][2]==+1 and S[1][2][1]==-1

def test_forward_backward():
    s,k = multiply_units(1,2)  # +e4
    assert (s,k)==(+1,4)
    s,k = multiply_units(2,1)  # -e4
    assert (s,k)==(-1,4)
