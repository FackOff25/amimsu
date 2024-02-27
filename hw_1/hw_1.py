import numpy as np
import random
import argparse

import make_graph
import csv_reader as csv
import limit_probaility
import simulation
import average

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--taskfile', help='file with variants', required=False, type=str, default='Task1.csv')
parser.add_argument('-g', '--graphfile', help='file to save graph to', required=False, type=str, default='results/Graph.png')
parser.add_argument('-v', '--variant', help='variant to make', required=False, type=int, default=0)
parser.add_argument('-e', '--error', help='acceptable error when comparing numbers', required=False, type=float, default=1e-8)
parser.add_argument('-r', '--resultfile', help='file to save experiment results to', required=False, type=str, default='results/results.csv')
parser.add_argument('-c', '--visitfile', help='file to save visits count to', required=False, type=str, default='results/visits.csv')
parser.add_argument('-a', '--avgfile', help='file to save square average dispersion to', required=False, type=str, default='results/average.csv')

args = vars(parser.parse_args())

taskFile = args['taskfile']
graphFile = args['graphfile']
variant = args['variant']
error = args['error']
resultfile = args['resultfile']
visitfile = args['visitfile']
avgfile = args['avgfile']

print(f"Taskfile: {taskFile}, variant: {variant}, graph will be in file {graphFile}")

P = csv.get_matrix(taskFile, variant)
# нарисовать граф цепи
make_graph.make_graph(P, graphFile)

# рассчитать предельные вероятности
# записать предельную матрицу переходов
P_l = limit_probaility.get_limit_probability_matrix(P)
limitFile = open("results/limit.csv", 'w')
for vector in P_l.tolist():
    line = ""
    for el in vector:
        line += str("{:.2f}".format(el)) + ','
    line = line[:-1]
    limitFile.write(line + '\n')
limitFile.close()
print(f'Check if limit matrix right: {limit_probaility.check_limit_matrix(P_l, error)}')

experiment_results = []
visit_counts = []
random.seed(1)
for i in range(50):
    # случайно выбрать начальное состояние
    start_state = random.randint(0, len(P_l)-1)
    # случайно разыграть переход в новое состояние, учитывая распределение вероятностей перехода
    experiment_result, visit_count = simulation.simulate_a_lot_of_steps(P, start_state, 100)
    experiment_results.append(experiment_result)
    visit_counts.append(visit_count)

file1 = open(resultfile, 'w')
for experiment in experiment_results:
    line = ""
    for state in experiment:
        line += str(state) + ','
    line = line[:-1]
    file1.write(line + '\n')
file1.close()

# составить таблицу для сравнения относительных частот наблюдений вхождения в каждое из состояний системы
file2 = open(visitfile, 'w')
for visit_count in visit_counts:
    line = ""
    for visit in visit_count.keys():
        line += str(visit_count[visit] / 100) + ','
    line = line[:-1]
    file2.write(line + '\n')
file2.close()

# построить «графики» переключений состояний цепи (для наглядности соединяем дискретные точки) для 3 произвольных экспериментов
randomlist = random.sample(range(50), 3)
for i in range(3):
    simulation.make_plot(experiment_results[randomlist[i]], 'results/plot' + str(i+1) + '.png')

file3 = open(avgfile, 'w')

square = average.calculate_square_errors([[v/100 for v in vector.values()] for vector in visit_counts])
file3.write(f'{square}\n')
square = average.calculate_fixed_square_errors([[v/100 for v in vector.values()] for vector in visit_counts])
file3.write(f'{square}\n')
file3.close()