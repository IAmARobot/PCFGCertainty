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

hypothesis_space = defaultdict(lambda: [])
data = defaultdict(lambda : defaultdict(lambda: []))

# Populate hypothesis space for each condition
for condition in xrange(1, 11):
    for i in os.listdir("Data/condition" + str(condition)):
        with open("Data/condition" + str(condition) + '/' +  i, 'r') as f:
            hypothesis_space[condition].append(pickle.load(f))

results = []
result_strings = []
maxPHumanData = 0
idealAlpha = 0
idealBeta = 0
currentPData = 0

behavioralData = pandas.read_csv('behavioralAccuracyCounts.csv')

## Let's pretend hypothesis_space is a dict from conditions to a set of hypotheses
## Pretend data is dict from conditions to the list of data

for alpha in numpy.linspace(0, 1, num = 10):
    for beta in numpy.linspace(0, 5, num = 10):

        # Set the decays
        for hs in hypothesis_space.values():
            for s in hs:
                for h in s:
                    h.ll_decay = beta

        # set the alpha
        for condition in xrange(1, 11):
            for time in xrange(1, 25):
                data[condition][time] = make_data('condition' + str(condition), time, alpha)

        pHumanData = 0.0

        for row in behavioralData.itertuples():
            condition = row[1]
            trial = row[2]
            number_inaccurate = row[3]
            number_accurate = row[4]

            hs = hypothesis_space[condition]
            d = data[condition]

            # compute the posterior using all previous data
            for s in hs:
                for h in s:
                    previousData = d[1]

                    for t in xrange(2, trial + 1):
                        previousData.append(d[t])

                    h.compute_posterior(previousData)

            Z = logsumexp([h.posterior_score for s in hs for h in s])

            # compute the predicted probability of being accurate
            hyp_accuracy = sum([math.exp(h.posterior_score - Z) for s in hs for h in s if [int(h(dp.input) == dp.output) for dp in d[trial]]])

            # mix to in the alpha (again) to account for the noise assumed in the model
            predicted_accuracy = alpha * hyp_accuracy + (1 - alpha) * 0.5

            # compute the probability of the observed responses given the model prediction
            pHumanData += log(predicted_accuracy) * number_accurate + log(1 - predicted_accuracy) * number_inaccurate

        print alpha, beta, pHumanData

        if (pHumanData > maxPHumanData):
            maxPHumanData = pHumanData
            idealAlpha = alpha
            idealBeta = beta

print "Best: ", idealAlpha, idealBeta, maxPHumanData