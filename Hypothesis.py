from math import log
from LOTlib.Miscellaneous import attrmem
from LOTlib.Hypotheses.LOTHypothesis import LOTHypothesis
from LOTlib.Hypotheses.Likelihoods.BinaryLikelihood import BinaryLikelihood
from LOTlib.Hypotheses.Likelihoods.PowerLawDecayed import PowerLawDecayed
from Grammar import grammar

class MyHypothesis(LOTHypothesis, PowerLawDecayed):
    def __init__(self, **kwargs):
        LOTHypothesis.__init__(self, grammar=grammar, display="lambda IMG: %s", **kwargs)

    def compute_single_likelihood(self, datum, **kwargs):
        ll = log(datum.alpha * (self(*datum.input) == datum.output) + (1.0 - datum.alpha) / 2.0)

        return ll / self.likelihood_temperature

def make_hypothesis(**kwargs):
    return MyHypothesis(**kwargs)
