from ..core import BlockParser


def _is_kpoint(line):
    """Is this line the start of a new k-point block"""
    # Try to parse the k-point; false otherwise
    toks = line.split()
    # k-point header lines have 4 tokens
    if len(toks) != 4:
        return False

    try:
        # K-points are centered at the origin
        xs = [float(x) for x in toks[:3]]
        # Weights are in [0,1]
        w = float(toks[3])
        return all(abs(x) <= 0.5 for x in xs) and w >= 0.0 and w <= 1.0
    except ValueError:
        return False


def _parse_kpoint(line, lines):
    """Parse the k-point and then continue to iterate over the band energies and occupations"""
    toks = line.split()
    kpoint = [float(x) for x in toks[:3]]
    weight = float(toks[-1])
    newline = next(lines)

    bands_up = []
    occ_up = []
    bands_down = []
    occ_down = []
    ispin = None

    while len(newline.split()) > 0:
        toks = newline.split()
        if ispin is None:
            # there are two spins if there are 5 columns (two spin energies and occupancies) or
            # very probably if there are 3 columns and the last column's first value isn't 1.0
            # (which would be the occupancy of the lowest energy level)
            ispin = (len(toks) == 5) or (len(toks) == 3 and abs(float(toks[2]) - 1.0) > 1.0e-4)

        if len(toks) == 2:
            bands_up.append(float(toks[1]))
        elif len(toks) == 3 and not ispin:
            bands_up.append(float(toks[1]))
            occ_up.append(float(toks[2]))
        elif len(toks) == 3 and ispin:
            bands_up.append(float(toks[1]))
            bands_down.append(float(toks[2]))
        elif len(toks) == 5 and ispin:
            bands_up.append(float(toks[1]))
            bands_down.append(float(toks[2]))
            occ_up.append(float(toks[3]))
            occ_down.append(float(toks[4]))
        else:
            raise ValueError("Encountered {} when parsing k-point".format(newline))
        newline = next(lines)

    res = {"kpoint": kpoint, "weight": weight}
    if len(bands_down) > 0:
        res["energies"] = list(zip(bands_up, bands_down))
    else:
        res["energies"] = list(zip(bands_up))

    if len(occ_down) > 0:
        res["occupancies"] = list(zip(occ_up, occ_down))
    elif len(occ_up) > 0:
        res["occupancies"] = list(zip(occ_up))
      
    return res

# The only rule pulls out k-points and the energies (and optionally occupations) at them
base_rules = [
  (_is_kpoint, _parse_kpoint)
]

class EigenvalParser(BlockParser):
    """Parser for VASP's EIGENVAL files"""
    def __init__(self, rules=base_rules):
        BlockParser.__init__(self)
        for rule in rules:
            self.add_rule(rule)

