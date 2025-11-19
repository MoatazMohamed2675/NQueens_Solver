import random
import numpy as np

class PopulationSpace:
    def __init__(self, n, population_size):
        self.n = n
        self.population_size = population_size
        self.population = [self.create_chromosome() for _ in range(population_size)]

    def create_chromosome(self):
        return [random.randint(0, self.n - 1) for _ in range(self.n)]
    
    def fittness(self, population, chromosome=None):
        fitness_values = []
        for chrom in population:
            penalty = 0
            for i in range(self.n):
                r = chrom[i]  # column of queen
                for j in range(i + 1, self.n):
                    d = abs(i - j)
                    if chrom[j] in {r, r - d, r + d}:
                        penalty += 1
            fitness_values.append(penalty)
        return -1 * np.array(fitness_values)
    
    def selection(self, population, fitness_values):
        # Convert fitness to positive probabilities
        probs = fitness_values.copy()
        
        # Shift if there are negatives
        shift = abs(min(probs)) + 1
        probs = [p + shift for p in probs]

        # Normalize to probabilities
        probs = [f / sum(probs) for f in probs]

        # Choose *two* parents according to probabilities
        indices = np.arange(len(population))
        selected_indices = np.random.choice(indices, size=2, replace=False, p=probs)

        parent1 = population[selected_indices[0]]
        parent2 = population[selected_indices[1]]

        return parent1, parent2

    
    def crossover(self, parent1, parent2):
        cp = random.randint(1, self.n - 2)

        child1 = parent1[:cp] + parent2[cp:]
        child2 = parent2[:cp] + parent1[cp:]

        return [child1, child2]


    def mutate(self, chromosome, mutation_rate=0.1):

        # Check if mutation should happen based on the rate
        if random.random() < mutation_rate:
            # Choose two distinct positions (genes) to swap
            idx1, idx2 = random.sample(range(self.n), 2)
            
            # Perform the swap (swap mutation)
            chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
            
            
        return chromosome

    def crossover_mutation(self, selected_pop, pm):

        N = len(selected_pop)
        new_pop_list = [] # Use list for easy assignment and list-based crossover

        # 1. Crossover: Pair and cross parents
        for i in range(0, N, 2):
            parent1 = selected_pop[i]
            
            # Handle odd size
            if i + 1 >= N:
                new_pop_list.append(parent1)
                break

            parent2 = selected_pop[i + 1]

            # Generate two children (pc is included in the signature but ignored as your crossover is unconditional)
            children = self.crossover(parent1, parent2)
            
            new_pop_list.extend(children)
        
        # 2. Mutation: Loop through all children
        for i in range(len(new_pop_list)):
            # pm (mutation rate) is passed here
            # self.mutate modifies the chromosome list in place.
            self.mutate(new_pop_list[i], pm) 
            
        # 3. Return the new population (NO self.population update here)
        return new_pop_list
    def n_queens(self, pop_size=100, max_generations=10000):

        population = self.population
        best_fitness_overall = None
        best_solution = None

        for gen in range(max_generations):

            # FITNESS
            fitness_vals = self.fittness(population)

            best_idx = np.argmax(fitness_vals)
            best_fitness = fitness_vals[best_idx]

            if best_fitness_overall is None or best_fitness > best_fitness_overall:
                best_fitness_overall = best_fitness
                best_solution = population[best_idx]

            print(f"\rGen={gen:06d} -f={int(-best_fitness_overall):03d}", end='')

            if best_fitness == 0:
                print("\nFound optimal solution")
                break

            # SELECTION
            selected = []
            for _ in range(pop_size // 2):
                p1, p2 = self.selection(population, fitness_vals)
                selected.append(p1)
                selected.append(p2)

            # CROSSOVER + MUTATION
            new_population = self.crossover_mutation(selected, pm=0.01)

            population = new_population[:pop_size]

        print("\nBest solution:", best_solution)
        return best_solution

