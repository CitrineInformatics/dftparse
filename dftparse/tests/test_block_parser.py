from dftparse.core import BlockParser


def test_multiple_parsers():
    """Test that parsers don't have interacting state"""
    rules = []
    first_parser = BlockParser(rules)
    assert len(first_parser.rules) == 0

    rules.append((lambda x: True, 1.0))
    second_parser = BlockParser(rules)
    assert len(second_parser.rules) == 1

    assert len(first_parser.rules) == 0, "Non-local mutation of a parser's rules"
