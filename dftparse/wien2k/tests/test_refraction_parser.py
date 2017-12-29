from dftparse.wien2k.refract_parser import RefractionParser


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
    res = list(RefractionParser().parse(lines))

    empty = True
    no_of_rows = 0
    energies = []
    ref_ind_zz = []
    for dic in res:
        if len(dic) > 0:
            empty = False
            no_of_rows += 1
            assert len(dic) == 5, "Incorrect number of columns parsed"
            assert "energy" in dic, "Missing energy"
            assert "ref_ind_zz" in dic, "Missing ref_ind {zz}"

            energies.append(dic["energy"])
            ref_ind_zz.append(dic["ref_ind_zz"])

    assert 0.42178 in energies, "Missing energy value"
    assert 2.82296 in ref_ind_zz, "Missing ref_ind_zz value"

    if empty:
        raise ValueError("Nothing parsed from file")

    assert no_of_rows == 6, "Incorrect number of rows parsed from file"
