
###############################################
# TreeReader:
# Goals:
# - read TTree produced at step1 in pyROOT
# - create numpy.array to be analyzed later on
###############################################

import numpy as np
from ROOT import TTree, TFile

# read a root file based on the path/name [filename]
# return a numpy.array: an row per HSCP candidate, columns corresponding to variables
# list of variables selected in "varList"

def LoadTree(filename,varList):
