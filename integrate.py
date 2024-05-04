import pandas as pd
import numpy as np
from deap import base, creator, tools, algorithms
import pyswarms as ps
import random

# Load and preprocess CSV data
df = pd.read_csv('your_file_path.csv')

# Initial Parameters (assuming a simple random choice for baseline)
initial_params = [np.random.uniform(-100, 100), np.random.uniform(-100, 100)]
initial_error = np.sum((initial_params - df[['X Position', 'Y Position']].mean().values)**2)

# Define the evaluation function using historical data for GA
def evaluate(individual):
    simulated_x, simulated_y = individual[0], individual[1]
    error = (simulated_x - df['X Position'].mean())**2 + (simulated_y - df['Y Position'].mean())**2
    return error,

# Setup for Genetic Algorithm
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, -100, 100)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=2)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

# Initialize population and run GA
population = toolbox.population(n=50)
result = algorithms.eaSimple(population, toolbox, cxpb=0.8, mutpb=0.2, ngen=150, verbose=True)

# Extract best individual from GA
best_ind_ga = tools.selBest(population, k=1)[0]

# Define PSO fitness function using GA's best position
def pso_fitness_with_ga_best(x):
    return np.sum((x - best_ind_ga)**2, axis=1)

# Setup and run Particle Swarm Optimization using GA's best position
options_pso = {'c1': 0.8, 'c2': 0.7, 'w': 0.6}
n_particles = 50
dimensions = 2
iters_pso = 300

optimizer = ps.single.GlobalBestPSO(n_particles=n_particles, dimensions=dimensions, options=options_pso)
cost_pso, pos_pso = optimizer.optimize(pso_fitness_with_ga_best, iters=iters_pso)

# Calculate Improvement Percentage
optimized_error = evaluate(best_ind_ga)[0]
improvement_percentage = 100 * (initial_error - min(optimized_error, cost_pso)) / initial_error

print("Initial error (baseline):", initial_error)
print("Optimized error from GA:", optimized_error)
print("Optimized error from PSO (best cost):", cost_pso)
print("Improvement Percentage:", improvement_percentage)
print("Best position from PSO (parameters for snowflake):", pos_pso)
