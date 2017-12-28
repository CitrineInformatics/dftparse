from dftparse.wien2k.refract_parser import RefractionParser


def _flatten(ds):
    """Helper to flatten a list of dictionaries"""
    res = {}
    [res.update(d) for d in ds]
    return res


def test_parse_refraction():
    """Test that the optical conductivity and absorption are parsed out correctly"""
    lines = """
    #                                                                                
    # Lorentzian broadening with gamma= 0.100000  [eV]
    # Im(epsilon) shifted by   0.0000   [eV]
    # No intraband contributions added
    #
    # Energy [eV]  ref_ind_xx    ref_ind_zz    extinct_xx    extinct_zz
    #
       0.312930  0.307899E+01  0.281637E+01  0.205709E-01  0.169715E-01
       0.340140  0.308085E+01  0.281783E+01  0.209682E-01  0.172753E-01
       0.367350  0.308287E+01  0.281941E+01  0.213794E-01  0.175887E-01
       0.394570  0.308506E+01  0.282112E+01  0.218053E-01  0.179124E-01
       0.421780  0.308742E+01  0.282296E+01  0.222465E-01  0.182466E-01
       0.448990  0.308995E+01  0.282493E+01  0.227042E-01  0.185921E-01
    """.split("\n")
    res = _flatten(RefractionParser().parse(lines))

    assert len(res) == 7, "Incorrect number of columns parsed"
    assert "energies" in res, "Missing energies"
    assert "wavelengths" in res, "Missing wavelengths"
    assert "ref_ind$_{xx}$" in res, "Missing ref_ind {xx}"
    assert "extinct$_{zz}$" in res, "Missing extinct {zz}"

    assert len(res["energies"]) == 6, "Incorrect number of energy rows parsed"
    assert len(res["ref_ind$_{xx}$"]) == 6, "Incorrect number of reflect$_{xx}$ rows parsed"
    assert len(res["extinct$_{zz}$"]) == 6, "Incorrect number of reflect$_{zz}$ rows parsed"

    assert res["energies"][2] == 0.367350, "Incorrect value"
    assert res["ref_ind$_{xx}$"][3] == 3.08506, "Incorrect value"
    assert res["extinct$_{zz}$"][5] == 0.0185921, "Incorrect value"
