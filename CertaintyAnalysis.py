import os
import pickle
from optparse import OptionParser
from Data import make_data
from Primitives import *
from Hypothesis import *

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

def assess_hyp(hypothesis, condition, currentTime):
    data = make_data(condition, currentTime, options.alpha)
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

for i, space in enumerate(hypothesis_space):
    working_space.update(space)

    for s, h in enumerate(working_space):
        for wrd in assess_hyp(h, options.condition, i + 1):
            result = [s] + wrd
            result_strings.append(', '.join(str(j) for j in result))
            results.append(result)

#if (currentLikelihood > maxLikelihood):
#        maxLikelihood = currentLikelihood
#        csvResult = result_strings
#        pklResult = results

#    result_strings = []
#    results = []
#    working_space = set()
#    currentLikelihood = 0

print "Writing csv file . . ."
with open(options.out_path, 'a') as f:
    f.write('\n'.join(result_strings) + '\n')

if options.pkl_loc is not None:
    with open(options.pkl_loc, 'w') as f:
        pickle.dump(results, f)
