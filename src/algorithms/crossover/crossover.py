import numpy as np
import random
from src.population.specimen import Specimen

# Wyjebanie klasy
# Zmiana argumentów wywołania (PyGAD ma swoje)
# Zwraca jednego potomka 
# Zwraca go jako tablicę wartości (tablica z tablicami genów)



def discrete_crossover(parents, offspring_size):
    offspring = []
    idx = 0

    while len(offspring) != offspring_size[0]:
        parent1 = parents[idx % parents.shape[0], :].copy()
        parent2 = parents[(idx + 1) % parents.shape[0], :].copy()

        child1 = parent1
        child2 = parent2

    
        for i in range(parent1.shape[1]):
            if random.uniform(0, 1) < 0.5:
                child1[i] = parent1[i]
            else:
                child1[i] = parent2[i]


            if random.uniform(0, 1) < 0.5:
                child2[i] = parent2[i]
            else:
                child2[i] = parent1[i]
        
        offspring.append(child1)
        offspring.append(child2)

        idx += 1
    
    return np.array(offspring)


    

def elite_crossover(self, specimen1, specimen2):
    if random.random() < self.crossover_prob:
        self.single_point_crossover(specimen1, specimen2)
        child1, child2 = self.children[0], self.children[1]
        ratings = [specimen.fitness for specimen in [specimen1, specimen2, child1, child2]]
        elite_index = np.argsort(ratings)[-2:]
        new_population = [specimen1, specimen2, child1, child2][elite_index[0]], [specimen1, specimen2, child1, child2][elite_index[1]]
        self.children = []
        self.children.append(new_population[0])
        self.children.append(new_population[1])
    else:
        self.children.append(specimen1)
        self.children.append(specimen2)

def self_crossover(self, specimen1, specimen2):
    if random.random() >= self.crossover_prob:
        self.children.append(specimen1)
        self.children.append(specimen2)
    else:
        child1_chromosomes = []
        child2_chromosomes = []

        for i in range(len(specimen1.specimen)):
            chromosome = specimen1.specimen[i].chromosome
            child1 = np.zeros_like(chromosome)
            ones_counter = sum(chromosome)
            ones_index = random.sample(range(len(chromosome)), ones_counter)
            for index in ones_index:
                child1[index] = 1
            child1_chromosomes.append(child1)

        for i in range(len(specimen2.specimen)):
            chromosome = specimen2.specimen[i].chromosome
            child2 = np.zeros_like(chromosome)
            ones_counter = sum(chromosome)
            ones_index = random.sample(range(len(chromosome)), ones_counter)
            for index in ones_index:
                child2[index] = 1
            child2_chromosomes.append(child2)

        child1 = Specimen.from_chromosomes(child1_chromosomes, specimen1.boundaries, specimen1.accuracy,
                                            specimen1.fitness_function)
        child2 = Specimen.from_chromosomes(child2_chromosomes, specimen2.boundaries, specimen2.accuracy,
                                            specimen2.fitness_function)

        self.children.append(child1)
        self.children.append(child2)

def binary_crossover(self, specimen1, specimen2):
    if random.random() >= self.crossover_prob:
        self.children.append(specimen1)
        self.children.append(specimen2)
    else:
        child1_chromosomes = []
        child2_chromosomes = []

        for i in range(len(specimen1.specimen)):
            chromosome_1 = specimen1.specimen[i].chromosome
            chromosome_2 = specimen2.specimen[i].chromosome

            left, right = 0, len(chromosome_1) - 1

            while left < right - 2:
                center = (left + right) // 2

                TP_1 = np.concatenate((chromosome_1[:center], chromosome_2[center:]))
                TP_2 = np.concatenate((chromosome_2[:center], chromosome_1[center:]))

                NTP_1 = np.sum(TP_1)
                NTP_2 = np.sum(TP_2)

                if NTP_1 > NTP_2:
                    left = center
                else:
                    right = center

            child_1 = np.concatenate((chromosome_1[:right], chromosome_2[right:]))
            child_2 = np.concatenate((chromosome_2[:right], chromosome_1[right:]))

            child1_chromosomes.append(child_1)
            child2_chromosomes.append(child_2)

        child1 = Specimen.from_chromosomes(child1_chromosomes, specimen1.boundaries, specimen1.accuracy,
                                            specimen1.fitness_function)
        child2 = Specimen.from_chromosomes(child2_chromosomes, specimen2.boundaries, specimen2.accuracy,
                                            specimen2.fitness_function)

        self.children.append(child1)
        self.children.append(child2)

def linkage_evolution_crossover(self, specimen1, specimen2):
    if random.random() >= self.crossover_prob:
        self.children.append(specimen1)
        self.children.append(specimen2)
    else:
        child1_chromosomes = []
        child2_chromosomes = []

        for i in range(len(specimen1.specimen)):
            chromosome_1 = specimen1.specimen[i].chromosome
            chromosome_2 = specimen2.specimen[i].chromosome

            child1_segment_list = []
            child2_segment_list = []

            segments = random.randint(1, min(3, len(chromosome_1)))
            split_points = sorted(random.sample(range(1, len(chromosome_1)), segments - 1))
            split_points = [0] + split_points + [len(chromosome_1)]

            for j in range(len(split_points) - 1):
                segment_start = split_points[j]
                segment_end = split_points[j + 1]

                if j % 2 == 0:
                    child1_segment_list.append(chromosome_1[segment_start:segment_end])
                    child2_segment_list.append(chromosome_2[segment_start:segment_end])
                else:
                    child1_segment_list.append(chromosome_2[segment_start:segment_end])
                    child2_segment_list.append(chromosome_1[segment_start:segment_end])

            child1_chromosome = np.concatenate(child1_segment_list)
            child2_chromosome = np.concatenate(child2_segment_list)

            child1_chromosomes.append(child1_chromosome)
            child2_chromosomes.append(child2_chromosome)

        child1 = Specimen.from_chromosomes(child1_chromosomes, specimen1.boundaries, specimen1.accuracy,
                                            specimen1.fitness_function)
        child2 = Specimen.from_chromosomes(child2_chromosomes, specimen2.boundaries, specimen2.accuracy,
                                            specimen2.fitness_function)

        self.children.append(child1)
        self.children.append(child2)


