from math import log
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib.Hypotheses.Likelihoods.PowerLawDecayed import PowerLawDecayed
from Grammar import grammar

class MyHypothesis(PowerLawDecayed, LOTHypothesis):
    def __init__(self, **kwargs):
        LOTHypothesis.__init__(self, grammar=grammar, display="lambda IMG: %s", **kwargs)

    def compute_single_likelihood(self, datum, **kwargs):
        ll = log(datum.alpha * (self(*datum.input) == datum.output) + (1.0 - datum.alpha) / 2.0)

        return ll

    def compute_prior(self):
        return 0

def make_hypothesis(**kwargs):
    return MyHypothesis(**kwargs)
