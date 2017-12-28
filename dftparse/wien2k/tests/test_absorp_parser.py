from dftparse.wien2k.absorp_parser import AbsorpParser


def _flatten(ds):
    """Helper to flatten a list of dictionaries"""
    res = {}
    [res.update(d) for d in ds]
    return res


def test_parse_absorp():
    """Test that the optical conductivity and absorption are parsed out correctly"""
    lines = """
    #                                                                                
    # Lorentzian broadening with gamma= 0.100000  [eV]
    # Im(epsilon) shifted by   0.0000   [eV]
    # No intraband contributions added
    #
    # optical conductivity sigma in [1 / (Ohm cm)]       absorption in [10^4 / cm)]
    #
    # Energy [eV] Re_sigma_xx   Re_sigma_zz     absorp_xx     absorp_zz
    #
       2.598690  0.264140E+04  0.184428E+04  0.272237E+02  0.212944E+02
       2.625900  0.281094E+04  0.193515E+04  0.290967E+02  0.223449E+02
       2.653110  0.296628E+04  0.202989E+04  0.309388E+02  0.234653E+02
       2.680320  0.309807E+04  0.212534E+04  0.326454E+02  0.246247E+02
       2.707530  0.320516E+04  0.221928E+04  0.341799E+02  0.257957E+02
       2.734750  0.329030E+04  0.231272E+04  0.355501E+02  0.269836E+02
    """.split("\n")
    res = _flatten(AbsorpParser().parse(lines))

    assert len(res) == 7, "Incorrect number of columns parsed"
    assert "energies" in res, "Missing energies"
    assert "wavelengths" in res, "Missing wavelengths"
    assert "Re $\sigma_{xx}$" in res, "Missing optical conductivity {xx}"
    assert "absorp$_{xx}$" in res, "Missing absorption {xx}"

    assert len(res["energies"]) == 6, "Incorrect number of energy rows parsed"
    assert len(res["Re $\sigma_{xx}$"]) == 6, "Incorrect number of Re $\sigma_{xx}$ rows parsed"
    assert len(res["absorp$_{xx}$"]) == 6, "Incorrect number of absorp$_{xx}$ rows parsed"

    assert res["energies"][2] == 2.653110, "Incorrect value"
    assert res["Re $\sigma_{zz}$"][3] == 2125.34, "Incorrect value"
    assert res["absorp$_{zz}$"][5] == 26.9836, "Incorrect value"


test_parse_absorp()
