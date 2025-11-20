# ---------------------- FULL GA RUN ----------------------
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms.Cultural_Algorithm.CA import CulturalAlgorithm
from algorithms.Cultural_Algorithm.PopulationSpace import PopulationSpace
import numpy as np
# # test GA For N-Queens Problem

# def print_board(solution):
#     n = len(solution)
#     print("\n--- Chessboard ---")
#     for row in range(n):
#         line = ""
#         for col in range(n):
#             if solution[row] == col:
#                 line += " Q "
#             else:
#                 line += " . "
#         print(line)


# N = 8
# POP_SIZE = 200
# MAX_GEN = 3000

# ps = PopulationSpace(n=N, population_size=POP_SIZE)

# print(f"--- Running Genetic Algorithm for N={N} ---")

# solution = ps.n_queens(
#     pop_size=POP_SIZE,
#     max_generations=MAX_GEN
# )

# print("\nFinal Solution Returned by GA:", solution)

# print_board(solution)

# test CA For N-Queens Problem 



def print_board(solution):
    n = len(solution)
    print("\nFinal N-Queens Board:")
    for row in range(n):
        line = ""
        for col in range(n):
            if solution[col] == row:
                line += " Q "
            else:
                line += " . "
        print(line)
    print()

# ----------------------------
# RUN CULTURAL ALGORITHM
# ----------------------------
n = 3
ca = CulturalAlgorithm(n=n, population_size=200, mutation_rate=0.5, max_generations=5000)

print("\nRunning Cultural Algorithm...")
solution = ca.run()

if solution:
    print("\nSolution Found!")
    print("Chromosome:", solution)
    print_board(solution)
else:
    print("\nNo solution found.")


# test GA VS CA Performance Comparison


# def run_GA_only(n=8, pop_size=150, max_gens=5000, mutation_rate=0.01):
#     PS = PopulationSpace(n, pop_size)
#     population = PS.population

#     for gen in range(max_gens):
#         fitness = PS.fittness(population)
#         best_idx = np.argmax(fitness)
#         best_fit = fitness[best_idx]

#         if best_fit == 0:
#             return gen, population[best_idx]  # Found

#         selected = []
#         for _ in range(pop_size // 2):
#             p1, p2 = PS.selection(population, fitness)
#             selected.append(p1)
#             selected.append(p2)

#         population = PS.crossover_mutation(selected, mutation_rate)

#     return None, None  # No solution


# def print_board(solution):
#     n = len(solution)
#     print("\nBoard:")
#     for r in range(n):
#         line = ""
#         for c in range(n):
#             line += " Q " if solution[c] == r else " . "
#         print(line)
#     print()


# # --------------------------
# # RUN GA ONLY
# # --------------------------
# print("\n--- Running GA ONLY ---")
# gen_ga, sol_ga = run_GA_only()

# if sol_ga is not None:
#     print(f"GA found solution at generation {gen_ga}")
#     print("Solution:", sol_ga)
#     print_board(sol_ga)
# else:
#     print("GA failed to find solution.")


# # --------------------------
# # RUN CULTURAL ALGORITHM
# # --------------------------
# print("\n--- Running CA (GA + Belief Space) ---")
# ca = CulturalAlgorithm(n=8, population_size=150, mutation_rate=0.01)
# sol_ca = ca.run()

# print("\nCA Solution:", sol_ca)
# print_board(sol_ca)
