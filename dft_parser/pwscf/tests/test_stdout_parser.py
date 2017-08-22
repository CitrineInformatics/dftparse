from dft_parser.pwscf.stdout_parser import PwscfStdOutputParser


def test_simple():
    """Test that parsing simple one-line rules works"""
    parser = PwscfStdOutputParser()
    lines = """
        bravais-lattice index     =            0
        lattice parameter (alat)  =       7.1517  a.u.
        unit-cell volume          =     919.5821 (a.u.)^3
    """.split("\n")
    results = list(parser.parse(lines))
    flattened = {}
    for r in results:
        flattened.update(r)
    assert flattened["lattice parameter"] == 7.1517
    assert flattened["bravais-lattice index"] == 0
    assert flattened["unit-cell volume"] == 919.5821
    assert flattened["unit-cell volume units"] == "(a.u.)^3"


def test_parse_stress():
    """Test that parses multiple lines into a list output"""
    lines = """
                total   stress  (Ry/bohr**3)                   (kbar)     P=  -77.72
        -0.00055293   0.00000000   0.00000000        -81.34      0.00      0.00
         0.00000000  -0.00055293   0.00000000          0.00    -81.34      0.00
         0.00000000   0.00000000  -0.00047917          0.00      0.00    -70.49
      """.split("\n")
    parser = PwscfStdOutputParser()
    results = list(parser.parse(lines))
    flattened = {}
    for r in results:
        flattened.update(r)
    assert flattened["pressure"] == -77.72
    assert flattened["pressure units"] == "kbar"
    assert len(flattened["stress"]) == 3
    assert flattened["stress"][1][1] == -81.34
    assert flattened["stress units"] == "kbar"
