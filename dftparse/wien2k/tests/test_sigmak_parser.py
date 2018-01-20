from dftparse.wien2k.sigmak_parser import SigmakParser


def test_parse_sigmak():
    """Test that the optical conductivity and absorption are parsed out correctly"""
    lines = """
    #                                                                                
    # Lorentzian broadening with gamma= 0.100000  [eV]
    # Im(epsilon) shifted by   0.0000   [eV]
    # No intraband contributions added
    #
    # optical conductivity sigma in [10^15 / sec]
    #
    # Energy [eV] Re_sigma_xx   Im_sigma_xx   Re_sigma_zz   Im_sigma_zz
    #
       1.537440  0.206674E+00 -0.217258E+01  0.978155E-01 -0.176002E+01
       2.544270  0.207954E+01 -0.384535E+01  0.151224E+01 -0.308459E+01
       5.265400  0.781662E+01 -0.360693E+01  0.473580E+01 -0.270977E+01
       7.578370  0.646808E+01  0.128851E+01  0.613028E+01  0.666280E+00
      10.544420  0.424403E+01  0.273408E+01  0.422050E+01  0.275269E+01
      13.211130  0.141364E+01  0.279121E+01  0.184177E+01  0.316581E+01
    """.split("\n")
    res = list(SigmakParser().parse(lines))

    empty = True
    no_of_rows = 0
    energies = []
    re_sigma_zz = []
    for dic in res:
        if len(dic) > 0:
            empty = False
            no_of_rows += 1
            assert len(dic) == 5, "Incorrect number of columns parsed"
            assert "energy" in dic, "Missing energy"
            assert "re_sigma_zz" in dic, "Missing Re optical conductivity {zz}"
            assert "im_sigma_xx" in dic, "Missing Im optical conductivity {xx}"

            energies.append(dic["energy"])
            re_sigma_zz.append(dic["re_sigma_zz"])

    assert 5.2654 in energies, "Missing energy value"
    assert 4.2205 in re_sigma_zz, "Missing re_sigma_zz value"

    if empty:
        raise ValueError("Nothing parsed from file")

    assert no_of_rows == 6, "Incorrect number of rows parsed from file"
