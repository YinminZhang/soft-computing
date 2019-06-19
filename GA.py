# -*- coding: utf-8 -*
import copy
import random
import numpy as np
import matplotlib.pyplot as plt


P_RECOMBINATION = 0.8
P_VARIATION = 0.005
TOTAL_GENERATIONS = 100
INDIVIDUAL_NUM = 100
MAX_OR_MIN = "MIN"

class Individual:
    def __init__(self):
        self.x1 = random.randint(0, 15)
        self.x2 = random.randint(0, 15)
        self.x3 = random.randint(0, 15)
        self.genotype = self.phenotype_to_genotype(self.x1, self.x2, self.x3)
        self.y = self._y(self.x1, self.x2, self.x3)

    @staticmethod
    def _y(x1, x2, x3):
        if MAX_OR_MIN == "MAX":
            return 2 * x1 * x1 - 3 * x2 * x2 - 4 * x1 + 5 * x2 + x3
        elif MAX_OR_MIN == "MIN":
            return -(2 * x1 * x1 - 3 * x2 * x2 - 4 * x1 + 5 * x2 + x3)

    def calc_y(self):
        self.y = self._y(self.x1, self.x2, self.x3)

    @staticmethod
    def phenotype_to_genotype(*args):
        x = [*args]
        return "".join(map(lambda _x: bin(_x).replace('0b', '').zfill(4), x))

    @staticmethod
    def genotype_to_phenotype(s):
        return int(s[0:4], 2), int(s[4:8], 2), int(s[8:12], 2)


individuals = [Individual() for i in range(100)]

max_all = []
for n in range(TOTAL_GENERATIONS):
    # Recombination
    for num in range(INDIVIDUAL_NUM):
        individuals[num].genotype = Individual.phenotype_to_genotype(individuals[num].x1, individuals[num].x2, individuals[num].x3)
    p = random.random()
    if p < P_RECOMBINATION:
        random.shuffle(individuals)
        for num in range(0, 50):
            start_locus = random.randint(0, 12)
            s1 = list(individuals[num].genotype)
            s2 = list(individuals[num + 50].genotype)
            for locus in range(start_locus, 12):
                tmp = s1[locus]
                s1[locus] = s2[locus]
                s2[locus] = tmp
            individuals[num].genotype = "".join(s1)
            individuals[num + 50].genotype = "".join(s2)
    # print(genotype)

    # Variation
    for num in range(INDIVIDUAL_NUM):
        # print(genotype)
        s = list(individuals[num].genotype)
        p = random.random()
        if p < P_VARIATION:
            locus = random.randint(0, 11)
            if s[locus] == '0':
                s[locus] = '1'
            else:
                s[locus] = '0'
            individuals[num].genotype = ''.join(s)

    # update genotype x1, x2, x3
    for num in range(INDIVIDUAL_NUM):
        individuals[num].x1, individuals[num].x2, individuals[num].x3 = Individual.genotype_to_phenotype(individuals[num].genotype)
        individuals[num].calc_y()

    # Selection
    min_y = min(individuals, key=lambda i: i.y).y
    list_fitness = []
    sum_y_diff = 0
    y_diff = [0] * TOTAL_GENERATIONS
    for num in range(INDIVIDUAL_NUM):
        y_diff[num] -= min_y
        sum_y_diff += y_diff[num]

    # print([individuals[num].y_diff for num in range(INDIVIDUAL_NUM)])
    if sum_y_diff == 0:
        continue
    for num in range(INDIVIDUAL_NUM):
        list_fitness.append(1.0 * y_diff[num] / sum_y_diff)
        list_fitness[num] += list_fitness[num - 1]
    # print(list_fitness)

    individuals_new = []

    for num in range(INDIVIDUAL_NUM):
        p = random.random()
        for i in range(INDIVIDUAL_NUM):
            if list_fitness[i] >= p:
                individuals_new.append(copy.deepcopy(individuals[i]))
                break
    individuals = individuals_new

    max_all.append(max(individuals, key=lambda i: i.y).y)

max = 0
for num in range(0, len(max_all)):
    if max_all[num] > max:
        max = max_all[num]
if MAX_OR_MIN == "MAX":
    print('max: ', max)
elif MAX_OR_MIN == "MIN":
    max_all = list(map(lambda x: -x, max_all))
    print('max: ', -max)
x = np.linspace(0, TOTAL_GENERATIONS, len(max_all))
print(max_all)
plt.plot(x, max_all)
plt.show()
