import numpy as np
import random
import matplotlib.pyplot as plt

def simulate_step(step_vector: list) -> int:
    generated = random.uniform(0, 1)
    for i in range(len(step_vector)):
        generated -= step_vector[i]
        if generated < 0:
            return i
    return len(step_vector)-1

def simulate_a_lot_of_steps(P: np.matrix, start_state: int, steps_number: int) -> (np.array, dict):
    state = start_state
    results = list([state])
    visit_count = {}
    P = P.tolist()
    for i in range (len(P)):
        visit_count[i] = 0
    for i in range(steps_number):
        step_vector = P[state]
        state = simulate_step(step_vector)
        results.append(state)
        visit_count[state] += 1
    return np.array(results), visit_count

def make_plot(state_list: list, file: str):
    plt.xlabel('Шаг')
    plt.ylabel('Состояние')
    plt.plot(range(len(state_list)), state_list)
    plt.savefig(file)

def clear_plot():
    plt.clf()
