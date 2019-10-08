#author: Edvin von Platen

import treeanalysis as ta
import duplicateanalysis as da

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

print("ROOTED REAL")
ta.tree_analysis(rr_json_path, rr_tree_path)
da.duplication_analysis(rr_json_path)
print("NON-ROOT REAL")
ta.tree_analysis(nr_json_path, nr_tree_path)
da.duplication_analysis(nr_json_path)
print("ROOTED SYNTHETIC")
ta.tree_analysis(rs_json_path, rs_tree_path)
da.duplication_analysis(rs_json_path)
print("NON-ROOT SYNTHETIC")
ta.tree_analysis(ns_json_path, ns_tree_path)
da.duplication_analysis(ns_json_path)
