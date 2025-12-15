import numpy as np
import random

class PopulationSpace:
    def __init__(self, n, population_size):
        self.n = n
        self.population_size = population_size
        self.population = [self.create_chromosome() for _ in range(population_size)]

    def create_chromosome(self):
        return np.random.randint(0, self.n, size=self.n).tolist()

    def fittness(self, population):
        pop = np.array(population)
        n = self.n

        penalties = np.zeros(len(pop), dtype=int)

        for i in range(n):
            for j in range(i + 1, n):
                d = j - i
                penalties += (pop[:, i] == pop[:, j])          # same row
                penalties += (pop[:, i] == pop[:, j] - d)      # main diagonal
                penalties += (pop[:, i] == pop[:, j] + d)      # other diagonal

        return -penalties

    # --- FASTER SELECTION ---
    def selection(self, population, fitness):
        fitness_shifted = fitness - fitness.min() + 1
        probs = fitness_shifted / fitness_shifted.sum()

        idx = np.random.choice(len(population), size=2, replace=False, p=probs)
        return population[idx[0]], population[idx[1]]

    # --- UNIFORM CROSSOVER (FASTER & BETTER FOR N-QUEENS) ---
    # def crossover(self, p1, p2):
    #     mask = np.random.randint(0, 2, size=self.n)
    #     c1 = [p1[i] if mask[i] else p2[i] for i in range(self.n)]
    #     c2 = [p2[i] if mask[i] else p1[i] for i in range(self.n)]
    #     return c1, c2
    def crossover(self, p1, p2):

        cp = np.random.randint(1, self.n - 1)

        c1 = p1[:cp] + p2[cp:]
        c2 = p2[:cp] + p1[cp:]

        return c1, c2

    # --- FAST MUTATION ---
    def mutate(self, chrom, pm):
        if random.random() < pm:
            i = random.randrange(self.n)
            chrom[i] = random.randrange(self.n)
        return chrom

    # --- FULL OPERATOR PIPELINE ---
    def crossover_mutation(self, selected_pop, pm):
        new_pop = []

        for i in range(0, len(selected_pop), 2):
            if i + 1 >= len(selected_pop):
                new_pop.append(selected_pop[i])
                break

            p1, p2 = selected_pop[i], selected_pop[i + 1]
            c1, c2 = self.crossover(p1, p2)

            self.mutate(c1, pm)
            self.mutate(c2, pm)

            new_pop.extend([c1, c2])

        return new_pop
