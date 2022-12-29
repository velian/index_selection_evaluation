import json
import csv
from typing import Dict, Set

path = '/Users/Julius/masterarbeit/J-Index-Selection/benchmark_results/plans/2022-12-02 23:35:50.json'
target = ''

# read jason
# extract indexes
#

with open(path) as file:
    plans = json.load(file)

def rec_plan_search(node: Dict, indexes: Set):
    if node['Node Type'] in ['Index Scan', 'Index Only Scan']:
        indexes.add(node['Index Name'])

    if 'Plans' in node.keys():
        for sub_node in node['Plans']:
            rec_plan_search(sub_node, indexes)
    else:
        return

indexes = set()
for query in plans.keys():
    for node in plans[query]:
        rec_plan_search(node, indexes)
    print(f"query {query}")
    print(indexes)
    indexes = set()

print(indexes)
