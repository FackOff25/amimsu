import numpy as np

def get_matrix(filename: str, variant_number: int) -> np.matrix:
    file = open(filename, 'r')
    to_search = '#' + str(variant_number) + '\n'
    line = ''
    
    while line != to_search:
        line = file.readline()

    A_list = []

    line = file.readline()
    while line != '\n':
        line = line[:-1]
        list = [float(num) for num in line.split(',')]
        A_list.append(list)
        line = file.readline()
        
    file.close()
    return np.matrix(A_list)