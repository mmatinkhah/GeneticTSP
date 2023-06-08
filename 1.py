from pyeasyga import pyeasyga
import random
def mutate_swap(individual):
    size = len(individual)
    pos_1 = random.randint(0, size - 1)
    pos_2 = random.randint(0, size - 1)
    individual[pos_1], individual[pos_2] = individual[pos_2], individual[pos_1]

def ordered_crossover(parent_1, parent_2):
    size = len(parent_1)
    child_1 = [-1] * size
    child_2 = [-1] * size

    # Select random positions for the crossover
    start_pos = random.randint(0, size - 1)
    end_pos = random.randint(0, size - 1)

    # Make sure start_pos is smaller than end_pos
    if start_pos > end_pos:
        start_pos, end_pos = end_pos, start_pos

    # Copy the selected portion from parents to children
    for i in range(start_pos, end_pos + 1):
        child_1[i] = parent_1[i]
        child_2[i] = parent_2[i]

    # Fill the remaining positions with the remaining cities from parents
    # in the order they appear
    pointer_1, pointer_2 = 0, 0
    for i in range(size):
        if child_1[i] == -1:
            while parent_2[pointer_2] in child_1:
                pointer_2 += 1
            child_1[i] = parent_2[pointer_2]
            pointer_2 += 1

        if child_2[i] == -1:
            while parent_1[pointer_1] in child_2:
                pointer_1 += 1
            child_2[i] = parent_1[pointer_1]
            pointer_1 += 1

    return child_1, child_2

# Define the distance matrix
distances = [
    [0, 51, 44, 64, 19, 42, 94, 57, 76, 23],
    [51, 0, 35, 39, 100, 13, 20, 92, 91, 40],
    [44, 35, 0, 25, 49, 64, 85, 34, 66, 89],
    [64, 39, 25, 0, 92, 10, 60, 80, 44, 23],
    [19, 100, 49, 92, 0, 28, 96, 10, 73, 53],
    [42, 13, 64, 10, 28, 0, 60, 79, 20, 57],
    [94, 20, 85, 60, 96, 60, 0, 82, 16, 26],
    [57, 92, 34, 80, 10, 79, 82, 0, 51, 69],
    [76, 91, 66, 44, 73, 20, 16, 51, 0, 35],
    [23, 40, 89, 23, 53, 57, 26, 69, 35, 0]
]

# Create an instance of the pyeasyga class
ga = pyeasyga.GeneticAlgorithm([], population_size=200)

# Define the required functions for pyeasyga

# Function to create an individual with a random permutation of cities
def create_individual(data):
    individual = list(range(len(data)))
    random.shuffle(individual)
    return individual

# Function to calculate the total distance of an individual (route)
def calculate_distance(individual, data):
    distance = 0
    if len(individual) > 1:
        for i in range(len(individual) - 1):
            start_city = individual[i]
            end_city = individual[i + 1]
            distance += data[start_city][end_city]
        distance += data[individual[-1]][individual[0]]  # Swap indices of last and first city
    return distance

# Set the required functions
ga.create_individual = create_individual

def fitness_function(individual, data):
    distance = calculate_distance(individual, data)
    if distance == 0:
        return 1e-10  # Assign a very low fitness value if distance is zero
    else:
        return 1.0 / distance

ga.fitness_function = fitness_function
ga.crossover_function = ordered_crossover
ga.mutate_function = mutate_swap

# Set the distance matrix as an attribute of the ga object
ga.seed_data = distances

# Run the GA
ga.run()

# Print the best individual and its distance
best_individual = ga.best_individual()[1]
best_distance = calculate_distance(best_individual, distances)
print("Best Individual:", best_individual)
print("Best Distance:", best_distance)
