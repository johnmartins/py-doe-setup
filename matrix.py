from copy import copy
import numpy.random as np_random

from methods import ExperimentType


def create_factorial_matrix(parameters):
    """
    Creates a DOE matrix with all possible combinations of the parameters used with this method.

    High time complexity O(k^j) where k is the amount of parameters, and j is the amount of levels for each parameter.
    Careful with large amounts of parameters. This is not optimized for large experiments. In fact, it is not optimized
    at all.

    :param parameters: Whatever parameters you wish to vary in your experiment
    :return: DOE Parameter matrix with all combinations. Combinations are sorted by row (one row = one combination).
    """
    # calculate dimension
    num_runs = 1

    for parameter in parameters:
        num_runs *= len(parameter)

    parameter_matrix = []
    parameter_matrix_converted = []

    zeros_array = [0] * len(parameters)
    parameter_matrix.append(zeros_array)

    for i in range(1, num_runs + 1):
        params = copy(parameter_matrix[i - 1])  # Copy last set of parameters

        # Convert and insert the values from the LAST iteration into a new matrix.
        actual_values = []
        for j in range(0, len(params)):
            actual_values.append(parameters[j][params[j]])
        parameter_matrix_converted.append(actual_values)

        index = 0
        while params[index] == len(parameters[index]) - 1:
            params[index] = 0
            index += 1

            if index >= len(params):
                break

        if index == len(params):
            break

        params[index] += 1
        parameter_matrix.append(params)

    return parameter_matrix_converted


def create_latin_hypercube(parameters, stratifications=10, samples=5):
    dims = len(parameters)
    parameter_matrix = []

    dim_strats = []

    for parameter in parameters:
        if len(parameter) != 2:
            raise TypeError('Parameters needs to come in pairs of 2 when using the latin hypercube method')

        lim_upper = parameter[1]
        lim_lower = parameter[0]
        if parameter[0] > parameter[1]:
            lim_upper = parameter[0]
            lim_lower = parameter[1]

        dim_range = lim_upper - lim_lower
        strat_range = dim_range/stratifications

        strats = []
        for i in range (0, stratifications):
            strats.append([lim_lower + strat_range * i, lim_lower + strat_range * (i + 1)])

        # At this point we have the array "strats", which contains the upper limit of each stratification.
        # The first one being equal to lim_lower + strat_range, and the last one being equal to lim_upper.
        # Thus, we can check if a value is greater than an element in the strats array to determine in which
        # stratification that value belongs. Slow, but functional.
        dim_strats.append(strats)

        sample_array = []
        while len(strats) != 0 and len(sample_array) != samples:
            print("sample array len: " + str(len(sample_array)) + ". Max samples: "+str(samples))
            mean = (lim_upper + lim_lower) / 2
            std = (mean - lim_lower) / 2
            random_number = np_random.normal(mean, std, 1)

            for i in range(0, len(strats)):
                value = random_number[0]
                if strats[i][0] < value < strats[i][1]:
                    sample_array.append(value)
                    strats.pop(i)   # Remove dat strat to prevent it from being used again
                    break

        print(sample_array)

        # Now we have all the values. Randomly put them together (or just put them together as they are already random)

    return parameter_matrix


def run_experiments(experiment_method, parameters, experiment_name='Unnamed experiment', print_to_stdout=False,
                    method=ExperimentType.FACTORIAL, stratifications=10, samples=5):
    """
    Automatically sets up a DOE, and runs the experiment_method function. The experiment_method function needs to
    have one argument that is an array which contains the specific experiment parameters. If the method returns a value
    then it will be stored in an array which is returned by this method. The index of that results array corresponds to
    the experiment number.

    :param experiment_method: The method which is to be run each experiment
    :param parameters: An array of parameters which that experiment uses
    :param experiment_name: Whatever you want to call the experiment (optional)
    :param print_to_stdout: If set to True it may be easier to monitor the progress
    :param method: instance of method.ExperimentType
    :param stratifications: Is only used for Latin Hypercubes. Amount of stratifications per dimension.
    :param samples: If only used for Latin Hypercubes. Amount of samples. Cant be more than the amount of stratifications
    :return: Array of results
    """
    if isinstance(method, ExperimentType) is False:
        raise TypeError('Invalid method. Needs to be of ExperimentType')

    if print_to_stdout:
        print("New experiment: " + experiment_name)

    if method == ExperimentType.FACTORIAL:
        parameter_matrix = create_factorial_matrix(parameters)
    elif method == ExperimentType.LATIN_HYPERCUBE:
        parameter_matrix = create_latin_hypercube(parameters, stratifications=stratifications, samples=samples)
        print('Latin hypercube! Very cool!')
        return
    else:
        raise Exception('This should not be possible (TM)')
    results_array = []

    i = 0
    for parameter_set in parameter_matrix:
        if print_to_stdout:
            new_exp_str = "EXPERIMENT {}/{}".format(i + 1, len(parameter_matrix))
            print(new_exp_str)

        result = experiment_method(parameter_set, i+1)

        results_array.append(result)

        i += 1

    if print_to_stdout:
        print("Experiment concluded successfully")

    return results_array


'''
# Use-case example:

def exp_met(params):
    return params[0] + params[1] + params[2] 
    
a = [1, 2]
b = [3, 4]
c = [5, 6]

res = run_experiments(exp_met, [a, b, c], experiment_name="My experiment", print_to_stdout=True)
print(res)
'''
