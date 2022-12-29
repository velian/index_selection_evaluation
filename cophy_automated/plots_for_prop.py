import matplotlib.pyplot as plt

file_sizes = [2, 57, 19, 47000]
labels = ['1-1', '1-2', '2-1', '2-2']
plt.bar(labels, file_sizes)
plt.xlabel('Configuration')
plt.ylabel('File size in KB')
plt.title('Ilp file size for TPCH configurations')

plt.show()


gen_times = [10, 12, 16, 416]
labels = ['1-1', '1-2', '2-1', '2-2']
plt.bar(labels, gen_times)
plt.xlabel('Configuration')
plt.ylabel('Generation Time in seconds')
plt.title('Ilp file generation time for TPCH configurations')

plt.show()