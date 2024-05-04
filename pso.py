import pyswarms as ps
import numpy as np

# Define a more relevant objective function
def snowflake_behavior(x):

    return np.sum((x[:,0]-5)**2 + (x[:,1]-5)**2, axis=1)  # Example function

# Setup hyperparameters
options = {'c1': 0.6, 'c2': 0.4, 'w': 0.9}

# Create a swarm
optimizer = ps.single.GlobalBestPSO(n_particles=50, dimensions=2, options=options)

# Perform optimization
cost, pos = optimizer.optimize(snowflake_behavior, iters=100)

print("Best position (parameters for snowflake):", pos)
print("Minimum cost (objective function result):", cost)
