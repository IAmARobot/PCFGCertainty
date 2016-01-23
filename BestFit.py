import os
import pickle
from optparse import OptionParser
from Data import make_data
from LOTlib.Miscellaneous import logsumexp
from Primitives import *
from Hypothesis import *
import numpy
import pandas
import math
from collections import defaultdict
from optparse import OptionParser

#############################################################################################
#    Option Parser
#############################################################################################
parser = OptionParser()
parser.add_option("--alpha", dest="alpha", type="float", default=0.1, help="Reliability value 0-1")
parser.add_option("--beta", dest="beta", type="float", default=0.5, help="Memory decay value 0-5")

(options, args) = parser.parse_args()

#############################################################################################
#    MAIN CODE
#############################################################################################
hypothesis_space = defaultdict(lambda: [])
data = defaultdict(lambda : defaultdict(lambda: []))

# Populate hypothesis space for each condition
for condition in xrange(1, 11):
    for i in os.listdir("Data/condition" + str(condition)):
        with open("Data/condition" + str(condition) + '/' +  i, 'r') as f:
            hypothesis_space[condition].append(pickle.load(f))

behavioralData = pandas.read_csv('behavioralAccuracyCounts.csv')

# Set the decays
for hs in hypothesis_space.values():
    for s in hs:
        for h in s:
            h.ll_decay = options.beta

# set the alpha
for condition in xrange(1, 11):
    for time in xrange(1, 25):
        data[condition][time] = make_data('condition' + str(condition), time, options.alpha)

pHumanData = 0.0

for row in behavioralData.itertuples():
    condition = row[1]
    trial = row[2]
    number_inaccurate = row[3]
    number_accurate = row[4]

    hs = hypothesis_space[condition]
    d = data[condition]

    previousData = d[1]

    for t in xrange(2, trial + 1):
        previousData = previousData + d[t]

    # compute the posterior using all previous data
    for s in hs:
        for h in s:
            h.compute_posterior(previousData)

    Z = logsumexp([h.posterior_score for s in hs for h in s])

    # compute the predicted probability of being accurate
    hyp_accuracy = sum([math.exp(h.posterior_score - Z) for s in hs for h in s if sum([int(h(dp.input[0]) == dp.output) for dp in d[trial]]) == len(d[trial])])

    # mix to in the alpha (again) to account for the noise assumed in the model
    predicted_accuracy = options.alpha * hyp_accuracy + (1 - options.alpha) * 0.5

    # compute the probability of the observed responses given the model prediction
    pHumanData += log(predicted_accuracy) * number_accurate + log(1 - predicted_accuracy) * number_inaccurate

print options.alpha, options.beta, pHumanData

with open('bestFits.csv', 'a') as f:
    f.write(options.alpha + ',' + options.beta + ',' + pHumanData + ',' + '\n')
