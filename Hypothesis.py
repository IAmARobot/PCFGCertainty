from math import log
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib.Hypotheses.Likelihoods.PowerLawDecayed import PowerLawDecayed
from Grammar import grammar
from LOTlib.Miscellaneous import attrmem

class MyHypothesis(PowerLawDecayed, LOTHypothesis):
    def __init__(self, **kwargs):
        LOTHypothesis.__init__(self, grammar=grammar, display="lambda IMG: %s", **kwargs)

    def compute_single_likelihood(self, datum, **kwargs):
        ll = log(datum.alpha * (self(*datum.input) == datum.output) + (1.0 - datum.alpha) / 2.0)

        return ll

    @attrmem('posterior_no_prior')
    def compute_posterior_no_prior(self, d, **kwargs):
        return self.compute_likelihood(d, **kwargs)

def make_hypothesis(**kwargs):
    return MyHypothesis(**kwargs)
