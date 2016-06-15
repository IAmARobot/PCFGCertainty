import os
import pickle
from Data import make_data
from LOTlib.Miscellaneous import logsumexp, Infinity
from Primitives import *
from Hypothesis import *
import pandas
import math
from optparse import OptionParser

#############################################################################################
#    Option Parser
#############################################################################################
parser = OptionParser()
parser.add_option("--alpha", dest="alpha", type="float", default=0.65, help="Reliability value (0-1]")
parser.add_option("--beta", dest="beta", type="float", default=0.06, help="Memory decay value 0-5")
parser.add_option("--condition", dest="condition", type="int", default='1', help="Which condition are we running for?")
parser.add_option("-s", action = "store_true", dest = "isOneShot", help = "Is this a single trial experiment?")

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

behavioralData = pandas.read_csv('counts.csv')
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

pHumanData = 0.0

# Iterate through each trial for all conditions
for row in behavioralData.itertuples():
    condition, trial, number_accurate, number_inaccurate  = row[1:5]
    if condition not in hypothesis_space: continue

    hs = hypothesis_space[condition]
    d = data[condition]
    highestPosterior = -Infinity
    highestLikelihood = -Infinity

    # compute the posterior using all previous data
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
    assert 0.0 <= hyp_accuracy <= 1.0

    # mix to in the alpha (again) to account for the noise assumed in the model
    predicted_accuracy = options.alpha * hyp_accuracy + (1 - options.alpha) * 0.5

    # compute the probability of the observed responses given the model prediction
    pHumanData += log(predicted_accuracy) * number_accurate + log(1.0 - predicted_accuracy) * number_inaccurate

    hypPs = [math.exp(h.posterior_score - Z) for h in hs]
    entropy = sum([p * log(p) for p in hypPs])

    highestPosterior = math.exp(highestPosterior - Z)

    highestLikelihood = math.exp(highestLikelihood - Zml)

    with open('modelData.csv', 'a') as f:
        f.write(str(condition) + ',' + str(trial) + ',' + str(number_accurate) + ',' +
                str(number_inaccurate) + ',' + str(hyp_accuracy) + ',' + str(predicted_accuracy) + ',' +
                str(entropy) + ',' + str(pHumanData) + ',' + str(highestPosterior) + ',' +
                str(highestLikelihood) + '\n')

print "Done"