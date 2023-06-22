import random
import math
import numpy as np

# Parameters
N = 10                 # Number of particles
MAX_ITERATION = 100   # Maximum number of iterations
D = 2                 # Number of dimensions
POS_MAX = 10          # Maximum position in each dimension
POS_MIN = -10         # Minimum position in each dimension
w = 0.5               # Inertia weight
rho_max = 0.5         # Maximum value for rho

# Particle class
class Particle:
    def __init__(self, D):
        self.position = np.random.uniform(POS_MIN, POS_MAX, D)
        self.velocity = np.zeros(D)
        self.pbest = None
        self.pbest_fitness = math.inf
        self.gbest = None
        self.fitness = None

    def set_fitness(self, fitness):
        self.fitness = fitness

    def set_pbest(self):
        if self.pbest is None or self.fitness < self.pbest_fitness:
            self.pbest = self.position.copy()
            self.pbest_fitness = self.fitness

    def set_gbest(self, gbest):
        self.gbest = gbest

    def update_position(self):
        self.position += self.velocity
        self.position = np.clip(self.position, POS_MIN, POS_MAX)

    def update_velocity(self, w, rho_max):
        rho = np.random.uniform(0, rho_max, len(self.velocity))
        self.velocity = w * self.velocity + rho * (self.pbest - self.position) + rho * (self.gbest - self.position)

# Field class
class Field:
    def __init__(self, N, D, function_name):
        self.N = N
        self.D = D
        self.function_name = function_name
        self.gbest = None
        self.gbest_fitness = math.inf
        self.particles = [Particle(D) for _ in range(N)]
        self.update_best()

    def fitness(self, position):
        if self.function_name == "rastrigin":
            return self.D * 10 + np.sum(position ** 2 - 10 * np.cos(2 * np.pi * position))
        elif self.function_name == "rosenbrock":
            return np.sum(100.0 * (position[1:] - position[:-1]**2.0)**2.0 + (1 - position[:-1])**2.0)
        else:
            raise ValueError("Invalid function name")

    def __set_g_best(self):
        p_index = np.argmin([p.fitness for p in self.particles])
        self.gbest = self.particles[p_index].pbest.copy()
        self.gbest_fitness = self.particles[p_index].pbest_fitness

    def update_best(self):
        for particle in self.particles:
            particle.set_fitness(self.fitness(particle.position))
            particle.set_pbest()
        self.__set_g_best()
        for particle in self.particles:
            particle.set_gbest(self.gbest)

    def move_update(self, w, rho_max):
        for particle in self.particles:
            particle.update_velocity(w, rho_max)
            particle.update_position()
            particle.set_fitness(self.fitness(particle.position))

# PSO Algorithm with Rastrigin Function
pso = Field(N, D, "rastrigin")
for i in range(MAX_ITERATION):
    pso.move_update(w, rho_max)
    pso.update_best()
    print(f"Rastrigin, iteration: {i}, gbest: {pso.gbest}, gbest_fitness: {pso.gbest_fitness}")

# PSO Algorithm with Rosenbrock Function
# pso = Field(N, D, "rosenbrock")
# for i in range(MAX_ITERATION):
#     pso.move_update(w, rho_max)
#     pso.update_best()
#     print(f"Rosenbrock, iteration: {i}, gbest: {pso.gbest}, gbest_fitness: {pso.gbest_fitness}")
