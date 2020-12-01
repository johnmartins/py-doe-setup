from matrix import run_experiments
from methods import ExperimentType
import matplotlib.pyplot as plt


x = []
y = []


def experiment(params, number):
    x.append(params[0])
    y.append(params[1])


a = [0, 100]
b = [0, 100]

parameters = [a, b]

run_experiments(experiment, parameters, method=ExperimentType.LATIN_HYPERCUBE, stratifications=100)

plt.scatter(x, y)
plt.xlabel("x")
plt.ylabel("y")
plt.show()
