import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))            # current folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # parent folder

from PopulationSpace import PopulationSpace
from BeliefSpace import BeliefSpace
import numpy as np

class CulturalAlgorithm:
    def __init__(self, n, population_size=300, mutation_rate=0.01, max_generations=5000):
        self.n = n
        self.pop_size = population_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations

        self.PS = PopulationSpace(n, population_size)
        self.BS = BeliefSpace(n)

    def run(self, log_callback=None):
        population = self.PS.population
        best_solution = None
        best_conflicts = None

        for gen in range(self.max_generations):

            fitness = self.PS.fittness(population)
            self.BS.update(population, fitness)

            best_idx = fitness.argmax()
            best_fit = fitness[best_idx]
            print(f"\rGen={gen:05d} | conflicts={-best_fit:03d}", end="")
            if log_callback:
                log_callback(f"Gen={gen:05d} | conflicts={-best_fit}")

            best_conflicts = -best_fit
            best_solution = population[best_idx]

            if best_fit == 0:
                if log_callback:
                    log_callback("Solution Found!")
                return best_solution

            # SELECTION
            selected = [
                p for _ in range(self.pop_size // 2)
                for p in self.PS.selection(population, fitness)
            ]

            # VARIATION
            new_population = self.PS.crossover_mutation(selected, self.mutation_rate)

            # CULTURAL INFLUENCE
            population = self.BS.influence(new_population)

        if log_callback:
            log_callback(f"No perfect solution found. Final conflicts: {best_conflicts}")

        return None

