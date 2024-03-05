#!/usr/bin/env python3

import numpy as np
import os
import argparse
import sys
import random

import state_classes
import csv_maker

sys.path.insert(0, '../')

import hw_1.make_graph as make_graph
import hw_1.csv_reader as csv
import hw_1.limit_probaility as limit_probaility
import hw_1.simulation as simulation
import hw_1.average as average

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--taskfile', help='file with variants', required=False, type=str, default='Task2.csv')
parser.add_argument('-g', '--graphfile', help='file to save graph to', required=False, type=str, default='results/Graph.png')
parser.add_argument('-v', '--variant', help='variant to make', required=False, type=int, default=0)
parser.add_argument('-e', '--error', help='acceptable error when comparing numbers', required=False, type=float, default=1e-8)
parser.add_argument('-r', '--resultfile', help='file to save experiment results to', required=False, type=str, default='results/results.csv')
parser.add_argument('-c', '--visitfile', help='file to save visits count to', required=False, type=str, default='results/visits.csv')
parser.add_argument('-a', '--avgfile', help='file to save square average dispersion to', required=False, type=str, default='results/average.csv')
parser.add_argument('-p', '--plotfile', help='file to save experiments plots to', required=False, type=str, default='results/plot.png')

args = vars(parser.parse_args())

taskFile = args['taskfile']
graphFile = args['graphfile']
variant = args['variant']
error = args['error']
resultfile = args['resultfile']
visitfile = args['visitfile']
avgfile = args['avgfile']
plotfile = args['plotfile']

print(f"Taskfile: {taskFile}, variant: {variant}, graph will be in file {graphFile}")

P = csv.get_matrix(taskFile, variant)
# Вывод cтарой матрицы
print("Изначальная матрица:")
print(csv_maker.get_matrix_sep(P, '\t'))
classes = state_classes.get_sets(P)
P = state_classes.transform_to_packed_matrix(P)
# Вывод новой матрицы
print("Изменённая матрица:")
print(csv_maker.get_matrix_sep(P, '\t'))
packedFile = open("results/packed.csv", 'w')
packedFile.write(csv_maker.get_matrix(P))
packedFile.close()

# нарисовать граф цепи
os.makedirs(os.path.dirname(graphFile), exist_ok=True)
make_graph.make_graph(P, graphFile)

new_classes = state_classes.get_sets(P)
limit_vectors = {}
for k in new_classes.keys():
    if k == 0:
        continue
    cl = new_classes[k]
    grid = np.ix_(np.arange(cl[0], cl[len(cl) - 1] + 1), np.arange(cl[0], cl[len(cl) - 1] + 1))
    P_l = P[grid]
    # рассчитать предельные вероятности
    # записать предельную матрицу переходов
    print('Предельная матрица класса №' + str(k))
    print(csv_maker.get_matrix_sep(limit_probaility.get_limit_probability_matrix(P_l), ' '))
    limit_vectors[k] = limit_probaility.get_limit_probability_vector(P_l)

reduced_matrix_size = len(new_classes[0]) + len(new_classes) - 1
P_r = np.eye(reduced_matrix_size)
sums = {}
for i in new_classes[0]:
    for j in new_classes[0]:
        P_r[i][j] = P.item(i,j)
    for cl in new_classes.keys():
        if cl != 0:
            sum = np.sum(P[np.ix_(np.array([i]), np.arange(new_classes[cl][0], new_classes[cl][len(new_classes[cl]) - 1] + 1))])
            P_r[i][len(new_classes[0]) + cl - 1] = sum
            try:
                sums[cl].append(sum)
            except KeyError:
                sums[cl] = []
                sums[cl].append(sum)

print("Сокращённая матрица")
print(csv_maker.get_matrix_sep(P_r, '\t'))
P_r_l = limit_probaility.get_limit_probability_matrix_by_pow(P_r)
print("Предельная сокращённая матрица")
print(csv_maker.get_matrix_sep(P_r_l, '\t'))

P_l = np.zeros((len(P), len(P)))
for i in new_classes[0]:
    for j in new_classes[0]:
        P_l[i][j] = 0
    for cl in new_classes.keys():
        if cl != 0:
            sum = np.sum(P[np.ix_(np.array([i]), np.arange(new_classes[cl][0], new_classes[cl][len(new_classes[cl]) - 1] + 1))])
            for j in range(len(new_classes[cl])):
                P_l[i][new_classes[cl][j]] = P_r_l.item(i, len(new_classes[0]) + cl - 1) * limit_vectors[cl][j]

for cl in new_classes.keys():
    if cl != 0:
        first = new_classes[cl][0]
        for s_i in new_classes[cl]:
            for s_j in new_classes[cl]:
                P_l[s_i][s_j] = limit_vectors[cl][s_j-first]

limitfile = open('results/limit.csv', 'w')
limitfile.write(csv_maker.get_matrix(P_l))
limitfile.close()

experiment_results = []
visit_counts = []
steps_num = 100
random.seed(3)
# повторить эксперимент 10 раз для каждого исходного состояния
for i in range(10):
    # перебираем все состояния в качестве исходных
    for start_state in range(len(P)):
        # случайно разыграть переход в новое состояние, учитывая распределение вероятностей перехода
        experiment_result, visit_count = simulation.simulate_a_lot_of_steps(P, start_state, steps_num)
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

print('Средняя частота посещения')
print(csv_maker.get_vector_sep(average.calculate_average_vector(visit_counts) / steps_num, '\t'))

# составить таблицу для сравнения относительных частот наблюдений вхождения в каждое из состояний системы
file2 = open(visitfile, 'w')
for visit_count in visit_counts:
    line = ""
    for visit in visit_count.keys():
        line += str(visit_count[visit] / steps_num) + ','
    line = line[:-1]
    file2.write(line + '\n')
file2.close()

# построить «графики» переключений состояний цепи
for k in new_classes.keys():
    if k == 0:
        # стартовать по 6 раза внутри каждого класса существенных состояний
        experiment_set_list = random.sample(range(10), 6)
        for exp_set in experiment_set_list:
            state = random.randint(0, len(new_classes[k]) - 1)
            idx = exp_set * len(P) + state
            simulation.make_plot(experiment_results[idx], plotfile)
    else:
        # стартовать по 2 раза внутри каждого класса существенных состояний
        randomlist = random.sample(new_classes[k], 2)
        for i in range(2):
            simulation.make_plot(experiment_results[randomlist[i]], plotfile)

simulation.clear_plot()