from ..core import BlockParser


def _parse_absorption(line, lines):
    """Parse Energy, Re sigma xx, Re sigma zz, absorp xx, absorp zz"""

    split_line = line.split()

    energy = float(split_line[0])
    re_sigma_xx = float(split_line[1])
    re_sigma_zz = float(split_line[2])
    absorp_xx = float(split_line[3])
    absorp_zz = float(split_line[4])

    return {"energy": energy, "re_sigma_xx": re_sigma_xx, "re_sigma_zz": re_sigma_zz,
            "absorp_xx": absorp_xx, "absorp_zz": absorp_zz}


base_rules = [
    (lambda x: len(x) > 0 and "#" not in x and len(x.split()) == 5, _parse_absorption)
]


class AbsorpParser(BlockParser):
    """Parser for Wien2k's .absorp file"""

    def __init__(self, rules=base_rules):
        BlockParser.__init__(self)
        for rule in rules:
            self.add_rule(rule)
