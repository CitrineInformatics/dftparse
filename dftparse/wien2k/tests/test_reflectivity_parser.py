from dftparse.wien2k.reflectivity_parser import ReflectivityParser


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
    res = list(ReflectivityParser().parse(lines))

    empty = True
    no_of_rows = 0
    energies = []
    reflect_zz = []
    for dic in res:
        if len(dic) > 0:
            empty = False
            no_of_rows += 1
            assert len(dic) == 3, "Incorrect number of columns parsed"
            assert "energy" in dic, "Missing energy"
            assert "reflect_zz" in dic, "Missing reflection {zz}"

            energies.append(dic["energy"])
            reflect_zz.append(dic["reflect_zz"])

    assert 0.44899 in energies, "Missing energy value"
    assert 0.228227 in reflect_zz, "Missing reflect_zz value"

    if empty:
        raise ValueError("Nothing parsed from file")

    assert no_of_rows == 6, "Incorrect number of rows parsed from file"
