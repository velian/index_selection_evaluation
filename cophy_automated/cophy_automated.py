# export PYTHONPATH=${PYTHONPATH}:${PWD} <-- DIS GUS TING

import os
import subprocess
import time
from typing import Dict, List
from config_generator import generate_cophy_config_files
from os import listdir, remove, removedirs, makedirs
from shutil import copy
from pathlib import Path
from model_gen import model_gen
from satistics import ExecutionStatistics

from selection.index_selection_evaluation import IndexSelection



amplpath = '/Users/Julius/masterarbeit/ampl_macos64/ampl'
runpath = 'cophy_automated/cophy.run'
modelpath = 'cophy_automated/cophy_ampl_model.mod'
max_widths = [2, 1]
max_indexes = [2, 1]
scale_factor = 10
algorithms = ['tpch']
budgets = [1000000000, 2000000000, 3000000000, 4000000000, 5000000000, 6000000000, 7000000000, 8000000000, 9000000000, 10000000000, 11000000000, 12000000000]
path = 'proposal/tpch_2_2_some'

#for file in listdir(path + "/data"):
#    remove(path +  '/data/' + file)#
#
#for file in listdir(path + "/configs"):
#    remove(path +  '/configs/' + file)#

#for file in listdir(path + "/results"):
#    remove(path +  '/results/' + file)

os.makedirs(path, exist_ok=True)
os.makedirs(path + '/data', exist_ok=True)
os.makedirs(path + '/configs', exist_ok=True)
os.makedirs(path + '/results', exist_ok=True)


for rithm in algorithms:
    for width in max_widths:
        for indexes in max_indexes:
            generate_cophy_config_files(rithm, 10, width, indexes, path)



for config in listdir(path + '/configs'):
    print('---------------------')
    print(f'Running {config} data generation')
    start = time.time()
    IndexSelection()._run_algorithms(f'{path}/configs/{config}') # this needs to be run as a python subprocess so i can time it out
    end = time.time()
    print(f'Generating Data took {end-start}')
    print('---------------------')

data_files = listdir(path + '/data')
data_files.sort()
for data_file in data_files:
    for budget in budgets:
        dest_file_path = path + '/data/' + Path(data_file).stem + f'_{budget}.dat'
        copy(path + '/data/' + data_file, dest_file_path)
        with open(dest_file_path, 'a') as file:
            file.write(f'\nparam budget := {budget};\n')

#cleanup
for file in data_files:
    remove(path + '/data/' + file)

# now solve
data_files = listdir(path + '/data')
data_files.sort()
makedirs(path + '/results', exist_ok=True)
for data_file in data_files:
    print('---------------------')
    print(f'solving {data_file}')
    with open(path + '/data/' + data_file, 'r')as file:
        line = file.readline()
        indexes = int(line[1:])
        line = file.readline()
        combis = int(line[1:])
    model_gen(indexes, combis)
    start = time.time()
    with open(path + f'/results/{Path(data_file).stem}.txt', 'w+') as outfile:
        subprocess.run([amplpath, Path(modelpath).absolute(), Path(path + '/data/' + data_file).absolute(), Path(runpath).absolute()],stdout=outfile)
    end = time.time()
    print(f'Solving Data took {end-start}')
    print('---------------------')
