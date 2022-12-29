from typing import List
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def cost_collate(list: List, cost):
    #todo
    for i in range(len(list)):
        list[i] = (list[i]/cost)
    return list

def add_runtime(list: List, runtime: float):
    for i in range(len(list)):
        list[i] = list[i] + runtime



# TPCH RUNTIMES
budget = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
runtime_ilp_tpch_1_1 = [0.20, 0.14, 0.15, 0.15, 0.15, 0.17, 0.18, 0.14, 0.14, 0.19, 0.17, 0.17]
generate_1_1 = 31
whatiftime = 7.8
add_runtime(runtime_ilp_tpch_1_1, generate_1_1)
add_runtime(runtime_ilp_tpch_1_1, generate_1_1)
runtime_ilp_tpch_2_1 = [12, 9.22, 10.4, 4.48, 4.8, 8.92, 4.68, 5.0, 9.52, 4.3, 4.6, 11.]
generate_2_1 = 269
whatif_2_1 = 247
add_runtime(runtime_ilp_tpch_2_1, generate_2_1)
add_runtime(runtime_ilp_tpch_2_1, whatif_2_1)
runtime_extend_1 = [40.04, 71.11, 81.23, 94.51, 102.89, 109.3, 109.58, 110.88, 114.52, 113.92, 113.01, 113.01]
runtime_extend_2 = [136.86, 222.81, 258.21, 321.17, 354.83, 380.42, 438.96, 528.41, 575.67, 576.02, 577.86, 571.19]
runtime_extend_3 = [153.9, 253.01, 311.07, 400.79, 484.86, 522.57, 619.08, 761.73, 798.21, 860.26, 925.65, 1033.14]

plt.step(budget, runtime_ilp_tpch_1_1, where='mid', label = 'ILP-1-1', color='tab:blue', marker='v', fillstyle='none')
plt.step(budget, runtime_ilp_tpch_2_1, where='mid', label = 'ILP-2-1', color='tab:orange', marker='o', fillstyle='none')
plt.step(budget, runtime_extend_1, where='mid', label = 'Extend-1', color='tab:purple', marker='p', fillstyle='none', linestyle='dashed')
plt.step(budget, runtime_extend_2, where='mid', label = 'Extend-2', color='tab:cyan', marker='*', fillstyle='none', linestyle='dashed')
plt.step(budget, runtime_extend_3, where='mid', label = 'Extend-3', color='tab:olive', marker='D', fillstyle='none', linestyle='dashed')

plt.xlabel('Budget (GB)')
plt.ylabel('Algorithm Runtime (sec)')
plt.title('Algorithm Runtime on TPC-H - All Queries')
plt.legend()
plt.savefig('tpcds_runtimes_allqueries.png')
plt.clf()


#TPCH ALL REMOVED RUNTIME
# TPCH RUNTIMES

plt.step(budget, runtime_ilp_tpch_1_1, where='mid', label = 'ILP-1-1', color='tab:blue', marker='v', fillstyle='none')
plt.step(budget, runtime_ilp_tpch_2_1, where='mid', label = 'ILP-2-1', color='tab:orange', marker='o', fillstyle='none')
plt.step(budget, runtime_extend_1, where='mid', label = 'Extend-1', color='tab:purple', marker='p', fillstyle='none', linestyle='dashed')
plt.step(budget, runtime_extend_2, where='mid', label = 'Extend-2', color='tab:cyan', marker='*', fillstyle='none', linestyle='dashed')
plt.step(budget, runtime_extend_3, where='mid', label = 'Extend-3', color='tab:olive', marker='D', fillstyle='none', linestyle='dashed')

plt.xlabel('Budget (GB)')
plt.ylabel('Algorithm Runtime (sec)')
plt.title('Algorithm Runtime on TPC-DS - All Queries')
plt.legend()
plt.savefig('tpcDS_runtimes_allqueries.png')
plt.clf()


#TPCH SOLUTION QUALITY
no_index_cost = 430788547670
budget = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
solution_ilp_1_1 = [3950004136, 3948755133, 3947785076, 3947593156, 3947403481, 3946394693, 3945567445, 3945343185, 3945318894, 3945318894]
solution_ilp_1_2 = [960539520, 957102389, 955450321, 954064344, 954064344, 953064344, 952064344, 950547657, 949789744, 949157428]
solution_ilp_2_1 = [4043985240, 4040956004, 4039515554, 4038113583, 4036852781, 4035997075, 4035017871, 4034179054, 4033727372, 4033466132]

cost_collate(solution_ilp_1_1, no_index_cost)
cost_collate(solution_ilp_1_2, no_index_cost)
cost_collate(solution_ilp_2_1, no_index_cost)

solution_extend_1 = [262827066, 257489470, 255189185, 254294984, 254294984, 254294984, 251106978, 251106978, 251106978, 251106978]
solution_extend_2 = [176929128, 171398220, 168331287, 163994017, 161047676, 158837348, 157964960, 157964960, 157964960, 157964960]
solution_extend_3 = [176929128, 171398220, 168331287, 163994017, 161047676, 158837348, 157499538, 156546044, 155671369, 154259598]

cost_collate(solution_extend_1, no_index_cost)
cost_collate(solution_extend_2, no_index_cost)
cost_collate(solution_extend_3, no_index_cost)

plt.step(budget, solution_ilp_1_1, where='mid', label = 'ILP-1-1', color='tab:blue', marker='v', fillstyle='none')
plt.step(budget, solution_ilp_2_1, where='mid', label = 'ILP-2-1', color='tab:orange', marker='o', fillstyle='none')
plt.step(budget, solution_ilp_1_2, where='mid', label = 'ILP-1-2', color='tab:green', marker='^', fillstyle='none')
plt.step(budget, solution_extend_1, where='mid', label = 'Extend-1', color='tab:purple', marker='p', fillstyle='none', linestyle='dashed')
plt.step(budget, solution_extend_2, where='mid', label = 'Extend-2', color='tab:cyan', marker='*', fillstyle='none', linestyle='dashed')
plt.step(budget, solution_extend_3, where='mid', label = 'Extend-3', color='tab:olive', marker='D', fillstyle='none', linestyle='dashed')

plt.xlabel('Budget (GB)')
plt.ylabel('Relative Workload Cost')
plt.title('Solution Quality on TPC-DS - All Queries')
plt.legend()
plt.savefig('tpcds_qualities_allqueries.png')
plt.clf()


#TPCH SOLUTION QUALITY NO 1-1
quit()
plt.xlabel('Budget')
plt.ylabel('Relative Workload Cost')
plt.title('Solution Quality on TPC-DS - All Queries')
plt.legend()
plt.savefig('tpcds_qualities_allqueries.png')
plt.clf()