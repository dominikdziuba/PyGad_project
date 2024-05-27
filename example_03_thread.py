#na podstawie przykładu: https://pypi.org/project/pygad/1.0.18/
import logging
import pygad
import numpy as np
import benchmark_functions as bf
import random
#Konfiguracja algorytmu genetycznego

num_genes = 2
func = bf.Ackley(n_dimensions=num_genes)
def fitness_func(ga_instance, solution, solution_idx):
    fitness = func(solution)
    return 1./fitness

def fitness_fun(ga_instance, solution):
    fitness = func(solution)
    return 1./fitness


fitness_function = fitness_func
num_generations = 100
sol_per_pop = 6
num_parents_mating = 3
#boundary = func.suggested_bounds() #możemy wziąć stąd zakresy
init_range_low = -32.768
init_range_high = 32.768
mutation_num_genes = 1
parent_selection_type = "tournament"


def crossover_func(parents, offspring_size, ga_instance):
    offspring = []
    idx = 0
    while len(offspring) != offspring_size[0]:
        parent1 = parents[idx % parents.shape[0], :].copy()
        parent2 = parents[(idx + 1) % parents.shape[0], :].copy()

        random_split_point = np.random.choice(range(offspring_size[1]))

        parent1[random_split_point:] = parent2[random_split_point:]

        offspring.append(parent1)

        idx += 1
    return np.array(offspring)


def imperfect_crossover(parents, offspring_size, ga_instance):
    offspring = []
    idx = 0
    while len(offspring) != offspring_size[0]:
        parent1 = parents[idx % parents.shape[0], :].copy()
        parent2 = parents[(idx + 1) % parents.shape[0], :].copy()
        rand_temp = random.uniform(0, 1)
        point = random.randint(1, len(parent1) - 1)
        child1 = [0] * len(parent1)
        child2 = [0] * len(parent2)

        if rand_temp < 0.33:
            child1[:point - 1] = parent1[:point - 1]
            child1[point + 1:] = parent2[point + 1:]
            child1[point] = np.random.uniform(np.min(parent1), np.max(parent1))

            child2[:point - 1] = parent2[:point - 1]
            child2[point + 1:] = parent1[point + 1:]
            child2[point] = np.random.uniform(np.min(parent2), np.max(parent2))
        elif rand_temp < 0.66:
            child1[:point - 1] = parent1[:point - 1]
            child1[point + 1:] = parent2[point + 1:]
            child1[point] = 0

            child2[:point - 1] = parent2[:point - 1]
            child2[point + 1:] = parent1[point + 1:]
            child2[point] = 0
        else:
            child1[:point] = parent1[:point]
            child1[point:] = parent2[point:]

            child2[:point] = parent2[:point]
            child2[point:] = parent1[point:]

        offspring.append(child1)
        offspring.append(child2)
        idx += 1

    return np.array(offspring)

def mutation_func(offspring, ga_instance):

    for chromosome_idx in range(offspring.shape[0]):
        random_gene_idx = np.random.choice(range(offspring.shape[1]))

        offspring[chromosome_idx, random_gene_idx] += np.random.random()
    return offspring

#Konfiguracja logowania

level = logging.DEBUG
name = 'logfile.txt'
logger = logging.getLogger(name)
logger.setLevel(level)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_format = logging.Formatter('%(message)s')
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)

def on_generation(ga_instance):
    ga_instance.logger.info("Generation = {generation}".format(generation=ga_instance.generations_completed))
    solution, solution_fitness, solution_idx = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)
    ga_instance.logger.info("Best    = {fitness}".format(fitness=1./solution_fitness))
    ga_instance.logger.info("Individual    = {solution}".format(solution=repr(solution)))

    tmp = [1./x for x in ga_instance.last_generation_fitness] #ponownie odwrotność by zrobić sobie dobre statystyki

    ga_instance.logger.info("Min    = {min}".format(min=np.min(tmp)))
    ga_instance.logger.info("Max    = {max}".format(max=np.max(tmp)))
    ga_instance.logger.info("Average    = {average}".format(average=np.average(tmp)))
    ga_instance.logger.info("Std    = {std}".format(std=np.std(tmp)))
    ga_instance.logger.info("\r\n")


#Właściwy algorytm genetyczny

ga_instance = pygad.GA(num_generations=num_generations,
          sol_per_pop=sol_per_pop,
          num_parents_mating=num_parents_mating,
          num_genes=num_genes,
          fitness_func=fitness_func,
          init_range_low=init_range_low,
          init_range_high=init_range_high,
          mutation_num_genes=mutation_num_genes,
          parent_selection_type=parent_selection_type,
          crossover_type=imperfect_crossover,
          mutation_type=mutation_func,
          keep_parents= 2,
          keep_elitism=0,
          K_tournament=3,
          random_mutation_max_val=32.768,
          random_mutation_min_val=-32.768,
          logger=logger,
          on_generation=on_generation,
          parallel_processing=['thread', 4])

ga_instance.run()

best = ga_instance.best_solution()
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=1./solution_fitness))


# sztuczka: odwracamy my narysował nam się oczekiwany wykres dla problemu minimalizacji
ga_instance.best_solutions_fitness = [1. / x for x in ga_instance.best_solutions_fitness]
ga_instance.plot_fitness()

