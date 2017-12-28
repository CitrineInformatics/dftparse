from dftparse.wien2k.eloss_parser import ElossParser


def _flatten(ds):
    """Helper to flatten a list of dictionaries"""
    res = {}
    [res.update(d) for d in ds]
    return res


def test_parse_eloss():
    """Test that the optical conductivity and absorption are parsed out correctly"""
    lines = """
    #                                                                                
    # Lorentzian broadening with gamma= 0.100000  [eV]
    # Im(epsilon) shifted by   0.0000   [eV]
    # No intraband contributions added
    #
    # Energy [eV]    eloss_xx      eloss_zz
    #       
       0.530620  0.162573E-02  0.173530E-02
       0.557830  0.165644E-02  0.176554E-02
       0.585040  0.168814E-02  0.179664E-02
       0.612260  0.172092E-02  0.182867E-02
       0.639470  0.175483E-02  0.186166E-02
       0.666680  0.178998E-02  0.189568E-02
    """.split("\n")
    res = _flatten(ElossParser().parse(lines))

    assert len(res) == 5, "Incorrect number of columns parsed"
    assert "energies" in res, "Missing energies"
    assert "wavelengths" in res, "Missing wavelengths"
    assert "eloss$_{xx}$" in res, "Missing eloss {xx}"
    assert "eloss$_{zz}$" in res, "Missing eloss {zz}"

    assert len(res["energies"]) == 6, "Incorrect number of energy rows parsed"
    assert len(res["eloss$_{xx}$"]) == 6, "Incorrect number of eloss$_{xx}$ rows parsed"
    assert len(res["eloss$_{zz}$"]) == 6, "Incorrect number of eloss$_{zz}$ rows parsed"

    assert res["energies"][2] == 0.585040, "Incorrect value"
    assert res["eloss$_{xx}$"][3] == 0.00172092, "Incorrect value"
    assert res["eloss$_{zz}$"][5] == 0.00189568, "Incorrect value"
