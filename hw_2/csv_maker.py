import numpy as np

def get_vector(vector: list) -> str:
    return get_vector_sep(vector, ',')

def get_vector_sep(vector: list, separator: str) -> str:
    line = ""
    for el in vector:
        line += str("{:.2f}".format(el)) + separator
    line = line[:-1]
    return line


def get_matrix(matrix: np.matrix):
    result = ""
    for vector in matrix.tolist():
        line = get_vector(vector)
        result += line + '\n'
    return result

def get_matrix_sep(matrix: np.matrix, separator: str):
    result = ""
    for vector in matrix.tolist():
        line = get_vector_sep(vector, separator)
        result += line + '\n'
    return result