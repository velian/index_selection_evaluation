
from typing import List
import matplotlib.pyplot as plt

def cost_collate(list: List, cost):
    #todo
    for i in range(len(list)):
        list[i] = list[i]/cost
    return list

# TPCH RUNTIMES
budget = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
runtime_ilp_tpch_1_1 = [12.4, 12.4, 12.4, 12.4, 12.4, 12.4, 12.4, 12.4, 12.4, 12.4, ]
#runtime_ilp_tpch_1_2 = [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, ]
runtime_ilp_tpch_2_1 = [16.5, 16.5, 16.5, 16.5, 16.5, 16.5, 16.5, 16.5, 16.5, 16.5]
#runtime_ilp_tpch_2_2 = [415.2, 415.2, 415.2, 415.2, 415.2, 415.2, 415.2, 415.2, 415.2, 415.2, ]

runtime_extend_tpch = [0.54, 1.69, 2.29, 3.43, 3.91, 5.82, 6.73, 6.93, 6.91, 6.98]
plt.step(budget, runtime_ilp_tpch_1_1,'r-*', where='mid', label = 'ILP-1-1')
plt.step(budget, runtime_ilp_tpch_2_1,'g-*', where='mid', label = 'ILP-2-1')
# plt.step(budget, runtime_ilp_tpch_1_2,'b-*', where='mid', label = 'ILP-1-2')
# plt.step(budget, runtime_ilp_tpch_2_2,'r-v', where='mid', label = 'ILP-2-2')
plt.step(budget, runtime_extend_tpch,'g-v', where='mid', label = 'Extend')

plt.xlabel('Budget')
plt.ylabel('Runtime Algorithm')
plt.title('Algortihm Runtime on TPCH')
plt.show()

#TPCH SOLUTION QUALITY
no_index_cost = 18710250539762.86
budget = [ 2, 3, 4, 5, 6, 7, 8, 9, 10]
solution_ilp_tpch_1_1 = cost_collate([ 1120504622, 1119342217, 1112335080, 1111982074, 1111881331, 1111881331, 1111881331, 1111881331, 1111881331], no_index_cost)
solution_ilp_tpch_2_1 = cost_collate([ 1175326120, 142365462.8, 141170836.2, 134194316.4, 133023779.6, 132088283, 124724419.6, 124571329.6, 124571200.1], no_index_cost)
#solution_ilp_tpch_1_2 = []
#solution_ilp_tpch_2_2 = []

solution_tpch_extend = cost_collate([ 808419478.2500001, 53463731.690000005, 52305268.5, 45156724.58000001, 43936729.0, 43794367.38, 43794367.38, 43794367.38, 43794367.38], no_index_cost)


plt.step(budget, solution_ilp_tpch_1_1,'r-*', where='mid', label = 'ILP-1-1')
plt.step(budget, solution_ilp_tpch_2_1,'g-*', where='mid', label = 'ILP-2-1')
# plt.step(budget, solution_ilp_tpch_1_2,'b-*', where='mid', label = 'ILP-1-2')
# plt.step(budget, solution_ilp_tpch_2_2,'r-v', where='mid', label = 'ILP-2-2')
plt.step(budget, solution_tpch_extend,'g-v', where='mid', label = 'Extend')

plt.xlabel('Budget')
plt.ylabel('Solution Acceleration')
plt.title('Costs Per budget')
plt.legend()
plt.show()

quit()

# TPCDS RUNTIMES
budget = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
runtime_ilp_tpcds_1_1 = [33, 33, 33, 33, 33, 33, 33, 33, 33, 33, ]
runtime_ilp_tpcds_1_2 = []
runtime_ilp_tpcds_2_1 = [253.4, 253.4, 253.4, 253.4, 253.4, 253.4, 253.4, 253.4, 253.4, 253.4, ]
runtime_ilp_tpcds_2_2 = []

#runtime_extend_tpds = [139.39, 240.51, 296.17, 376.88, 437.34, , , , , 712.03]
plt.step(budget, runtime_ilp_tpcds_1_1,'r-*', where='mid', label = 'ILP-1-1')
plt.step(budget, runtime_ilp_tpcds_2_1,'g-*', where='mid', label = 'ILP-2-1')
plt.step(budget, runtime_ilp_tpcds_1_2,'b-*', where='mid', label = 'ILP-1-2')
plt.step(budget, runtime_ilp_tpcds_2_2,'r-v', where='mid', label = 'ILP-2-2')
#plt.step(budget, runtime_extend_tpds,'g-v', where='mid', label = 'Extend')
plt.xlabel('Budget')
plt.ylabel('Runtime Algorithm')
plt.title('Algortihm Runtime on TPCDS')
plt.show()

# TPCDSOLUTION QUALITY

budget = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
solution_ilp_tpcds_1_1 = []
solution_ilp_tpcds_2_1 = []
solution_ilp_tpcds_1_2 = []
solution_ilp_tpcds_2_2 = []

solution_tpcds_extend = []
plt.step(budget, solution_ilp_tpcds_1_1,'r-*', where='mid', label = 'ILP-1-1')
plt.step(budget, solution_ilp_tpcds_2_1,'g-*', where='mid', label = 'ILP-2-1')
plt.step(budget, solution_ilp_tpcds_1_2,'b-*', where='mid', label = 'ILP-1-2')
plt.step(budget, solution_ilp_tpcds_2_2,'r-v', where='mid', label = 'ILP-2-2')
plt.step(budget, solution_tpcds_extend,'g-v', where='mid', label = 'Extend')

plt.xlabel('Budget')
plt.ylabel('Solution Quality')
plt.title('Costs Per budget')
plt.legend()
plt.show()
