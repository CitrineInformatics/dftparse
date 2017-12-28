from ..core import BlockParser


def _parse_absorption(line, lines):
    """Parse Energy, Re sigma xx, Re sigma zz, absorp xx, absorp zz"""
    # skip the first two lines after the rule line
    # next(lines)
    # newline = next(lines)

    newline = line

    energies = []
    re_sigma_xx = []
    re_sigma_zz = []
    absorp_xx = []
    absorp_zz = []

    while newline[0] != "#" and len(newline.split()) == 5:
        split_line = newline.split()

        energies.append(float(split_line[0]))
        re_sigma_xx.append(float(split_line[1]))
        re_sigma_zz.append(float(split_line[2]))
        absorp_xx.append(float(split_line[3]))
        absorp_zz.append(float(split_line[4]))

        newline = next(lines)

    return {"energies": energies, "Re $\sigma_{xx}$": re_sigma_xx, "Re $\sigma_{zz}$": re_sigma_zz,
            "absorp$_{xx}$": absorp_xx, "absorp$_{zz}$": absorp_zz}


base_rules = [
    (lambda x: len(x) > 0 and x.split()[0] != "#" and len(x.split()) == 5, _parse_absorption)
]


class AbsorpParser(BlockParser):
    """Parser for Wien2k's .absorp file"""

    def __init__(self, rules=base_rules):
        BlockParser.__init__(self)
        for rule in rules:
            self.add_rule(rule)
