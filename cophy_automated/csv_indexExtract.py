import csv
path = '/Users/Julius/masterarbeit/J-Index-Selection/benchmark_results/results_extend_tpcds_99_queries.csv'
time_code = '2022-11-23 08:02:08'

with open(path, 'r') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    for line in reader:
        if line[0] == time_code:
            print(line[-1])

