from ..core import BlockParser


def _parse_total_magnetization(line, lines):
    """Parse the total magnetization, which is somewhat hidden"""
    toks = line.split()
    res = {"number of electrons": float(toks[3])}
    if len(toks) > 5:
        res["total magnetization"] = float(toks[5])
    return res

base_rules = [
    (lambda x: " number of electron " in x, _parse_total_magnetization)
]


class OutcarParser(BlockParser):
    """Parser for VASP's OUTCAR file"""

    def __init__(self, rules=base_rules):
        BlockParser.__init__(self)
        for rule in rules:
            self.add_rule(rule)
