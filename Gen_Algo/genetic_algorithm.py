import random
import numpy 
from deap import base, creator, tools, algorithms

class CustomRandom():
    def __init__(self, seed=1):
        self.seed = seed
        self.state = seed

    def random(self):
        """Implement a linear congruential generator for demonstration purposes."""
        self.state = (1103515245 * self.state + 12345) % (2**31)
        return self.state / (2**31)

# Define the target string
TARGET_STRING = "Hello, World!"

# Define the fitness function
def fitness(individual):
    return sum(ind_char == target_char for ind_char, target_char in zip(individual, TARGET_STRING)),

# Define the individual and population
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

# Initialize your custom random number generator
my_rng = CustomRandom()
random.seed(my_rng.random())

toolbox.register("random", my_rng.random)
# Define the gene
toolbox.register("attr_char", random.choice, 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!, ')

# Define the individual and population
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_char, len(TARGET_STRING))
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Define the operators
toolbox.register("evaluate", fitness)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=len(TARGET_STRING)-1, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)

# Run the genetic algorithm
def main():
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    #pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=40, 
    #                               stats=stats, halloffame=hof, verbose=True)

    for gen in range(40):  # number of generations
        algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=1, 
                            stats=stats, halloffame=hof, verbose=True)
        # Print the best individual of the current generation
        best_ind = tools.selBest(pop, 1)[0]
        print("Generation: ", gen, " Best individual: ", ''.join(str(best_ind)))

    #return pop, log, hof
    return pop, hof

if __name__ == "__main__":
    main()
