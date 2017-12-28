from ..core import BlockParser


def _parse_refraction(line, lines):
    """Parse Energy [eV]  ref_ind_xx    ref_ind_zz    extinct_xx    extinct_zz"""
    # skip the first two lines after the rule line
    next(lines)
    newline = next(lines)

    energies = []
    ref_ind_xx = []
    ref_ind_zz = []
    extinct_xx = []
    extinct_zz = []

    while newline[0] != "#" and len(newline.split()) == 5:
        split_line = newline.split()

        energies.append(float(split_line[0]))
        ref_ind_xx.append(float(split_line[1]))
        ref_ind_zz.append(float(split_line[2]))
        extinct_xx.append(float(split_line[3]))
        extinct_zz.append(float(split_line[4]))

        newline = next(lines)

    return {"energies": energies, "ref_ind$_{xx}$": ref_ind_xx, "ref_ind$_{zz}$": ref_ind_zz,
            "extinct$_{xx}$": extinct_xx, "extinct$_{zz}$": extinct_zz}


base_rules = [
    (lambda x: "# Energy [eV]  ref_ind_xx    ref_ind_zz    extinct_xx    extinct_zz" in x, _parse_refraction)
]


class RefractionParser(BlockParser):
    """Parser for Wien2k's .refract file"""

    def __init__(self, rules=base_rules):
        BlockParser.__init__(self)
        for rule in rules:
            self.add_rule(rule)
