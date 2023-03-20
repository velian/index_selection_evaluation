import logging

from selection.index import Index
from selection.selection_algorithm import SelectionAlgorithm
import json

from selection.workload import Column, Table

DEFAULT_PARAMETERS = {"json_path": None, "max_index_width": 99, }


class CophyOptimizer(SelectionAlgorithm):
    def __init__(self, database_connector, parameters):
        SelectionAlgorithm.__init__(
            self, database_connector, parameters, DEFAULT_PARAMETERS
        )
        assert(self.parameters['json_path'])

    def _calculate_best_indexes(self, workload):
        logging.info("Start example index selection algorithm")
        with open(self.parameters['json_path'], 'r', encoding='utf-8') as file:
            dict = json.load(file)
        self.parameters['budget'] = dict['budget_in_bytes']
        indexes =  []
        for indexes_strings in dict['selected_indexes']:
            column_names = indexes_strings.split(',')
            table = Table(column_names[0].split('.')[0])
            columns = []
            for column in column_names:
                col = Column(column.split('.')[1])
                columns.append(col)
                table.add_column(col)
            indexes.append(Index(columns))

        print(indexes)

        cost = self.cost_evaluation.calculate_cost(
            workload, indexes, store_size=True
        )
        print('ENDING')
        print(cost)

        return indexes

