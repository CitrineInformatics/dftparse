from dftparse.vasp.outcar_parser import OutcarParser


def _flatten(ds):
    """Helper to flatten a list of dictionaries"""
    res = {}
    [res.update(d) for d in ds]
    return res


def test_parse_magnetization():
    """Test that the total magnetization parses out correctly"""
    lines = """
     eigenvalue-minimisations  :  9897
 total energy-change (2. order) :-0.2503977E-01  (-0.2503131E-01)
 number of electron      12.9999995 magnetization      -0.0000036
 augmentation part       12.9999995 magnetization      -0.0000036
    """.split("\n")
    res = _flatten(OutcarParser().parse(lines))
    assert res["total magnetization"] == -0.0000036, "Parsed the total magnetization incorrectly"
    assert res["number of electrons"] == 12.9999995, "Parsed the number of electrons incorrectly"


def test_parse_volume_of_cell():
    """Test that the volume of cell parses out correctly"""
    lines = """
 VOLUME and BASIS-vectors are now :
 -----------------------------------------------------------------------------
  energy-cutoff  :      650.00
  volume of cell :       22.75
      direct lattice vectors                 reciprocal lattice vectors
    """.split("\n")
    res = _flatten(OutcarParser().parse(lines))
    assert res["volume of cell"] == 22.75, "Parsed the volume of cell incorrectly"
