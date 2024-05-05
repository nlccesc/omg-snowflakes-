import pandas as pd
import numpy as np
from deap import base, creator, tools, algorithms
from lifelines import KaplanMeierFitter
import pyswarms as ps
import random
import multiprocessing

# Load and preprocess CSV data
df = pd.read_csv('C:\\Users\\haoha\\OneDrive\\Desktop\\personal\\Projects\\Personal\\WIP\\omg-snowflakes--main\\snowflake_data.csv')

# Define the snowflake simulation function
def simulate_snowflake(simulated_x, simulated_y, n_snowflakes=100, temperature_threshold=5, max_time=100):
    # If scalar values are passed in, convert them to arrays
    if np.isscalar(simulated_x) and np.isscalar(simulated_y):
        simulated_x = np.full(n_snowflakes, simulated_x)
        simulated_y = np.full(n_snowflakes, simulated_y)
        
    time_to_failure = np.zeros(n_snowflakes)
    censored = np.ones(n_snowflakes, dtype=bool)
    for i in range(n_snowflakes):
        current_temperature = 0
        for t in range(max_time):
            current_temperature = 0.1 * t - 0.01 * (simulated_x[i] + simulated_y[i])
            if current_temperature > temperature_threshold:
                time_to_failure[i] = t
                censored[i] = False
                break
    return pd.DataFrame({
        'Time_to_Failure': time_to_failure,
        'Censored': censored
    })

# Define the survival function using Kaplan-Meier estimator
def survival_function(df):
    kmf = KaplanMeierFitter()
    kmf.fit(df['Time_to_Failure'], event_observed=1 - df['Censored'])
    return kmf.median_survival_time_

# Define the evaluation function using survival analysis for GA
def evaluate(individual):
    simulated_x, simulated_y = individual[0], individual[1]
    df = simulate_snowflake(simulated_x, simulated_y)
    median_survival_time = survival_function(df)
    if np.isinf(median_survival_time):
        return (1e6,)  # Return a large positive number if median_survival_time is infinity
    else:
        return (1000 - median_survival_time,)

# Initial Parameters (average positions) and calculate initial_error
initial_params = df[['X Position', 'Y Position']].mean().values
initial_df = simulate_snowflake(initial_params[0], initial_params[1])
initial_error = evaluate(initial_params)[0]  # Evaluate initial parameters

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
    fitness = np.zeros(x.shape[0])
    for i in range(x.shape[0]):
        simulated_x, simulated_y = x[i, 0], x[i, 1]
        df = simulate_snowflake(simulated_x, simulated_y)
        median_survival_time = survival_function(df)
        if np.isinf(median_survival_time):
            fitness[i] = 1e6  # Use a large positive number if median_survival_time is infinity
        else:
            fitness[i] = 1000 - median_survival_time
    return fitness

# Setup and run Particle Swarm Optimization using GA's best position
options_pso = {'c1': 0.8, 'c2': 0.7, 'w': 0.6}
n_particles = 50
dimensions = 2
iters_pso = 300

optimizer = ps.single.GlobalBestPSO(n_particles=n_particles, dimensions=dimensions, options=options_pso)
cost_pso, pos_pso = optimizer.optimize(pso_fitness_with_ga_best, iters=iters_pso)

# Define the pool of workers for parallel processing
pool = multiprocessing.Pool()

# Modify the toolbox to use the pool of workers for evaluation
toolbox.register("map", pool.map)

# Define a grid of parameters for GA and PSO
ga_parameters = {'cxpb': [0.5, 0.7, 0.9], 'mutpb': [0.1, 0.2, 0.3]}
pso_parameters = {'c1': [0.5, 0.7, 0.9], 'c2': [0.3, 0.5, 0.7], 'w': [0.4, 0.6, 0.8]}

# Calculate Improvement Percentage
optimized_error = evaluate(best_ind_ga)[0]
improvement_percentage = 100 * (initial_error - min(optimized_error, cost_pso)) / initial_error

print("Initial error (baseline):", initial_error)
print("Optimized error from GA:", optimized_error)
print("Optimized error from PSO (best cost):", cost_pso)
print("Improvement Percentage:", improvement_percentage)
print("Best position from PSO (parameters for snowflake):", pos_pso)
