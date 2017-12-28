from dftparse.wien2k.epsilon_parser import EpsilonParser


def _flatten(ds):
    """Helper to flatten a list of dictionaries"""
    res = {}
    [res.update(d) for d in ds]
    return res


def test_parse_epsilon():
    """Test that the optical conductivity and absorption are parsed out correctly"""
    lines = """
    #                                                                                
    # Lorentzian broadening with gamma= 0.100000  [eV]
    # Im(epsilon) shifted by   0.0000   [eV]
    # No intraband contributions added
    #
    # Energy [eV] Re_eps_xx     Im_eps_xx     Re_eps_zz     Im_eps_zz
    #
       0.312930  0.947976E+01  0.126675E+00  0.793167E+01  0.955959E-01
       0.340140  0.949118E+01  0.129200E+00  0.793985E+01  0.973574E-01
       0.367350  0.950362E+01  0.131820E+00  0.794874E+01  0.991794E-01
       0.394570  0.951710E+01  0.134541E+00  0.795838E+01  0.101066E+00
       0.421780  0.953164E+01  0.137368E+00  0.796876E+01  0.103019E+00
       0.448990  0.954726E+01  0.140309E+00  0.797991E+01  0.105043E+00
    """.split("\n")
    res = _flatten(EpsilonParser().parse(lines))

    assert len(res) == 7, "Incorrect number of columns parsed"
    assert "energies" in res, "Missing energies"
    assert "wavelengths" in res, "Missing wavelengths"
    assert "Re $\\varepsilon_{xx}$" in res, "Missing Re dielectric constant {xx}"
    assert "Im $\\varepsilon_{zz}$" in res, "Missing Im dielectric constant {zz}"

    assert len(res["energies"]) == 6, "Incorrect number of energy rows parsed"
    assert len(res["Re $\\varepsilon_{xx}$"]) == 6, "Incorrect number of Re $\\varepsilon_{xx}$ rows parsed"
    assert len(res["Im $\\varepsilon_{zz}$"]) == 6, "Incorrect number of Im $\\varepsilon_{zz}$ rows parsed"

    assert res["energies"][2] == 0.367350, "Incorrect value"
    assert res["Im $\\varepsilon_{xx}$"][3] == 0.134541, "Incorrect value"
    assert res["Re $\\varepsilon_{zz}$"][5] == 7.97991, "Incorrect value"
