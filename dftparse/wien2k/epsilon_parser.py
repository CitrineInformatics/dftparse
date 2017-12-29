from ..core import BlockParser


def _parse_epsilon(line, lines):
    """Parse Energy [eV] Re_eps_xx     Im_eps_xx     Re_eps_zz     Im_eps_zz"""

    split_line = line.split()

    energy = float(split_line[0])
    re_eps_xx = float(split_line[1])
    im_eps_xx = float(split_line[2])
    re_eps_zz = float(split_line[3])
    im_eps_zz = float(split_line[4])

    return {"energy": energy, "re_eps_xx": re_eps_xx, "im_eps_xx": im_eps_xx, "re_eps_zz": re_eps_zz,
            "im_eps_zz": im_eps_zz}


base_rules = [
    (lambda x: len(x) > 0 and "#" not in x and len(x.split()) == 5, _parse_epsilon)
]


class EpsilonParser(BlockParser):
    """Parser for Wien2k's .epsilon file"""

    def __init__(self, rules=base_rules):
        BlockParser.__init__(self)
        for rule in rules:
            self.add_rule(rule)
