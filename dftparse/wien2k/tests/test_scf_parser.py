from dftparse.wien2k.scf_parser import ScfParser


def _flatten(ds):
    """Helper to flatten a list of dictionaries"""
    res = {}
    [res.update(d) for d in ds]
    return res


def test_parse_energy():
    """Test that the total magnetization parses out correctly"""
    lines = """
    :PTO013:     -1   -1   -3  1.34800396E-02  5.121E-04  8.973E-04
    
    :ENE  : ********** TOTAL ENERGY IN Ry =       -94844.23535782
    
           TOTAL FORCE IN mRy/a.u. = |F|     Fx             Fy             Fz     with/without FOR in case.in2
    :FOR001:   1.ATOM         13.660          0.000          0.000        -13.660 partial forces
    """.split("\n")
    res = _flatten(ScfParser().parse(lines))
    assert res["total energy"] == -94844.23, "Parsed the total energy incorrectly"
