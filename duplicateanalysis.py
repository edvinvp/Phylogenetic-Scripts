#@edvin von platen
import json, os
from collections import defaultdict
from io import StringIOs
from Bio import Phylo
import matplotlib.pyplot as plt
import numpy as np
from ete3 import Tree

def duplication_analysis(json_path):
    # Find and open all available JSON files
    json_files = [pos_json for pos_json in os.listdir(json_path) if pos_json.endswith('.json')]

    # Store each parameter in it's own dictionary
    un_norm_posterior_densities = defaultdict()
    substition_model_densities = defaultdict()
    DLR_model_densities = defaultdict()
    duplication_rates = defaultdict()
    duplication_rates_means = defaultdict()
    loss_rates = defaultdict()
    edge_rate_means = defaultdict()
    edge_rate_CV = defaultdict()

    #################################

    # WRONG JSON Format from VMCMC -s, } missing at the end

    #################################

    for dont_use_this, js in enumerate(json_files):
        with open(json_path + js) as json_file:
            json_data = json.load(json_file)
            idx = int(js.split('.')[0]) # run number
        
            un_norm_posterior_densities[idx] = json_data["Parameters"]["UnnormalizedPosteriorDensity"]
            substition_model_densities[idx] = json_data["Parameters"]["SubstitutionModelDensity"]
            DLR_model_densities[idx] = json_data["Parameters"]["DLRModelDensity"]
            duplication_rates[idx] = json_data["Parameters"]["DuplicationRate"]
            duplication_rates_means[idx] = json_data["Parameters"]["DuplicationRate"]["Arithmetic Mean"]
            loss_rates[idx] = json_data["Parameters"]["EdgeRateMean"]
            edge_rate_means[idx] = json_data["Parameters"]["EdgeRateMean"]
            edge_rate_CV[idx] = json_data["Parameters"]["EdgeRateCV"]
        

    real_loss_rate = 0.1
    real_dup_rate = 0.4
    labels, data = [*zip(*duplication_rates_means.items())]
    # Histogram of runs
    plt.hist(data, bins=np.arange(min(data), max(data) + 0.15, 0.15))
    plt.ylabel("DLRS runs")
    plt.xlabel("Mean duplication rate. n="+str(len(data)) + ".")
    plt.show()










