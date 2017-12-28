from dftparse.wien2k.reflectivity_parser import ReflectivityParser


def _flatten(ds):
    """Helper to flatten a list of dictionaries"""
    res = {}
    [res.update(d) for d in ds]
    return res


def test_parse_reflectivity():
    """Test that the optical conductivity and absorption are parsed out correctly"""
    lines = """
    #                                                                                
    # Lorentzian broadening with gamma= 0.100000  [eV]
    # Im(epsilon) shifted by   0.0000   [eV]
    # No intraband contributions added
    #
    # Energy [eV]  reflect_xx    reflect_zz
    #
       0.367350  0.260272E+00  0.226934E+00
       0.394570  0.260540E+00  0.227158E+00
       0.421780  0.260829E+00  0.227399E+00
       0.448990  0.261140E+00  0.227657E+00
       0.476200  0.261472E+00  0.227933E+00
       0.503410  0.261825E+00  0.228227E+00
    """.split("\n")
    res = _flatten(ReflectivityParser().parse(lines))

    assert len(res) == 5, "Incorrect number of columns parsed"
    assert "energies" in res, "Missing energies"
    assert "wavelengths" in res, "Missing wavelengths"
    assert "reflect$_{xx}$" in res, "Missing reflect {xx}"
    assert "reflect$_{zz}$" in res, "Missing reflect {zz}"

    assert len(res["energies"]) == 6, "Incorrect number of energy rows parsed"
    assert len(res["reflect$_{xx}$"]) == 6, "Incorrect number of reflect$_{xx}$ rows parsed"
    assert len(res["reflect$_{zz}$"]) == 6, "Incorrect number of reflect$_{zz}$ rows parsed"

    assert res["energies"][2] == 0.421780, "Incorrect value"
    assert res["reflect$_{xx}$"][3] == 0.261140, "Incorrect value"
    assert res["reflect$_{zz}$"][5] == 0.228227, "Incorrect value"
