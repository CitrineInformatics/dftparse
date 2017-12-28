from ..core import BlockParser


def _parse_eloss(line, lines):
    """Parse Energy [eV]    eloss_xx      eloss_zz"""
    # skip the first two lines after the rule line
    next(lines)
    newline = next(lines)

    energies = []
    wavelengths = []
    frequencies = []
    eloss_xx = []
    eloss_zz = []

    while newline[0] != "#" and len(newline.split()) == 3:
        split_line = newline.split()

        energies.append(float(split_line[0]))
        wavelengths.append(float(split_line[0])/1240)
        frequencies.append(float(split_line[0])*2.418*10**14)

        eloss_xx.append(float(split_line[1]))
        eloss_zz.append(float(split_line[2]))

        newline = next(lines)

    return {"energies": energies, "wavelengths": wavelengths, "frequencies": frequencies,  "eloss$_{xx}$": eloss_xx,
            "eloss$_{zz}$": eloss_zz}


base_rules = [
    (lambda x: "# Energy [eV]    eloss_xx      eloss_zz" in x, _parse_eloss)
]


class ElossParser(BlockParser):
    """Parser for Wien2k's .eloss file"""

    def __init__(self, rules=base_rules):
        BlockParser.__init__(self)
        for rule in rules:
            self.add_rule(rule)
