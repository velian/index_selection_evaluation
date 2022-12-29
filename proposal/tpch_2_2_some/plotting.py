from typing import List
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def cost_collate(list: List, cost):
    #todo
    for i in range(len(list)):
        list[i] = (list[i]/cost) * 100
    return list

def add_runtime(list: List, runtime: float):
    for i in range(len(list)):
        list[i] = list[i] + runtime

#TPCH ALL REMOVED RUNTIME
# TPCH RUNTIMES

budget = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
runtime_ilp_tpch_1_1 = [0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08 ,0.08]
generate_1_1 = 10.93
add_runtime(runtime_ilp_tpch_1_1, generate_1_1)
runtime_ilp_tpch_1_2 = [ 0.34,  0.34,  0.34,  0.34,  0.34,  0.34,  0.34,  0.34,  0.34,  0.34,  0.34,  0.34]
generate_1_2 = 13.91
add_runtime(runtime_ilp_tpch_1_2, generate_1_2)
runtime_ilp_tpch_2_1 = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, ]
generate_2_1 = 16.53
add_runtime(runtime_ilp_tpch_2_1, generate_2_1)
runtime_extend_1 = [0.69, 0.56, 1.73, 1.48, 1.99, 1.62, 1.44, 1.44, 1.42, 1.57, 1.33, 1.33]
runtime_extend_2 = [0.8, 0.69, 2.4, 1.67, 4.33, 3.95, 4.13, 3.9, 3.98, 4.58, 4.5, 4.48]
runtime_extend_3 = [0.82, 0.9, 2.56, 1.56, 3.94, 3.91, 4.5, 5.68, 5.53, 6.1, 5.44, 5.39]

plt.step(budget, runtime_ilp_tpch_1_1, where='mid', label = 'ILP-1-1', color='tab:blue', marker='v', fillstyle='none')
plt.step(budget, runtime_ilp_tpch_2_1, where='mid', label = 'ILP-2-1', color='tab:orange', marker='o', fillstyle='none')
plt.step(budget, runtime_ilp_tpch_1_2, where='mid', label = 'ILP-1-2', color='tab:green', marker='^', fillstyle='none')
plt.step(budget, runtime_extend_2, where='mid', label = 'Extend-2', color='tab:cyan', marker='*', fillstyle='none')
plt.step(budget, runtime_extend_3, where='mid', label = 'Extend-3', color='tab:olive', marker='D', fillstyle='none')



plt.xlabel('Budget')
plt.ylabel('Algorithm Runtime (sec)')
plt.title('Algorithm Runtime on TPC-DS - All Queries')
plt.legend()
plt.savefig('tpcds_runtimes_ALLqueries.png')
plt.clf()


#TPCH SOLUTION QUALITY
no_index_cost = 42828273
budget = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
solution_ilp_1_1 = []
solution_ilp_1_2 = []
solution_ilp_2_1 = []
solution_ilp_2_2 = []

cost_collate(solution_ilp_1_1, no_index_cost)
cost_collate(solution_ilp_1_2, no_index_cost)
cost_collate(solution_ilp_2_1, no_index_cost)
cost_collate(solution_ilp_2_2, no_index_cost)

solution_extend_1 = [33499652, 31648033, 31027801, 31027801, 31027801, 31027801, 31027801, 31027801, 31027801, 31027801]
solution_extend_2 = [33355292, 31648033, 30740237, 30364686, 30364686, 30364686, 30364686, 30364686, 30364686, 30364686]
solution_extend_3 = [33355292, 31648033, 30740237, 30364686, 30364686, 30208333, 30208333, 30070261, 30070261, 30070261]


cost_collate(solution_extend_1, no_index_cost)
cost_collate(solution_extend_2, no_index_cost)
cost_collate(solution_extend_3, no_index_cost)

plt.step(budget, solution_ilp_1_1, where='mid', label = 'ILP-1-1', color='tab:blue', marker='v', fillstyle='none')
plt.step(budget, solution_ilp_2_1, where='mid', label = 'ILP-2-1', color='tab:orange', marker='o', fillstyle='none')
plt.step(budget, solution_ilp_1_2, where='mid', label = 'ILP-1-2', color='tab:green', marker='^', fillstyle='none')
plt.step(budget, solution_ilp_2_2, where='mid', label = 'ILP-2-2', color='tab:red', marker='s', fillstyle='none')
plt.step(budget, solution_extend_1, where='mid', label = 'Extend-1', color='tab:purple', marker='p', fillstyle='none')
plt.step(budget, solution_extend_2, where='mid', label = 'Extend-2', color='tab:cyan', marker='*', fillstyle='none')
plt.step(budget, solution_extend_3, where='mid', label = 'Extend-3', color='tab:olive', marker='D', fillstyle='none')

plt.xlabel('Budget')
plt.ylabel('Relative Workload Cost')
plt.title('Solution Quality on TPC-DS - All Queries')
plt.legend()
plt.savefig('tpcds_qualities_ALLqueries.png')
plt.clf()


#TPCH SOLUTION QUALITY NO 1-1

plt.xlabel('Budget')
plt.ylabel('Relative Workload Cost')
plt.title('Solution Quality on TPC-DS - All Queries')
plt.legend()
plt.savefig('tpcds_qualities_ALLqueries_All.png')
plt.clf()