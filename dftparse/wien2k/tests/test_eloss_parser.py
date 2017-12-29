from dftparse.wien2k.eloss_parser import ElossParser


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
    res = list(ElossParser().parse(lines))

    empty = True
    no_of_rows = 0
    energies = []
    eloss_xx = []
    for dic in res:
        if len(dic) > 0:
            empty = False
            no_of_rows += 1
            assert len(dic) == 3, "Incorrect number of columns parsed"
            assert "energy" in dic, "Missing energy"
            assert "eloss$_{xx}$" in dic, "Missing optical conductivity {xx}"

            energies.append(dic["energy"])
            eloss_xx.append(dic["eloss$_{xx}$"])

    assert 0.666680 in energies, "Missing energy value"
    assert 0.00178998 in eloss_xx, "Missing eloss_xx value"

    if empty:
        raise ValueError("Nothing parsed from file")

    assert no_of_rows == 6, "Incorrect number of rows parsed from file"
