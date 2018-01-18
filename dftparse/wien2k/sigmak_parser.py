from ..core import BlockParser


def _parse_sigmak(line, lines):
    """Parse Energy, Re sigma xx, Im sigma xx, Re sigma zz, Im sigma zz"""

    split_line = line.split()

    energy = float(split_line[0])
    re_sigma_xx = float(split_line[1])
    im_sigma_xx = float(split_line[2])
    re_sigma_zz = float(split_line[3])
    im_sigma_zz = float(split_line[4])

    return {"energy": energy, "re_sigma_xx": re_sigma_xx, "im_sigma_xx": im_sigma_xx, "re_sigma_zz": re_sigma_zz,
            "im_sigma_zz": im_sigma_zz}


base_rules = [
    (lambda x: len(x) > 0 and "#" not in x and len(x.split()) == 5, _parse_sigmak)
]


class SigmakParser(BlockParser):
    """Parser for Wien2k's .sigmak file"""

    def __init__(self, rules=base_rules):
        BlockParser.__init__(self)
        for rule in rules:
            self.add_rule(rule)
