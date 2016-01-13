from math import log
from LOTlib.Miscellaneous import attrmem
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib.Hypotheses.Likelihoods.BinaryLikelihood import BinaryLikelihood
from Grammar import grammar

class MyHypothesis(BinaryLikelihood, LOTHypothesis):
    def __init__(self, **kwargs):
        LOTHypothesis.__init__(self, grammar=grammar, args=['IMG'], **kwargs)

    @attrmem('likelihood')
    def compute_likelihood(self, data, **kwargs):
        ll = 0
        for datum in data:
            ll += log(datum.alpha * (self(*datum.input) == datum.output) + (1.0 - datum.alpha) / 2.0)
        return ll / self.likelihood_temperature

def make_hypothesis(**kwargs):
    return MyHypothesis(**kwargs)
