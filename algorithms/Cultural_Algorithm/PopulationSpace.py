import numpy as np
import random

class PopulationSpace:
    def __init__(self, n, population_size):
        self.n = n
        self.population_size = population_size
        self.population = [self.create_chromosome() for _ in range(population_size)]

    def create_chromosome(self):
        return np.random.randint(0, self.n, size=self.n).tolist()

    # --- FAST VECTORIZED FITNESS ---
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
    def crossover(self, p1, p2):
        mask = np.random.randint(0, 2, size=self.n)
        c1 = [p1[i] if mask[i] else p2[i] for i in range(self.n)]
        c2 = [p2[i] if mask[i] else p1[i] for i in range(self.n)]
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




# import random
# import numpy as np

# class PopulationSpace:
#     def __init__(self, n, population_size):
#         self.n = n
#         self.population_size = population_size
#         self.population = [self.create_chromosome() for _ in range(population_size)] # --> Create initial population

#     def create_chromosome(self):
#         return [random.randint(0, self.n - 1) for _ in range(self.n)]  # --> Create randoms positons for queens
    
#     def fittness(self, population, chromosome=None): # Calculate fitness values for  each chromsomes in the population
#         fitness_values = []
#         for chrom in population:
#             penalty = 0
#             for i in range(self.n):
#                 r = chrom[i]  # column of queen
#                 for j in range(i + 1, self.n):
#                     d = abs(i - j)
#                     if chrom[j] in {r, r - d, r + d}:
#                         penalty += 1
#             fitness_values.append(penalty)
#         return -1 * np.array(fitness_values)
    
#     def selection(self, population, fitness_values):
#         # Convert fitness to positive probabilities
#         probs = fitness_values.copy()
        
#         # Shift if there are negatives
#         shift = abs(min(probs)) + 1
#         probs = [p + shift for p in probs]

#         # Normalize to probabilities
#         probs = [f / sum(probs) for f in probs]

#         # Choose *two* parents according to probabilities
#         indices = np.arange(len(population))
#         selected_indices = np.random.choice(indices, size=2, replace=False, p=probs)

#         parent1 = population[selected_indices[0]]
#         parent2 = population[selected_indices[1]]

#         return parent1, parent2

    
#     def crossover(self, parent1, parent2):
#         cp = random.randint(1, self.n - 2) # random point for Crossover

#         child1 = parent1[:cp] + parent2[cp:]
#         child2 = parent2[:cp] + parent1[cp:]

#         return [child1, child2]


#     def mutate(self, chromosome, mutation_rate=0.1):

#         # Check if mutation should happen based on the rate
#         if random.random() < mutation_rate:
#             # Choose two distinct positions (genes) to swap
#             idx1, idx2 = random.sample(range(self.n), 2)
            
#             # Perform the swap (swap mutation)
#             chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
            
#         return chromosome

#     def crossover_mutation(self, selected_pop, pm):

#         N = len(selected_pop)
#         new_pop_list = [] # Use list for easy assignment and list-based crossover

#         # 1. Crossover: Pair and cross parents
#         for i in range(0, N, 2):
#             parent1 = selected_pop[i]
            
#             # Handle odd size
#             if i + 1 >= N:
#                 new_pop_list.append(parent1)
#                 break

#             parent2 = selected_pop[i + 1]

#             # Generate two children
#             children = self.crossover(parent1, parent2)
            
#             new_pop_list.extend(children)
        
#         # 2. Mutation
#         for i in range(len(new_pop_list)):
#             self.mutate(new_pop_list[i], pm) 
            
#         # 3. Return new population
#         return new_pop_list

