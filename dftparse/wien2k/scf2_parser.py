from ..core import BlockParser


def _parse_bandgap(line, lines):
    bandgap = float(line.split()[6])
    return {
        'band gap': bandgap,
        'total energy units': "eV"
    }


base_rules = [
    (lambda x: ":GAP (global)" in x, _parse_bandgap)
]


class ScfParser(BlockParser):
    """Parser for Wien2k's .scf file"""

    def __init__(self, rules=base_rules):
        BlockParser.__init__(self)
        for rule in rules:
            self.add_rule(rule)
