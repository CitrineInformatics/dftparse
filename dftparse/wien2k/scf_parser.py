from ..core import BlockParser


def _parse_total_energy(line, lines):
    total_energy = float(line[43:59])
    return {
        'total energy': total_energy,
        'total energy units': "Ry"
    }


base_rules = [
    (lambda x: ":ENE" in x, _parse_total_energy)
]


class ScfParser(BlockParser):
    """Parser for Wien2k's .scf file"""

    def __init__(self, rules=base_rules):
        BlockParser.__init__(self)
        for rule in rules:
            self.add_rule(rule)
