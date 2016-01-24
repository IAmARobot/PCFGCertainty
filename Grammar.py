from LOTlib.Grammar import Grammar

grammar = Grammar()

# shape, color, size
# DATA = image e.g., RED_TRIANGLE_LARGE
# Hypothesis: function(image) = Bool

grammar.add_rule('START', '', ['PREDICATE'], 1.0)

grammar.add_rule('START', 'True', None, 1.0)
grammar.add_rule('START', 'False', None, 1.0)

# Logical Primitives
grammar.add_rule('PREDICATE', 'and_', ['PREDICATE', 'PREDICATE'], 1.0)
grammar.add_rule('PREDICATE', 'or_', ['PREDICATE', 'PREDICATE'], 1.0)
grammar.add_rule('PREDICATE', 'not_', ['PREDICATE'], 1.0)

# Color Primitives
grammar.add_rule('PREDICATE', 'red_', ['IMG'], 1.0)
grammar.add_rule('PREDICATE', 'green_', ['IMG'], 1.0)

# Shape Primitives
grammar.add_rule('PREDICATE', 'triangle_', ['IMG'], 1.0)
grammar.add_rule('PREDICATE', 'square_', ['IMG'], 1.0)

# Size Primitives
grammar.add_rule('PREDICATE', 'large_', ['IMG'], 1.0)
grammar.add_rule('PREDICATE', 'small_', ['IMG'], 1.0)

if __name__ == "__main__":

    for _ in xrange(10):
        print grammar.generate()
