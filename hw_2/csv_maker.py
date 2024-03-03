import numpy as np

def get_vector(vector: list) -> str:
    line = ""
    for el in vector:
        line += str("{:.2f}".format(el)) + ','
    line = line[:-1]
    return line


def get_matrix(matrix: np.matrix):
    result = ""
    for vector in matrix.tolist():
        line = get_vector(vector)
        result += line + '\n'
    return result