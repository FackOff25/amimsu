import numpy as np

def calculate_average_vector(vectors: list) -> list:
    vec_len = len(vectors[0])
    average = np.zeros(vec_len)
    for v in vectors:
        for i in range(vec_len):
            average[i] += v[i]

    for i in range(len(vectors[0])):
        average /= vec_len

    return average

def calculate_squear_errors(vectors: list) -> list:
    vec_len = len(vectors[0])
    average = calculate_average_vector(vectors)
    squear = np.zeros(vec_len)
    for v in vectors:
        for i in range(vec_len):
            squear[i] += (v[i] - average[i]) ** 2

    for i in range(vec_len):
        squear[i] /= vec_len
        squear[i] = np.sqrt(squear[i])

    return squear