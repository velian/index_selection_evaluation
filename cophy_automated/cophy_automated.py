# export PYTHONPATH=${PYTHONPATH}:${PWD} <-- DIS GUS TING

import subprocess
import time
from config_generator import generate_cophy_config_files
from os import listdir, remove, removedirs, makedirs
from shutil import copy
from pathlib import Path

from selection.index_selection_evaluation import IndexSelection

amplpath = '/Users/Julius/masterarbeit/ampl_macos64/ampl'
runpath = 'cophy_automated/cophy.run'
modelpath = 'cophy_automated/cophy_ampl_model.mod' # THIS MODEL DOESNT WORK YET, WHICH IS ANNOYING

max_widths = [1,]
max_indexes = [1]
algorithms = ['tpch']
budgets = [5000000000]
path = 'autotesting'

for file in listdir(path + "/data"):
    remove(path +  '/data/' + file)

for file in listdir(path + "/configs"):
    remove(path +  '/configs/' + file)

for file in listdir(path + "/results"):
    remove(path +  '/results/' + file)

for rithm in algorithms:
    for width in max_widths:
        for indexes in max_indexes:
            generate_cophy_config_files(rithm, 1, width, indexes, path)


for config in listdir(path + '/configs'):
    print(f'Running {config} data generation')
    start = time.time()
    IndexSelection()._run_algorithms(f'{path}/configs/{config}') # this needs to be run as a python subprocess so i can time it out
    end = time.time()
    print(f'Generating Data took {end-start}')

data_files = listdir(path + '/data')
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
makedirs(path + '/results', exist_ok=True)
for data_file in data_files:
    print(f'solving {data_file}')
    start = time.time()
    with open(path + f'/results/{Path(data_file).stem}.txt', 'w+') as outfile:
        subprocess.run([amplpath, Path(modelpath).absolute(), Path(path + '/data/' + data_file).absolute(), Path(runpath).absolute()],stdout=outfile)
    end = time.time()
    print(f'Solving Data took {end-start}')
