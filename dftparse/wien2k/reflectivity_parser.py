from ..core import BlockParser


def _parse_reflectivity(line, lines):
    """Parse Energy [eV]  reflect_xx    reflect_zz"""
    # skip the first two lines after the rule line
    next(lines)
    newline = next(lines)

    energies = []
    wavelengths = []
    frequencies = []
    reflect_xx = []
    reflect_zz = []

    while newline[0] != "#" and len(newline.split()) == 3:
        split_line = newline.split()

        energies.append(float(split_line[0]))
        wavelengths.append(float(split_line[0])/1240)
        frequencies.append(float(split_line[0])*2.418*10**14)

        reflect_xx.append(float(split_line[1]))
        reflect_zz.append(float(split_line[2]))

        newline = next(lines)

    return {"energies": energies, "wavelengths": wavelengths, "frequencies": frequencies,  "reflect$_{xx}$": reflect_xx,
            "reflect$_{zz}$": reflect_zz}


base_rules = [
    (lambda x: "# Energy [eV]  reflect_xx    reflect_zz" in x, _parse_reflectivity)
]


class ReflectivityParser(BlockParser):
    """Parser for Wien2k's .absorp file"""

    def __init__(self, rules=base_rules):
        BlockParser.__init__(self)
        for rule in rules:
            self.add_rule(rule)
