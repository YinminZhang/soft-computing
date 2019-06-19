# -*- coding: utf-8 -*
import random
import numpy as np
import matplotlib.pyplot as plt


A1 = 2 # acceleration speed
A2 = 2 # acceleration speed
TOTAL_GENERATIONS = 100
INDIVIDUAL_NUM = 100
MAX_OR_MIN = "MAX"

class Individual:
    def __init__(self):
        self.x = [random.randint(0, 15), random.randint(0, 15), random.randint(0, 15)]
        self.v = [0] * 3
        self.y = self._y(self.x[0], self.x[1], self.x[2])
        self.max_y = self.y
        self.individual_best = self.x

    @staticmethod
    def _y(x1, x2, x3):
        if MAX_OR_MIN == "MAX":
            return 2 * x1 * x1 - 3 * x2 * x2 - 4 * x1 + 5 * x2 + x3
        elif MAX_OR_MIN == "MIN":
            return -(2 * x1 * x1 - 3 * x2 * x2 - 4 * x1 + 5 * x2 + x3)

    def move(self):
        for i in range(3):
            self.x[i] += int(self.v[i])
            if self.x[i] > 15:
                self.x[i] = 15
            if self.x[i] < 0:
                self.x[i] = 0
        self.calc_y()

    def calc_y(self):
        self.y = self._y(self.x[0], self.x[1], self.x[2])


individuals = [Individual() for i in range(100)]

max_all = []
max_y = individuals[0].y
global_best_x = individuals[0].x
for n in range(TOTAL_GENERATIONS):
    for i, individual in enumerate(individuals):
        if individuals[i].y > max_y:
            max_y = individuals[i].y
            global_best_x = individuals[i].x
    a = 1
    for num in range(100):
        for i in range(3):
            individuals[num].v[i] += random.random() * (global_best_x[i] - individuals[num].x[i]) * A1 + random.random() * (individuals[num].individual_best[i] - individuals[num].x[i]) * A2
            individuals[num].move()
            if individuals[num].y > individuals[num].max_y:
                individuals[num].max_y = individuals[num].y
                individuals[num].individual_best = individuals[num].x
    a = 1

    max_all.append(max(individuals, key=lambda i: i.y).y)

max = 0
for num in range(0, len(max_all)):
    if max_all[num] > max:
        max = max_all[num]
if MAX_OR_MIN == "MAX":
    print('max: ', max)
elif MAX_OR_MIN == "MIN":
    max_all = list(map(lambda x: -x, max_all))
    print('min: ', -max)
x = np.linspace(0, TOTAL_GENERATIONS, len(max_all))

print(max_all)
plt.plot(x, max_all)
plt.show()

