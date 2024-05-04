from deap import base, creator, tools, algorithms
import random
import matplotlib.pyplot as plt

# Define the evaluation function
def evaluate(individual):
    """Evaluate the individual: sum of squares function."""
    return sum(x**2 for x in individual),

# Create types
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimize the objective
creator.create("Individual", list, fitness=creator.FitnessMin)

# Initialize the toolbox
toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, -10, 10)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=3)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)

# Generate the population
population = toolbox.population(n=50)

# Prepare to capture the best fitness each generation
fitness_over_time = []

# Apply the genetic algorithm with fitness tracking
for gen in range(51):  # Running for 50 generations
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    
    population = toolbox.select(offspring, k=len(population))
    best_ind = tools.selBest(population, k=1)[0]
    fitness_over_time.append(best_ind.fitness.values[0])

# Output the final best individual and its fitness
print("Best individual (parameters for snowflake):", best_ind)
print("Best fitness (objective function result):", best_ind.fitness.values)

# Visualization of fitness over generations
plt.figure(figsize=(10, 5))
plt.plot(list(range(51)), fitness_over_time, marker='o', linestyle='-')
plt.title('Fitness Over Generations')
plt.xlabel('Generation')
plt.ylabel('Best Fitness')
plt.grid(True)
plt.show()
