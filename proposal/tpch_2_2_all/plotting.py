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



# TPCH RUNTIMES
budget = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
runtime_ilp_tpch_1_1 = [0.04, 0.04, 0.03, 0.03, 0.04, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02]
generate_1_1 = 10.29
whatif_1_1 = 0
add_runtime(runtime_ilp_tpch_1_1, generate_1_1)
runtime_ilp_tpch_1_2 = [0.17, 0.25, 0.38, 0.37, 0.34, 0.33, 0.24, 0.40, 0.29, 0.25, 0.24, 0.30]
generate_1_2 = 11.62
whatif_1_2 = 2.3
add_runtime(runtime_ilp_tpch_1_2, generate_1_2)
add_runtime(runtime_ilp_tpch_1_2, whatif_1_2)
runtime_ilp_tpch_2_1 = [0.05, 0.05, 0.07, 0.09, 0.08, 0.08, 0.11, 0.07, 0.08, 0.11, 0.08, 0.08]
generate_2_1 = 14.86
whatif_21 = 2.8
add_runtime(runtime_ilp_tpch_2_1, generate_2_1)
add_runtime(runtime_ilp_tpch_2_1, whatif_21)
runtime_ilp_tpch_2_2 = [21.68, 50.27, 248.39, 283.97, 406.16, 1400, 1546.62, 1412.92, 1363.17, 715.42, 1932.83, 1832.83]
generate_2_2 = 399.69
whatif_2_2 = 386
add_runtime(runtime_ilp_tpch_2_2, generate_2_2)
add_runtime(runtime_ilp_tpch_2_2, whatif_2_2)
runtime_extend_1 = [0.42, 0.7, 1.03, 1.19, 1.36, 1.77, 1.93, 1.69, 1.76, 1.85, 2.83, 1.87]
runtime_extend_2 = [0.56, 1.64, 2.13, 3.33, 3.52, 5.83, 6.62, 6.85, 6.85, 7.0, 7.08, 6.95]
runtime_extend_3 = [0.54, 1.8, 2.41, 4.25, 4.77, 7.95, 5.61, 7.28, 8.19, 8.81, 9.01, 9.01]

plt.step(budget, runtime_ilp_tpch_1_1, where='mid', label = 'ILP-1-1', color='tab:blue', marker='v', fillstyle='none')
plt.step(budget, runtime_ilp_tpch_2_1, where='mid', label = 'ILP-2-1', color='tab:orange', marker='o', fillstyle='none')
plt.step(budget, runtime_ilp_tpch_1_2, where='mid', label = 'ILP-1-2', color='tab:green', marker='^', fillstyle='none')
plt.step(budget, runtime_ilp_tpch_2_2, where='mid', label = 'ILP-2-2', color='tab:red', marker='s', fillstyle='none')
plt.step(budget, runtime_extend_1, where='mid', label = 'Extend-1', color='tab:purple', marker='p', fillstyle='none', linestyle='dashed')
plt.step(budget, runtime_extend_2, where='mid', label = 'Extend-2', color='tab:cyan', marker='*', fillstyle='none', linestyle='dashed')
plt.step(budget, runtime_extend_3, where='mid', label = 'Extend-3', color='tab:olive', marker='D', fillstyle='none', linestyle='dashed')

plt.xlabel('Budget (GB)')
plt.ylabel('Algorithm Runtime (sec)')
plt.title('Algorithm Runtime on TPC-H - All Queries')
plt.legend()
plt.savefig('tpch_runtimes_allqueries.pdf')
plt.clf()


#TPCH ALL REMOVED RUNTIME
# TPCH RUNTIMES
budget = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
runtime_ilp_tpch_1_1 = [0.04, 0.04, 0.03, 0.03, 0.04, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02]
generate_1_1 = 10.29
add_runtime(runtime_ilp_tpch_1_1, generate_1_1)
runtime_ilp_tpch_1_2 = [0.17, 0.25, 0.38, 0.37, 0.34, 0.33, 0.24, 0.40, 0.29, 0.25, 0.24, 0.30]
generate_1_2 = 11.62
add_runtime(runtime_ilp_tpch_1_2, generate_1_2)
runtime_ilp_tpch_2_1 = [0.05, 0.05, 0.07, 0.09, 0.08, 0.08, 0.11, 0.07, 0.08, 0.11, 0.08, 0.08]
generate_2_1 = 14.86
add_runtime(runtime_ilp_tpch_2_1, generate_2_1)
runtime_extend_1 = [0.42, 0.7, 1.03, 1.19, 1.36, 1.77, 1.93, 1.69, 1.76, 1.85, 2.83, 1.87]
runtime_extend_2 = [0.56, 1.64, 2.13, 3.33, 3.52, 5.83, 6.62, 6.85, 6.85, 7.0, 7.08, 6.95]
runtime_extend_3 = [0.54, 1.8, 2.41, 4.25, 4.77, 7.95, 5.61, 7.28, 8.19, 8.81, 9.01, 9.01]

plt.step(budget, runtime_ilp_tpch_1_1, where='mid', label = 'ILP-1-1', color='tab:blue', marker='v', fillstyle='none')
plt.step(budget, runtime_ilp_tpch_2_1, where='mid', label = 'ILP-2-1', color='tab:orange', marker='o', fillstyle='none')
plt.step(budget, runtime_ilp_tpch_1_2, where='mid', label = 'ILP-1-2', color='tab:green', marker='^', fillstyle='none')
plt.step(budget, runtime_extend_1, where='mid', label = 'Extend-1', color='tab:purple', marker='p', fillstyle='none', linestyle='dashed')
plt.step(budget, runtime_extend_2, where='mid', label = 'Extend-2', color='tab:cyan', marker='*', fillstyle='none', linestyle='dashed')
plt.step(budget, runtime_extend_3, where='mid', label = 'Extend-3', color='tab:olive', marker='D', fillstyle='none', linestyle='dashed')

plt.xlabel('Budget (GB)')
plt.ylabel('Algorithm Runtime (sec)')
plt.title('Algorithm Runtime on TPC-H - All Queries')
plt.legend()
plt.savefig('tpch_runtimes_allqueries_no22.pdf')
plt.clf()


#TPCH SOLUTION QUALITY
no_index_cost = 18720354307388
budget = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
solution_ilp_1_1 = [  1141518409, 1134509433, 1134156423, 1134082686, 1134082686, 1134082686, 1134082686, 1134082686, 1134082686, 1134082686]
solution_ilp_1_2 = [  95299418, 88343860, 87672237, 87672237, 87609338, 87609338, 87609338, 87609338, 87609338, 87609338]
solution_ilp_2_1 = [  148061335, 146866529, 139883070, 139295553, 139163872, 132193225, 132050377, 132050252, 131554773, 131422967]
solution_ilp_2_2 = [  51414161, 49579733, 43030211, 40030211, 36669673, 34800881, 33978868, 33897773, 33535763, 33535763]

cost_collate(solution_ilp_1_1, no_index_cost)
cost_collate(solution_ilp_1_2, no_index_cost)
cost_collate(solution_ilp_2_1, no_index_cost)
cost_collate(solution_ilp_2_2, no_index_cost)

solution_extend_1 = [88460728, 57076115, 56628346, 49017422, 49017422, 49017422, 49017422, 49017422, 49017422, 49017422]
solution_extend_2 = [50751924, 49594349, 42438472, 41218556, 41076903, 41076903, 41076903, 41076903, 41076903, 41076903]
solution_extend_3 = [51477682, 50154187, 43134988, 41814682, 34695108, 33966527, 33820618, 33664109, 33664109, 33664109]

cost_collate(solution_extend_1, no_index_cost)
cost_collate(solution_extend_2, no_index_cost)
cost_collate(solution_extend_3, no_index_cost)

plt.step(budget, solution_ilp_1_1, where='mid', label = 'ILP-1-1', color='tab:blue', marker='v', fillstyle='none')
plt.step(budget, solution_ilp_2_1, where='mid', label = 'ILP-2-1', color='tab:orange', marker='o', fillstyle='none')
plt.step(budget, solution_ilp_1_2, where='mid', label = 'ILP-1-2', color='tab:green', marker='^', fillstyle='none')
plt.step(budget, solution_ilp_2_2, where='mid', label = 'ILP-2-2', color='tab:red', marker='s', fillstyle='none')
plt.step(budget, solution_extend_1, where='mid', label = 'Extend-1', color='tab:purple', marker='p', fillstyle='none', linestyle='dashed')
plt.step(budget, solution_extend_2, where='mid', label = 'Extend-2', color='tab:cyan', marker='*', fillstyle='none', linestyle='dashed')
plt.step(budget, solution_extend_3, where='mid', label = 'Extend-3', color='tab:olive', marker='D', fillstyle='none', linestyle='dashed')

plt.xlabel('Budget (GB)')
plt.ylabel('Relative Workload Cost')
plt.title('Solution Quality on TPC-H - All Queries')
plt.legend()
plt.savefig('tpch_qualities_allqueries.pdf')
plt.clf()


#TPCH SOLUTION QUALITY NO 1-1
no_index_cost = 18720354307388
budget = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
solution_ilp_1_2 = [  95299418, 88343860, 87672237, 87672237, 87609338, 87609338, 87609338, 87609338, 87609338, 87609338]
solution_ilp_2_1 = [  148061335, 146866529, 139883070, 139295553, 139163872, 132193225, 132050377, 132050252, 131554773, 131422967]
solution_ilp_2_2 = [  51414161, 49579733, 43030211, 40030211, 36669673, 34800881, 33978868, 33897773, 33535763, 33535763]

cost_collate(solution_ilp_1_1, no_index_cost)
cost_collate(solution_ilp_1_2, no_index_cost)
cost_collate(solution_ilp_2_1, no_index_cost)
cost_collate(solution_ilp_2_2, no_index_cost)

solution_extend_1 = [88460728, 57076115, 56628346, 49017422, 49017422, 49017422, 49017422, 49017422, 49017422, 49017422]
solution_extend_2 = [50751924, 49594349, 42438472, 41218556, 41076903, 41076903, 41076903, 41076903, 41076903, 41076903]
solution_extend_3 = [51477682, 50154187, 43134988, 41814682, 34695108, 33966527, 33820618, 33664109, 33664109, 33664109]

cost_collate(solution_extend_1, no_index_cost)
cost_collate(solution_extend_2, no_index_cost)
cost_collate(solution_extend_3, no_index_cost)

plt.step(budget, solution_ilp_2_1, where='mid', label = 'ILP-2-1', color='tab:orange', marker='o', fillstyle='none')
plt.step(budget, solution_ilp_1_2, where='mid', label = 'ILP-1-2', color='tab:green', marker='^', fillstyle='none')
plt.step(budget, solution_ilp_2_2, where='mid', label = 'ILP-2-2', color='tab:red', marker='s', fillstyle='none')
plt.step(budget, solution_extend_1, where='mid', label = 'Extend-1', color='tab:purple', marker='p', fillstyle='none', linestyle='dashed')
plt.step(budget, solution_extend_2, where='mid', label = 'Extend-2', color='tab:cyan', marker='*', fillstyle='none', linestyle='dashed')
plt.step(budget, solution_extend_3, where='mid', label = 'Extend-3', color='tab:olive', marker='D', fillstyle='none', linestyle='dashed')

plt.xlabel('Budget (GB)')
plt.ylabel('Relative Workload Cost')
plt.title('Solution Quality on TPC-H - All Queries')
plt.legend()
plt.savefig('tpch_qualities_allqueries_no11.pdf')
plt.clf()