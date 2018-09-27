from ..core import BlockParser


def _parse_eloss(line, lines):
    """Parse Energy [eV]    eloss_xx      eloss_zz"""

    split_line = line.split()

    energy = float(split_line[0])
    eloss_xx = float(split_line[1])
    eloss_zz = float(split_line[2])

    return {"energy": energy, "eloss_xx": eloss_xx, "eloss_zz": eloss_zz}


base_rules = [
    (lambda x: len(x) > 0 and "#" not in x and len(x.split()) == 3, _parse_eloss)
]


class ElossParser(BlockParser):
    """Parser for Wien2k's .eloss file"""

    def __init__(self, rules=base_rules):
        BlockParser.__init__(self)
        for rule in rules:
            self.add_rule(rule)
