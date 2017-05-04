from LOTlib.Grammar import Grammar

grammar = Grammar()

# DATA = image e.g., RED_TRIANGLE_LARGE
# Hypothesis: function(image) = Bool

#grammar.add_rule('START', 'True', None, 1.0)
#grammar.add_rule('START', 'False', None, 1.0)

grammar.add_rule('START', '', ['DISJ'], 1.0)

grammar.add_rule('DISJ', '', ['CONJ'], 1.0)
grammar.add_rule('DISJ', 'or_', ['CONJ', 'DISJ'], 1.0)

grammar.add_rule('CONJ', '', ['BOOL'], 1.0)
grammar.add_rule('CONJ', 'and_', ['BOOL', 'CONJ'], 1.0)

grammar.add_rule('BOOL', '', ['PREDICATE'], 1.0)
grammar.add_rule('BOOL', 'not_', ['PREDICATE'], 1.0)

# Logical Primitives
#grammar.add_rule('PREDICATE', 'and_', ['PREDICATE', 'PREDICATE'], 1.0)
#grammar.add_rule('PREDICATE', 'or_', ['PREDICATE', 'PREDICATE'], 1.0)
#grammar.add_rule('PREDICATE', 'not_', ['PREDICATE'], 1.0)

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
