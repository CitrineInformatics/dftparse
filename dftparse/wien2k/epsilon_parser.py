from ..core import BlockParser


def _parse_epsilon(line, lines):
    """Parse Energy [eV] Re_eps_xx     Im_eps_xx     Re_eps_zz     Im_eps_zz"""
    # skip the first two lines after the rule line
    next(lines)
    newline = next(lines)

    energies = []
    re_eps_xx = []
    im_eps_xx = []
    re_eps_zz = []
    im_eps_zz = []

    while newline[0] != "#" and len(newline.split()) == 5:
        split_line = newline.split()

        energies.append(float(split_line[0]))
        re_eps_xx.append(float(split_line[1]))
        im_eps_xx.append(float(split_line[2]))
        re_eps_zz.append(float(split_line[3]))
        im_eps_zz.append(float(split_line[4]))

        newline = next(lines)

    return {"energies": energies, "Re $\\varepsilon_{xx}$": re_eps_xx, "Im $\\varepsilon_{xx}$": im_eps_xx,
            "Re $\\varepsilon_{zz}$": re_eps_zz, "Im $\\varepsilon_{zz}$": im_eps_zz}


base_rules = [
    (lambda x: "# Energy [eV] Re_eps_xx     Im_eps_xx     Re_eps_zz     Im_eps_zz" in x, _parse_epsilon)
]


class EpsilonParser(BlockParser):
    """Parser for Wien2k's .epsilon file"""

    def __init__(self, rules=base_rules):
        BlockParser.__init__(self)
        for rule in rules:
            self.add_rule(rule)
