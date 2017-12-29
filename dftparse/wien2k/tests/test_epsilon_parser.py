from dftparse.wien2k.epsilon_parser import EpsilonParser


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
    res = list(EpsilonParser().parse(lines))

    empty = True
    no_of_rows = 0
    energies = []
    re_eps_zz = []
    for dic in res:
        if len(dic) > 0:
            empty = False
            no_of_rows += 1
            assert len(dic) == 5, "Incorrect number of columns parsed"
            assert "energy" in dic, "Missing energy"
            assert "re_eps_zz" in dic, "Missing Re eps {zz}"

            energies.append(dic["energy"])
            re_eps_zz.append(dic["re_eps_zz"])

    assert 0.340140 in energies, "Missing energy value"
    assert 7.96876 in re_eps_zz, "Missing re_eps_zz value"

    if empty:
        raise ValueError("Nothing parsed from file")

    assert no_of_rows == 6, "Incorrect number of rows parsed from file"
