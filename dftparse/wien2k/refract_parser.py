from ..core import BlockParser


def _parse_refraction(line, lines):
    """Parse Energy [eV]  ref_ind_xx    ref_ind_zz    extinct_xx    extinct_zz"""
    split_line = line.split()

    energy = float(split_line[0])
    ref_ind_xx = float(split_line[1])
    ref_ind_zz = float(split_line[2])
    extinct_xx = float(split_line[3])
    extinct_zz = float(split_line[4])

    return {"energy": energy, "ref_ind_xx": ref_ind_xx, "ref_ind_zz": ref_ind_zz, "extinct_xx": extinct_xx,
            "extinct_zz": extinct_zz}


base_rules = [
    (lambda x: len(x) > 0 and "#" not in x and len(x.split()) == 5, _parse_refraction)
]


class RefractionParser(BlockParser):
    """Parser for Wien2k's .refract file"""

    def __init__(self, rules=base_rules):
        BlockParser.__init__(self)
        for rule in rules:
            self.add_rule(rule)
