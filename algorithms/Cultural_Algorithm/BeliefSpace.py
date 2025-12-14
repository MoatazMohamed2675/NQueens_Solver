import numpy as np

class BeliefSpace:
    def __init__(self, n, min_width=1):
        self.n = n
        self.min_width = min_width

        self.ranges = np.array([[0, n - 1] for _ in range(n)], dtype=int)

        self.last_best = None
        self.no_improve = 0

        self.tighten_ratio = 0.15
        self.widen_threshold = 50
        self.widen_step = 1

    def update(self, population, fitness):
        best = fitness.max()

        if self.last_best is None or best > self.last_best:
            self.last_best = best
            self.no_improve = 0
            self._tighten(population, fitness)
        else:
            self.no_improve += 1

        if self.no_improve > self.widen_threshold:
            self._widen()
            self.no_improve = 0

    # --- FAST TIGHTEN ---
    def _tighten(self, population, fitness):
        pop = np.array(population)
        k = max(1, int(len(pop) * self.tighten_ratio))

        elite_ids = np.argsort(fitness)[-k:]
        elites = pop[elite_ids]

        new_low = elites.min(axis=0)
        new_high = elites.max(axis=0)

        self.ranges = np.vstack((new_low, new_high)).T

    # --- FAST WIDEN ---
    def _widen(self):
        self.ranges[:, 0] = np.clip(self.ranges[:, 0] - self.widen_step, 0, self.n - 1)
        self.ranges[:, 1] = np.clip(self.ranges[:, 1] + self.widen_step, 0, self.n - 1)

    # --- FAST INFLUENCE ---
    def influence(self, population):
        pop = np.array(population)
        low = self.ranges[:, 0]
        high = self.ranges[:, 1]

        influenced = np.clip(pop, low, high)
        return influenced.tolist()
