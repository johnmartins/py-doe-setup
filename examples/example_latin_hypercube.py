from matrix import run_experiments
from methods import ExperimentType
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np

np.random.seed(1)


x = []
y = []


def experiment(params, number):
    x.append(params[0])
    y.append(params[1])


a = [0, 10]
b = a

parameters = [a, b]

run_experiments(experiment, parameters, method=ExperimentType.LATIN_HYPERCUBE, stratifications=a[1])

fig, ax = plt.subplots()
intervals = 1

loc = plticker.MultipleLocator(base=intervals)
ax.xaxis.set_major_locator(loc)
ax.yaxis.set_major_locator(loc)

ax.grid(which='major', axis='both', linestyle='-')

plt.scatter(x, y)
plt.xlabel("x")
plt.ylabel("y")
plt.xlim(a)
plt.ylim(b)
plt.show()
