# @edvin von platen
# Calculates the Mann-Whitney-U statistic for each pair of non-root / rooted start samples.

import json, os
from collections import defaultdict
from collections import Counter
from io import StringIO #Read newick strings
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import mannwhitneyu
from ete3 import Tree


def extract_posterior_probabilities_and_RFstar_distance(json_path, tree_path):
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
    

    print("json files : " + str(len(json_files)))
    print(json_files)
    print(GuestTreeGen_trees.keys())

    # For each dataset calculate the expected normalised RF value. E(RF(T)) = SUM RF(T)P(T)
    RF_expectations = []
    count = 0;

    for index, js in enumerate(json_files):
        RF_expectations.append(0)
        with open(json_path + js) as json_file:
            idx = int(js.split('.')[0]) # run number
            gt_in = Tree(GuestTreeGen_trees[idx], format=1) # GT from GuestTreeGen
            json_data = json.load(json_file)
            for i in range(len(json_data["Trees"]["Series_0"])):
                newick = json_data["Trees"]["Series_0"][i]["Newick"]
                prob = json_data["Trees"]["Series_0"][i]["Posterior probability"]
                probabilities[idx].append(prob)
            
                # Robinson foulds analysis:
                # Calculate RF between the guest tree and all trees in the run.
                gt_out = Tree(newick, format=1)
                rf, max_rf, common_leaves, parts_t1, parts_t2, s1, s2 = gt_in.robinson_foulds(gt_out, unrooted_trees=True)
                #  VMCMC truncates probabiities lower than 0.01 to 0. 
                if prob >= 0.01:
                    if max_rf == 0:
                        rf = rf * prob
                    else:
                        rf = rf / max_rf * prob
                    RF_expectations[count] += rf
        count += 1

    prob_maxes = [e[0] for e in probabilities.values()]
    return (prob_maxes, RF_expectations)


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
        
    tmp, means = [*zip(*duplication_rates_means.items())]
    return means


# rr = rooted real
# nr = nonroot real
rr_tree_path = "../Rooted/sim_data/real/"
rr_json_path = "../Rooted/traces/real/json/"
rr_stats_path = "../Rooted/traces/real/json_stats/"
nr_tree_path = "../NonRoot/sim_data/real/"
nr_json_path = "../NonRoot/traces/real/json/"
nr_stats_path = "../NonRoot/traces/real/json_stats/"
rs_tree_path = "../Rooted/sim_data/h5/"
rs_json_path = "../Rooted/traces/h5/json/"
rs_stats_path = "../Rooted/traces/h5/json_stats/"
ns_tree_path = "../NonRoot/sim_data/h5/"
ns_json_path = "../NonRoot/traces/h5/json/"
ns_stats_path = "../NonRoot/traces/h5/json_stats/"

prob_rs, RF_rs = extract_posterior_probabilities_and_RFstar_distance(rs_json_path, rs_tree_path)
prob_ns, RF_ns = extract_posterior_probabilities_and_RFstar_distance(ns_json_path, ns_tree_path)
prob_rr, RF_rr = extract_posterior_probabilities_and_RFstar_distance(rr_json_path, rr_tree_path)
prob_nr, RF_nr = extract_posterior_probabilities_and_RFstar_distance(nr_json_path, nr_tree_path)
dup_rs = duplication_analysis(rs_stats_path)
dup_rr = duplication_analysis(rr_stats_path)
dup_nr = duplication_analysis(nr_stats_path)
dup_ns = duplication_analysis(ns_stats_path)

print("Real posterior probability")
print("Samples rr: " + str(len(prob_rr)) + ". Samples nr: " + str(len(prob_nr)) + ".")
print(mannwhitneyu(prob_rr,prob_nr))
print("")

print("Real: RF*")
print("Samples rr: " + str(len(RF_rr)) + ". Samples nr: " + str(len(RF_nr)) + ".")
print(mannwhitneyu(RF_rr,RF_nr))
print("")

print("Real: dup")
print(mannwhitneyu(dup_rs, dup_rr))
print("")

print("Sim: posterior probability")
print("Samples rr: " + str(len(prob_rs)) + ". Samples nr: " + str(len(prob_ns)) + ".")
print(mannwhitneyu(prob_rs,prob_ns))
print("")

print("Sim: RF")
print("Samples rr: " + str(len(RF_rs)) + ". Samples nr: " + str(len(RF_ns)) + ".")
print(mannwhitneyu(RF_rs,RF_ns))
print("")

print("Sim: dup")
print(mannwhitneyu(dup_nr, dup_ns))
print("")
