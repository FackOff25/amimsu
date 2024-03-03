import numpy as np
import dijkstra

def get_sets(matrix: np.matrix) -> dict:
    result = {0:[]}
    inf = float('inf')
    for v in range(len(matrix)):
        paths = get_paths(matrix, v)
        if not inf in paths:
            result[0].append(v)
            continue
        notAdded = True
        for set in result.keys():
            if v in result[set]:
                notAdded = False
                break
        if notAdded:
            newSetId = len(result)
            result[newSetId] = []
            for idx in range(len(paths)):
                if paths[idx] != inf:
                    result[newSetId].append(idx)
        
    return result
 
def get_paths(matrix: np.matrix, source: int) -> list:
    return dijkstra.dijkstra_algorithm(matrix.tolist(), source)

def get_new_id(sets: dict, oldId: int) -> int:
    newId = 0
    for set in range(len(sets)):
        if oldId not in sets[set]:
            newId += len(sets[set])
        else:
            for idx in range(len(sets[set])):
                if sets[set][idx] == oldId:
                    newId += idx
                    break
            break
    return newId

def transform_to_packed_matrix(matrix: np.matrix) -> np.matrix:
    sets = get_sets(matrix)
    result = np.zeros((len(matrix), len(matrix)))
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            result[get_new_id(sets, i)][get_new_id(sets, j)] = matrix.item(i, j)
    
    return result

    