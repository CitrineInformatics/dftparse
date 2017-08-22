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

def test_parse_force():
    """Test that force parsing works"""
    lines = """
        Forces acting on atoms (Ry/au):
      
        atom    1 type  1   force =     0.00000000    0.00000000    0.00000000
        atom    2 type  2   force =     0.00000000    0.00000000    0.00000054
        The non-local contrib.  to forces
        atom    1 type  1   force =     0.00000000    0.00000000    0.00000000
        atom    2 type  2   force =     0.00000000    0.00000000   -0.00000016
        The ionic contribution  to forces
        atom    1 type  1   force =     0.00000000    0.00000000    0.00000000
        atom    2 type  2   force =     0.00000000    0.00000000    0.00000000
        The local contribution  to forces
        atom    1 type  1   force =     0.00000000    0.00000000    0.00000000
        atom    2 type  2   force =     0.00000000    0.00000000    0.00000187
        The core correction contribution to forces
        atom    1 type  1   force =     0.00000000    0.00000000    0.00000000
        atom    2 type  2   force =     0.00000000    0.00000000    0.00000000
        The Hubbard contrib.    to forces
        atom    1 type  1   force =     0.00000000    0.00000000    0.00000000
        atom    2 type  2   force =     0.00000000    0.00000000    0.00000000
        The SCF correction term to forces
        atom    1 type  1   force =     0.00000000    0.00000000    0.00000000
        atom    2 type  2   force =     0.00000000    0.00000000   -0.00000117
      
        Total force =     0.011752     Total SCF correction =     0.000072
    """.split("\n") 
    parser = PwscfStdOutputParser()
    results = list(parser.parse(lines))
    flattened = {}
    for r in results:
        flattened.update(r)
    assert flattened["force units"] == "(Ry/au)"
    assert flattened["total force"] == 0.011752
    assert flattened["total SCF correction"] == 0.000072
    assert flattened["forces"][1][2] == 0.00000054 
    assert flattened["non-local contribution to forces"][1][2] == -0.00000016
    assert flattened["Atomic species index for forces"][1] == 2
