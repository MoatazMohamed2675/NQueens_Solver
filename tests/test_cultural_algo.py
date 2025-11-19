# ---------------------- FULL GA RUN ----------------------

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.Cultural_Algorithm.PopulationSpace import PopulationSpace


def print_board(solution):
    n = len(solution)
    print("\n--- Chessboard ---")
    for row in range(n):
        line = ""
        for col in range(n):
            if solution[row] == col:
                line += " Q "
            else:
                line += " . "
        print(line)


N = 8
POP_SIZE = 200
MAX_GEN = 3000

ps = PopulationSpace(n=N, population_size=POP_SIZE)

print(f"--- Running Genetic Algorithm for N={N} ---")

solution = ps.n_queens(
    pop_size=POP_SIZE,
    max_generations=MAX_GEN
)

print("\nFinal Solution Returned by GA:", solution)

print_board(solution)
