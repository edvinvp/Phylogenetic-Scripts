# @edvin von platen
# Calculates expected RF_norm distances and posterior probabilities for a given DLRS run.

import json, os
from collections import defaultdict
from collections import Counter
from io import StringIO #Read newick strings
import matplotlib.pyplot as plt
import numpy as np
from ete3 import Tree

def tree_analysis(json_path, tree_path):
    ## Filename specification:
    # Simulation data from HostTreeGen etc:
    # sim_data/h5/h5.1.pruned.tree , sim_data/real/r.1.pruned.tree , sim_data/h4/h4.1.pruned.tree
    
    # Simulation data in json format from VMCMC parsed DLRS data
    # traces/h5/json/1.json
    
    # Read all guest trees generated by GuestTreeGen
    # key = run number, val = tree string
    GuestTreeGen_trees = defaultdict()
    tree_files = [pos_tree for pos_tree in os.listdir(tree_path) if pos_tree.endswith(".pruned.tree")]
    for index, tr in enumerate(tree_files):
        with open(tree_path + tr) as tree_file:
            idx = int(tr.split('.')[1]) # run number
            no_comment_tree_str = ""
            tree_str = tree_file.read()
            i = 0
            # ete3 can't read the commented newick strings. Remove comments.
            while i < len(tree_str):
                if (tree_str[i] == '['):
                    i += 1
                    while(tree_str[i] != ']'):
                        i += 1
                    i += 1
                if (tree_str[i] != '['):
                    no_comment_tree_str = no_comment_tree_str + tree_str[i]
                    i += 1
            GuestTreeGen_trees[idx] = no_comment_tree_str
        
    # Find and open all available JSON files
    json_files = [pos_json for pos_json in os.listdir(json_path) if pos_json.endswith('.json')]
    # Store posterior probabilities for all trees
    probabilities = defaultdict(list)
    # Store E(RF(T)) for each data file
    RF_expectations = []
    count = 0
    for index, js in enumerate(json_files):
        with open(json_path + js) as json_file:
            idx = int(js.split('.')[0]) # run number
            gt_in = Tree(GuestTreeGen_trees[idx], format=1) # GT from GuestTreeGen
            json_data = json.load(json_file)
            RF_expectations.append(0)
            for i in range(len(json_data["Trees"]["Series_0"])):                            
                prob = json_data["Trees"]["Series_0"][i]["Posterior probability"]
                probabilities[idx].append(prob)
            
                # Robinson foulds analysis:
                # Calculate RF between the guest tree and all trees in the run.
                newick = json_data["Trees"]["Series_0"][i]["Newick"]
                gt_out = Tree(newick, format=1)
                rf, max_rf, common_leaves, parts_t1, parts_t2, s1, s2 = gt_in.robinson_foulds(gt_out, unrooted_trees=True)
                # VMCMC truncates probabilities lower than 0.01
                if prob >= 0.01:
                    if max_rf == 0:
                        rf = rf * prob
                    else:
                        rf = rf / max_rf * prob
                    RF_expectations[count] += rf
                
        count += 1
    ### RF Plot
    plt.hist(RF_expectations, bins=15)
    plt.xlabel("Expected normalised Robinson-Foulds distance. n=" + str(len(RF_expectations)) + ".")
    plt.ylabel("DLRS runs")
    plt.show()


    ### Maximum probability tree analysis ###
    
    prob_maxes = [e[0] for e in probabilities.values()]
    plt.hist(prob_maxes, bins=np.arange(min(prob_maxes), max(prob_maxes) + 0.05, 0.05))
    plt.xlabel("Maximum DLRS inferred tree probability. n=" + str(len(prob_maxes)) + ".")
    plt.ylabel("DLRS runs")
    plt.show()
