from dftparse.wien2k.absorp_parser import AbsorpParser


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
    res = list(AbsorpParser().parse(lines))

    empty = True
    no_of_rows = 0
    energies = []
    absorp_xx = []
    for dic in res:
        if len(dic) > 0:
            empty = False
            no_of_rows += 1
            assert len(dic) == 5, "Incorrect number of columns parsed"
            assert "energy" in dic, "Missing energy"
            assert "re_sigma_xx" in dic, "Missing optical conductivity {xx}"
            assert "absorp_xx" in dic, "Missing absorption {xx}"

            energies.append(dic["energy"])
            absorp_xx.append(dic["absorp_xx"])

    assert 2.59869 in energies, "Missing energy value"
    assert 35.5501 in absorp_xx, "Missing absorp_xx value"

    if empty:
        raise ValueError("Nothing parsed from file")

    assert no_of_rows == 6, "Incorrect number of rows parsed from file"
