from math import log
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib.Hypotheses.Likelihoods.PowerLawDecayed import PowerLawDecayed
from Grammar import grammar

class MyHypothesis(PowerLawDecayed, LOTHypothesis):
    def __init__(self, **kwargs):
        LOTHypothesis.__init__(self, grammar=grammar, display="lambda IMG: %s", **kwargs)

    def compute_single_likelihood(self, datum, **kwargs):
        print "Start"
        print self(*datum.input)
        print datum.output
        print datum.alpha
        print (self(*datum.input) == datum.output)
        print datum.alpha * (self(*datum.input) == datum.output)
        print datum.alpha * (self(*datum.input) == datum.output) + (1.0 - datum.alpha) / 2.0

        ll = log(datum.alpha * (self(*datum.input) == datum.output) + (1.0 - datum.alpha) / 2.0)

        print ll
        print "End"

        return ll

def make_hypothesis(**kwargs):
    return MyHypothesis(**kwargs)
