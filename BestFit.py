import os
import pickle
from Data import make_data
from LOTlib.Miscellaneous import logsumexp
from Primitives import *
from Hypothesis import *
import numpy
import pandas
import math
from optparse import OptionParser

#############################################################################################
#    Option Parser
#############################################################################################
parser = OptionParser()
parser.add_option("--alpha", dest="alpha", type="float", default=0.01, help="Reliability value (0-1]")
#parser.add_option("--beta", dest="beta", type="float", default=0.05263158, help="Memory decay value 0-5")
parser.add_option("-s", action = "store_true", dest = "isOneShot", help = "Is this a single trial experiment?")

(options, args) = parser.parse_args()

#############################################################################################
#    MAIN CODE
#############################################################################################

# Populate hypothesis space for each condition
# Let's make a single set, the union of the sets over time
hypothesis_space = dict()
for condition in xrange(1, 11):
    hypothesis_space[condition] = set()

    for i in os.listdir("Data/condition" + str(condition)):
        if (i == "condition" + str(condition) + "_8.pkl"):
            with open("Data/condition" + str(condition) + '/' +  i, 'r') as f:
                hypothesis_space[condition].update(pickle.load(f))
        elif (not options.isOneShot):
            with open("Data/condition" + str(condition) + '/' +  i, 'r') as f:
                hypothesis_space[condition].update(pickle.load(f))

print "# Loaded hypothesis spaces ", [ len(hs) for hs in hypothesis_space.values() ]

behavioralData = pandas.read_csv('counts.csv')
print "# Loaded behavioral data"

data = dict()

if options.isOneShot:
    range = 8
else:
    range = 24

for condition in xrange(1, 11):
    data[condition] = [make_data('condition' + str(condition), time, alpha = options.alpha) for time in xrange(range)]

print "# Constructed data"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main loop
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# print "alpha beta pHumanData" # if you want a header

#for alpha in numpy.linspace(0, 1, num = 10):
for beta in numpy.linspace(0, .3, num = 31):
    print "# Starting", options.alpha, beta

    # Set the decays
    for hs in hypothesis_space.values():
        for h in hs:
            h.ll_decay = beta

    pHumanData = 0.0

    for row in behavioralData.itertuples():
        condition, trial, number_accurate, number_inaccurate = row[1:5]

        if condition not in hypothesis_space: continue

        hs = hypothesis_space[condition]
        d = data[condition]

        # compute the posterior using all previous data
        for h in hs:
            if (not options.isOneShot):
                h.compute_posterior(d[0:trial]) # all previous data
            else:
                h.compute_posterior(d[0:8])

        Z = logsumexp([h.posterior_score for h in hs])

        # compute the predicted probability of being accurate
        hyp_accuracy = sum([math.exp(h.posterior_score - Z) for h in hs if h(*d[trial - 1].input) == d[trial - 1].output])
        assert 0.0 <= hyp_accuracy <= 1.0

        # mix to in the alpha (again) to account for the noise assumed in the model
        predicted_accuracy = options.alpha * hyp_accuracy + (1 - options.alpha) * 0.5

        # compute the probability of the observed responses given the model prediction
        pHumanData += log(predicted_accuracy) * number_accurate + log(1.0 - predicted_accuracy) * number_inaccurate

    print options.alpha, beta, pHumanData

    with open('bestFits.csv', 'a') as f:
        f.write(str(options.alpha) + ',' + str(beta) + ',' + str(pHumanData) + ',' + '\n')