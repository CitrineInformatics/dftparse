def _parse_lines(lines):
    for line in lines:
        if "lattice parameter" in line:
            yield {"lattice parameter": line.split()[4]}
        else:
            yield {}

def parse_stdout(lines):
    gen = _parse_lines(lines)
    return gen
