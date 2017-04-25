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

(options, args) = parser.parse_args()

#############################################################################################
#    MAIN CODE
#############################################################################################

for study in xrange(1, 5):
    # Populate hypothesis space for each condition
    # Let's make a single set, the union of the sets over time
    hypothesis_space = dict()

    for condition in xrange(1, 11):
        hypothesis_space[condition] = set()

        for i in os.listdir("Data/condition" + str(condition)):
            if (i == "condition" + str(condition) + "_8.pkl"):
                with open("Data/condition" + str(condition) + '/' +  i, 'r') as f:
                    hypothesis_space[condition].update(pickle.load(f))
            elif (study != 2):
                with open("Data/condition" + str(condition) + '/' +  i, 'r') as f:
                    hypothesis_space[condition].update(pickle.load(f))

    print "# Loaded hypothesis spaces ", [ len(hs) for hs in hypothesis_space.values() ]

    behavioralData = pandas.read_csv("Study" + str(study) + "Counts.csv")
    print "# Loaded behavioral data " + str(study)

    data = dict()

    if study == 2:
        range = 8
    else:
        range = 24

    for condition in xrange(1, 11):
        data[condition] = [make_data('condition' + str(condition), time, alpha = options.alpha) for time in xrange(range)]

    print "# Constructed data"

    for beta in numpy.linspace(0, .1, num = 10):
        print "# Starting", options.alpha, beta

        # Set the decays
        for hs in hypothesis_space.values():
            for h in hs:
                h.ll_decay = beta

        pHumanData = 0

        for row in behavioralData.itertuples():
            condition, trial, number_accurate, number_inaccurate = row[1:5]

            if condition not in hypothesis_space: continue

            hs = hypothesis_space[condition]
            d = data[condition]

            # compute the posterior using all previous data
            for h in hs:
                if (study != 2):
                    h.compute_posterior(d[0:trial]) # all previous data
                else:
                    h.compute_posterior(d[0:8])

            Z = logsumexp([h.posterior_score for h in hs])

            # compute the predicted probability of being accurate
            hyp_accuracy = sum([math.exp(h.posterior_score - Z) for h in hs if h(*d[trial - 1].input) == d[trial - 1].output])
            assert 0 <= hyp_accuracy <= 1

            # mix to in the alpha (again) to account for the noise assumed in the model
            predicted_accuracy = options.alpha * hyp_accuracy + (1 - options.alpha) * .5

            # compute the probability of the observed responses given the model prediction
            pHumanData += log(predicted_accuracy) * number_accurate + log(1 - predicted_accuracy) * number_inaccurate

        print options.alpha, beta, pHumanData

        with open("bestFitsStudy" + str(study) + ".csv", 'a') as f:
            f.write(str(options.alpha) + ',' + str(beta) + ',' + str(pHumanData) + ',' + '\n')

print "Done"