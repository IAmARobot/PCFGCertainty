import numpy
import sys
from LOTlib.Inference.Samplers.MetropolisHastings import MHSampler
from LOTlib.MPI.MPI_map import MPI_map, is_master_process
from LOTlib.Miscellaneous import display_option_summary, Infinity
from LOTlib.TopN import TopN
from LOTlib import break_ctrlc
from optparse import OptionParser
from Grammar import grammar
from Primitives import *
from Hypothesis import *
from Data import make_data

######################################################################################################
#   Option Parser
######################################################################################################
parser = OptionParser()
parser.add_option("--out", dest="out_path", type="string",
                  help="Output file (a pickle of FiniteBestSet)", default="hypspace.pkl")

parser.add_option("--steps", dest="steps", type="int", default=1000000, help="Number of samples to run")
parser.add_option("--top", dest="top_count", type="int", default=1000, help="Top number of hypotheses to store")
parser.add_option("--chains", dest="chains", type="int", default=1,
                  help="Number of chains to run (new data set for each chain)")

parser.add_option("--alpha", dest="alpha", type="float", default=0.45, help="Reliability value (0-1]")
parser.add_option("--beta", dest="beta", type="float", default=0, help="Memory decay value 0-5")
parser.add_option("--condition", dest="condition", type="str", default='condition9', help="Which condition are we running for?")
parser.add_option("--time", dest="time", type="int", default=24, help="With how many data points?")

parser.add_option("--llt", dest="llt", type="float", default=1.0, help="Likelihood temperature")
parser.add_option("--pt", dest="prior_temp", type="float", default=1.0, help="Prior temperature")

(options, args) = parser.parse_args()

######################################################################################################
#   Chain Function
######################################################################################################
def run(data_pts):
    h0 = make_hypothesis()
    h0.ll_decay = options.beta

    hyps = TopN(N = options.top_count)

    mhs = MHSampler(h0, data_pts, options.steps, likelihood_temperature = options.llt, prior_temperature = options.prior_temp)

    for samples_yielded, h in break_ctrlc(enumerate(mhs)):
        h.ll_decay = options.beta
        hyps.add(h)

    return hyps

###################################################################################
# Main Running
###################################################################################

data = [make_data(options.condition, options.time, options.alpha)]

argarray = map(lambda x: [x], [data] * options.chains)

if is_master_process():
    display_option_summary(options)

hypothesis_space = set()

for h in MPI_map(run, argarray, progress_bar = False):
    hypothesis_space.update(h)

import pickle
with open(options.out_path, 'w') as f:
    pickle.dump(hypothesis_space, f)
