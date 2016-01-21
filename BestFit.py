import os
import pickle
from optparse import OptionParser
from Data import make_data
from LOTlib.Miscellaneous import logsumexp
from Primitives import *
from Hypothesis import *
import numpy
import pandas

#############################################################################################
#    Option Parser
#############################################################################################
parser = OptionParser()
parser.add_option("--read", dest="directory", type="string", help="Pickled results", default="Data/Baseline.pkl")
parser.add_option("--pickle", dest="pkl_loc", type="string", help="Output a pkl", default=None)
parser.add_option("--write", dest="out_path", type="string", help="Results csv", default="results.csv")

parser.add_option("--alpha", dest="alpha", type="float", default=0.5160735, help="Reliability value (0-1]")
parser.add_option("--condition", dest="condition", type="str", default='condition9', help="Which condition are we running for?")
parser.add_option("--time", dest="time", type="int", default=24, help="With how many data points?")

(options, args) = parser.parse_args()

def assess_hyp(hypothesis, condition, currentTime, alpha):
    data = make_data(condition, currentTime, alpha)
    hypothesis.compute_likelihood(data)

    if currentTime < options.time:
        datum = make_data(condition, currentTime + 1, options.alpha)[-1]
    else:
        datum = data[-1]

    acc = hypothesis(*datum.input) == datum.output

    return [[condition, currentTime, hypothesis.prior, hypothesis.likelihood, acc, options.alpha]]

#############################################################################################
#    MAIN CODE
#############################################################################################
print "Loading hypothesis space . . ."
hypothesis_space = []

for i in os.listdir(options.directory):
    with open(options.directory + i, 'r') as f:
        hypothesis_space.append(pickle.load(f))

print "Assessing hypotheses . . ."
results = []
result_strings = []

working_space = set()

maxPData = 0
idealAlpha = 0
idealBeta = 0
idealHypothesisSpace = set()
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
        for ds in data:
            for d in ds:
                data.alpha = alpha

        pHumanData = 0.0

        for row in behavioralData: ## check indexing in pandas
            condition, response_number, number_accurate, number_inaccurate =  behavioralData[r] #something like that

            hs = hypothesis_space[condition]
            d  = data[condition]

            # compute the posterior using all previous data
            for h in hs:
                h.compute_posterior(d[0:(response_number-1)])
            Z = logsumexp([h.posterior_score for h in hs])

            # compute the predicted probability of being accurate
            hyp_accuracy = sum([ exp(h.posterior_score-Z) for h in hs if h(d[response_number]) == d[response_number].output ])

            # mix to in the alpha (again) to account for the noise assumed in the model
            predicted_accuracy = alpha*hyp_accuracy + (1.0-alpha)*0.5

            # compute the probability of the observed responses given the model prediction
            pHumanData += log(predicted_accuracy) * number_accurate + log(1-predicted_accuracy)*number_inaccurate


        print alpha, beta, pHumanData

        if (currentPData > maxPData):
            maxPData = currentPData
            idealAlpha = alpha
            idealBeta = beta
            idealHypothesisSpace = hypothesis_space

        currentPData = 0

print "Best: ", idealAlpha, idealBeta, maxPData

print "Writing csv file . . ."
with open(options.out_path, 'a') as f:
    f.write('\n'.join(result_strings) + '\n')

if options.pkl_loc is not None:
    with open(options.pkl_loc, 'w') as f:
        pickle.dump(results, f)
