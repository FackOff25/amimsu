#!/usr/bin/env python3

import numpy as np
import os
import argparse
import sys

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
# Вывод cтарой матрицы
print("Изначальная матрица:")
print(P)
classes = state_classes.get_sets(P)
P = state_classes.transform_to_packed_matrix(P)
# Вывод новой матрицы
print("Изменённая матрица:")
print(P)
packedFile = open("results/packed.csv", 'w')
packedFile.write(csv_maker.get_matrix(P))
packedFile.close()

# нарисовать граф цепи
os.makedirs(os.path.dirname(graphFile), exist_ok=True)
make_graph.make_graph(P, graphFile)

new_classes = state_classes.get_sets(P)
for k in new_classes.keys():
    if k == 0:
        continue
    cl = new_classes[k]
    grid = np.ix_(np.arange(cl[0], cl[len(cl) - 1] + 1), np.arange(cl[0], cl[len(cl) - 1] + 1))
    P_l = P[grid]
    # рассчитать предельные вероятности
    # записать предельную матрицу переходов
    print(limit_probaility.get_limit_probability_matrix(P_l))
