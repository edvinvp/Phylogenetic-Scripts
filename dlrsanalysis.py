import treeanalysis as ta
import duplicateanalysis as da

da.duplication_analysis("NonRoot/traces/real/json_stats/")
ta.tree_analysis("NonRoot/traces/real/json/", "NonRoot/sim_data/real/")
