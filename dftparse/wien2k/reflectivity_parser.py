from ..core import BlockParser


def _parse_reflectivity(line, lines):
    """Parse Energy [eV]  reflect_xx    reflect_zz"""

    split_line = line.split()

    energy = float(split_line[0])
    reflect_xx = float(split_line[1])
    reflect_zz = float(split_line[2])

    return {"energy": energy, "reflect_xx": reflect_xx, "reflect_zz": reflect_zz}


base_rules = [
    (lambda x: len(x) > 0 and "#" not in x and len(x.split()) == 3, _parse_reflectivity)
]


class ReflectivityParser(BlockParser):
    """Parser for Wien2k's .reflectivity file"""

    def __init__(self, rules=base_rules):
        BlockParser.__init__(self)
        for rule in rules:
            self.add_rule(rule)
