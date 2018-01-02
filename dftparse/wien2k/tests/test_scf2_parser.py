from dftparse.wien2k.scf2_parser import Scf2Parser


def _flatten(ds):
    """Helper to flatten a list of dictionaries"""
    res = {}
    [res.update(d) for d in ds]
    return res


def test_parse_bandgap():
    """Test that the total magnetization parses out correctly"""
    lines = """
           Insulator, EF-inconsistency corrected
    :GAP (global)   :    0.0521 Ry =     0.709 eV (accurate value if proper k-mesh)
    :GAP (this spin):    0.0521 Ry =     0.709 eV (accurate value if proper k-mesh)
             Bandranges (emin - emax) and occupancy:
    :BAN00078:  78    0.500479    0.540403  1.00000000
    """.split("\n")
    res = _flatten(Scf2Parser().parse(lines))
    assert res["band gap"] == 0.709, "Parsed the band gap incorrectly"
    assert res["band gap units"] == "eV", "Incorrect units for band gap"
