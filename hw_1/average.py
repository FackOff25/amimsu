import numpy as np

def calculate_average_vector(vectors: list) -> list:
    vec_len = len(vectors[0])
    average = np.zeros(vec_len)
    for v in vectors:
        for i in range(vec_len):
            average[i] += v[i]

    for i in range(len(vectors[0])):
        average[i] /= len(vectors)

    return average

def calculate_square_errors(vectors: list) -> list:
    vec_len = len(vectors[0])
    average = calculate_average_vector(vectors)
    square = np.zeros(vec_len)
    for v in vectors:
        for i in range(vec_len):
            square[i] += (v[i] - average[i]) ** 2

    for i in range(vec_len):
        square[i] /= vec_len
        square[i] = np.sqrt(square[i])

    return square

def calculate_fixed_square_errors(vectors: list) -> list:
    vec_len = len(vectors[0])
    average = calculate_average_vector(vectors)
    square = np.zeros(vec_len)
    for v in vectors:
        for i in range(vec_len):
            square[i] += (v[i] - average[i]) ** 2
    
    for i in range(vec_len):
        square[i] /= vec_len - 1
        square[i] = np.sqrt(square[i])

    return square