
class BlockParser():
    """Parser built on rules that parse blocks of input"""

    def __init__(self, rules=[]):
        self.rules = rules

    def add_rule(self, rule):
        self.rules.append(rule)

    def parse(self, generator):
        gen = generator.__iter__()
        for line in gen:
            block = {}
            for rule in self.rules:
                if rule[0](line):
                    block = rule[1](line, gen)
                    break
            yield block
