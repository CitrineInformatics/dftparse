from dft_parser.pwscf.stdout_parser import parse_stdout

def test_alat():
    lines = []
    lines.append(" bravais-lattice index     =            0")
    lines.append(" lattice parameter (alat)  =       7.1517  a.u.")
    lines.append(" unit-cell volume          =     919.5821 (a.u.)^3")
    results = parse_stdout(lines)
    assert any(["lattice parameter" in d for d in results]), "Couldn't find 'lattice parameter' in output"

