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
data = defaultdict(lambda: [])

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
            for h in hs:
                h.ll_decay = beta

        # set the alpha
        for condition in numpy.linspace(1, 10, num = 10):
            for time in numpy.linspace(1, 24, num = 1):
                data[condition][time] = make_data(condition, time, alpha)

        pHumanData = 0.0

        for row in behavioralData: ## check indexing in pandas
            condition, trial, number_inaccurate, number_accurate =  behavioralData[row] #something like that

            hs = hypothesis_space[condition]
            d = data[condition]

            # compute the posterior using all previous data
            for h in hs:
                h.compute_posterior(d[0:(trial - 1)])

            Z = logsumexp([h.posterior_score for h in hs])

            # compute the predicted probability of being accurate
            hyp_accuracy = sum([math.exp(h.posterior_score - Z) for h in hs if h(d[trial]) == d[trial].output])

            # mix to in the alpha (again) to account for the noise assumed in the model
            predicted_accuracy = alpha * hyp_accuracy + (1.0 - alpha) * 0.5

            # compute the probability of the observed responses given the model prediction
            pHumanData += log(predicted_accuracy) * number_accurate + log(1 - predicted_accuracy) * number_inaccurate

        print alpha, beta, pHumanData

        if (pHumanData > maxPHumanData):
            maxPHumanData = pHumanData
            idealAlpha = alpha
            idealBeta = beta

print "Best: ", idealAlpha, idealBeta, maxPHumanData