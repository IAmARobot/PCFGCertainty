import os
import pickle
from Data import make_data, uniqueStimuli, conditions
from LOTlib.Miscellaneous import logsumexp, Infinity
from Hypothesis import *
import pandas
import math
from optparse import OptionParser
import itertools
import numpy
from Primitives import *

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

for i in os.listdir("Data/" + str(options.condition)):
    if (i == str(options.condition) + "_8.pkl"):
        with open("Data/" + str(options.condition) + '/' +  i, 'r') as f:
            hypothesis_space[options.condition].update(pickle.load(f))
    elif (not options.isOneShot):
        with open("Data/" + str(options.condition) + '/' +  i, 'r') as f:
            hypothesis_space[options.condition].update(pickle.load(f))

print "# Loaded hypothesis spaces ", [ len(hypothesisSpace) for hypothesisSpace in hypothesis_space.values() ]

behavioralData = pandas.read_csv(options.input)
print "# Loaded behavioral data"

data = dict()

if options.isOneShot:
    range = 8
else:
    range = 24

data[options.condition] = [make_data(options.condition, time, alpha = options.alpha) for time in xrange(range)]

print "# Constructed data"

for hypothesisSpace in hypothesis_space.values():
    for hypothesis in hypothesisSpace:
        hypothesis.ll_decay = options.beta

previousEntropy = 0
previousDomainEntropy = 0
previousHypPs = []
previousDataPs = []

stimuliPosterior = 0

hypothesisSpace = hypothesis_space[options.condition]
d = data[options.condition]

responseMatrix = numpy.zeros((len(hypothesisSpace), len(uniqueStimuli)))

for hi, h in enumerate(hypothesisSpace):
    for oi, o in enumerate(uniqueStimuli):
        if h(o):
            responseMatrix[hi, oi] = 1

# Iterate through each trial for all conditions
for row in behavioralData.itertuples():
    condition, trial, number_accurate, number_inaccurate  = row[1:5]
    if condition not in hypothesis_space: continue

    crossEntropy = 0
    domainCrossEntropy = 0

    highestPosterior = -Infinity
    highestLikelihood = -Infinity

    # compute the posterior
    for hypothesis in hypothesisSpace:
        if (not options.isOneShot):
            hypothesis.compute_posterior(d[0:trial]) # all previous data
        else:
            hypothesis.compute_posterior(d[0:8])

        if (hypothesis.likelihood > highestLikelihood):
            highestLikelihood = hypothesis.likelihood

        if (hypothesis.posterior_score > highestPosterior):
            highestPosterior = hypothesis.posterior_score

    Z = logsumexp([hypothesis.posterior_score for hypothesis in hypothesisSpace])
    Zml = logsumexp([hypothesis.likelihood for hypothesis in hypothesisSpace])

    # compute the predicted probability of being accurate
    hyp_accuracy = sum([math.exp(hypothesis.posterior_score - Z) for hypothesis in hypothesisSpace if hypothesis(*d[trial - 1].input) == d[trial - 1].output])
    assert 0 <= hyp_accuracy <= 1

    # mix to in the alpha (again) to account for the noise assumed in the model
    predicted_accuracy = options.alpha * hyp_accuracy + (1 - options.alpha) * .5

    # compute the probability of the observed responses given the model prediction
    pHumanData = log(predicted_accuracy) * number_accurate + log(1 - predicted_accuracy) * number_inaccurate

    hypothesesPosteriors = [math.exp(hypothesis.posterior_score - Z) for hypothesis in hypothesisSpace]
    dataPosteriors = numpy.dot(hypothesesPosteriors, responseMatrix)

    currentStimuli = conditions[condition][0][trial - 1]

    for i, stimuli in enumerate(uniqueStimuli):
        if stimuli == currentStimuli:
            stimuliPosterior = dataPosteriors[i]
            break

    entropy = sum([posterior * log(posterior) for posterior in hypothesesPosteriors])
    domainEntropy = sum([posterior * log(posterior) for posterior in dataPosteriors])

    changeInEntropy = previousEntropy - entropy
    changeInDomainEntropy = previousDomainEntropy - domainEntropy

    for posterior, previousPosterior in itertools.izip(hypothesesPosteriors, previousHypPs):
        crossEntropy += posterior * log(posterior / previousPosterior)

    for posterior, previousPosterior in itertools.izip(dataPosteriors, previousDataPs):
        domainCrossEntropy += posterior * log(posterior / previousPosterior)

    highestPosterior = math.exp(highestPosterior - Z)
    highestLikelihood = math.exp(highestLikelihood - Zml)

    previousEntropy = entropy
    previousDomainEntropy = domainEntropy
    previousHypPs = hypothesesPosteriors
    previousDataPs = dataPosteriors

    with open(options.output, 'a') as f:
        f.write(str(condition) + ',' + str(trial) + ',' + str(number_accurate) + ',' +
                str(number_inaccurate) + ',' + str(hyp_accuracy) + ',' + str(predicted_accuracy) + ',' +
                str(-entropy) + ',' + str(pHumanData) + ',' + str(highestPosterior) + ',' +
                str(highestLikelihood) + ',' + str(changeInEntropy) + ',' + str(-crossEntropy) + ',' +
                str(-domainEntropy) + ',' + str(changeInDomainEntropy) + ',' + str(-domainCrossEntropy) + ',' +
                str(stimuliPosterior) + '\n')

print "Done"