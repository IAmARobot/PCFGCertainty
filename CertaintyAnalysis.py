import os
import pickle
from Data import make_data, uniqueStimuli
from LOTlib.Miscellaneous import logsumexp, Infinity
from Hypothesis import *
import pandas
import math
from optparse import OptionParser
import itertools
import numpy

#############################################################################################
#    Option Parser
#############################################################################################
parser = OptionParser()
parser.add_option("--alpha", dest="alpha", type="float", default=0.65, help="Reliability value (0-1]")
parser.add_option("--beta", dest="beta", type="float", default=0.06, help="Memory decay value 0-5")
parser.add_option("--condition", dest="condition", type="int", default='1', help="Which condition are we running for?")
parser.add_option("-s", action = "store_true", dest = "isOneShot", help = "Is this a single trial experiment?")
parser.add_option("--input", dest="input", type="string", default="Study1Counts.csv", help="Input file")
parser.add_option("--output", dest="output", type="string", default="modelDataStudy1.csv", help="Output file")

(options, args) = parser.parse_args()

#############################################################################################
#    MAIN CODE
#############################################################################################

# Populate hypothesis space for each condition
# Let's make a single set, the union of the sets over time
hypothesis_space = dict()

hypothesis_space[options.condition] = set()

for i in os.listdir("Data/condition" + str(options.condition)):
    if (i == "condition" + str(options.condition) + "_8.pkl"):
        with open("Data/condition" + str(options.condition) + '/' +  i, 'r') as f:
            hypothesis_space[options.condition].update(pickle.load(f))
    elif (not options.isOneShot):
        with open("Data/condition" + str(options.condition) + '/' +  i, 'r') as f:
            hypothesis_space[options.condition].update(pickle.load(f))

print "# Loaded hypothesis spaces ", [ len(hs) for hs in hypothesis_space.values() ]

behavioralData = pandas.read_csv(options.input)
print "# Loaded behavioral data"

data = dict()

if options.isOneShot:
    range = 8
else:
    range = 24

data[options.condition] = [make_data('condition' + str(options.condition), time, alpha = options.alpha) for time in xrange(range)]

print "# Constructed data"

for hs in hypothesis_space.values():
    for h in hs:
        h.ll_decay = options.beta

previousEntropy = 0
previousDomainEntropy = 0
previousHypPs = []
previousDataPs = []
responseMatrix = []

hs = hypothesis_space[options.condition]
d = data[options.condition]

responseMatrix = numpy.zeros((len(hs), len(uniqueStimuli)))

for hi, h in enumerate(hs):
    for oi, o in enumerate(uniqueStimuli):
        if h(o):
            responseMatrix[hi, oi] = 1
        else:
            responseMatrix[hi, oi] = 0

# Iterate through each trial for all conditions
for row in behavioralData.itertuples():
    condition, trial, number_accurate, number_inaccurate  = row[1:5]
    if condition not in hypothesis_space: continue

    crossEntropy = 0
    domainCrossEntropy = 0

    highestPosterior = -Infinity
    highestLikelihood = -Infinity

    # compute the posterior
    for h in hs:
        if (not options.isOneShot):
            h.compute_posterior(d[0:trial]) # all previous data
        else:
            h.compute_posterior(d[0:8])

        if (h.likelihood > highestLikelihood):
            highestLikelihood = h.likelihood

        if (h.posterior_score > highestPosterior):
            highestPosterior = h.posterior_score

    Z = logsumexp([h.posterior_score for h in hs])
    Zml = logsumexp([h.likelihood for h in hs])

    # compute the predicted probability of being accurate
    hyp_accuracy = sum([math.exp(h.posterior_score - Z) for h in hs if h(*d[trial - 1].input) == d[trial - 1].output])
    assert 0 <= hyp_accuracy <= 1

    # mix to in the alpha (again) to account for the noise assumed in the model
    predicted_accuracy = options.alpha * hyp_accuracy + (1 - options.alpha) * .5

    # compute the probability of the observed responses given the model prediction
    pHumanData = log(predicted_accuracy) * number_accurate + log(1 - predicted_accuracy) * number_inaccurate

    hypPs = [math.exp(h.posterior_score - Z) for h in hs]

    post = [h.posterior_score - Z for h in hs]
    dataPs = [numpy.dot(post, responseMatrix)]

    entropy = sum([p * log(p) for p in hypPs])
    domainEntropy = sum([p * numpy.log10(p) for p in dataPs])

    changeInEntropy = previousEntropy - entropy
    changeInDomainEntropy = previousDomainEntropy - domainEntropy

    if previousHypPs:
        for p, p2 in itertools.izip(hypPs, previousHypPs):
            crossEntropy += p * log(p / p2)

    if previousDataPs:
        for p, p2 in itertools.izip(dataPs, previousDataPs):
            domainCrossEntropy += p * log(p / p2)

    highestPosterior = math.exp(highestPosterior - Z)
    highestLikelihood = math.exp(highestLikelihood - Zml)

    previousEntropy = entropy
    previousDomainEntropy = domainEntropy
    previousHypPs = hypPs

    with open(options.output, 'a') as f:
        f.write(str(condition) + ',' + str(trial) + ',' + str(number_accurate) + ',' +
                str(number_inaccurate) + ',' + str(hyp_accuracy) + ',' + str(predicted_accuracy) + ',' +
                str(-entropy) + ',' + str(pHumanData) + ',' + str(highestPosterior) + ',' +
                str(highestLikelihood) + str(changeInEntropy) + str(-crossEntropy) +
                str(-domainEntropy) + str(changeInDomainEntropy) + str(-domainCrossEntropy) + '\n')

print "Done"