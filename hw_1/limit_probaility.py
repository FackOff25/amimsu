import numpy as np

def get_limit_probability_vector(P: np.matrix) -> np.matrix:
    A = P.transpose()
    E = np.eye(len(P))
    A = A - E
    right_part = np.zeros(len(P))
    right_part[-1] = 1
    A[-1] = np.ones(len(P))
    result = np.linalg.lstsq(A, right_part, rcond=None)[0]
    return result

def get_limit_probability_matrix(P: np.matrix) -> np.matrix:
    return np.matrix([get_limit_probability_vector(P) for i in range(len(P))])

def check_limit_matrix(P: np.matrix, error: float) -> bool:
    length = len(P)
    vector = P[0]
    P = P.transpose()
    checkers = np.eye(length)
    for checker in checkers:
        if not np.isclose(P.dot(checker), vector, atol=error).all():
            return False
        
    for i in range(10):
        checker = np.random.dirichlet(np.ones(len(P)),size=1)[0]
        if not np.isclose(P.dot(checker), vector, atol=error).all():
            return False
    return True