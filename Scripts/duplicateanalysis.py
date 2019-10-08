#@edvin von platen
# Plots Histogram of duplication rate means for given DLRS run.

import json, os
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

def duplication_analysis(json_path):
    # Find and open all available JSON files
    json_files = [pos_json for pos_json in os.listdir(json_path) if pos_json.endswith('.json')]
    duplication_rates_means = defaultdict()

    #################################

    # WRONG JSON Format from VMCMC -s, } missing at the end

    #################################

    for dont_use_this, js in enumerate(json_files):
        with open(json_path + js) as json_file:
            json_data = json.load(json_file)
            idx = int(js.split('.')[0]) # run number
            duplication_rates_means[idx] = json_data["Parameters"]["DuplicationRate"]["Arithmetic Mean"]
        
    labels, data = [*zip(*duplication_rates_means.items())]
    # Histogram of runs
    plt.hist(data, bins=np.arange(min(data), max(data) + 0.15, 0.15))
    plt.ylabel("DLRS runs")
    plt.xlabel("Mean duplication rate. n="+str(len(data)) + ".")
    plt.show()










