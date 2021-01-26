import bisect
import itertools
import json
import warnings

import numpy as np
import scipy.optimize as spo


class Compare:
    """
    This class computes the priority vector and consistency ratio of a positive reciprocal matrix, created using a
    dictionary of pairwise comparison values. Optimal values are computed for any missing pairwise comparisons.
    The 'name' property is used to link the Compare object to its parent Compose object.
    The 'weights' property contains the priority vector as a dictionary whose keys are the criteria and
        whose values are the criteria's weights.
    The 'consistency_ratio' property contains the computed consistency ratio of the priority vector as a float.
    :param name: string, the name of the Compare object; if the object has a parent, this name MUST be included
        as a criterion of its parent
    :param comparisons: dictionary, a dictionary in one of two forms: (i) each key is a tuple of two criteria and
        each value is their pairwise comparison value, or (ii) each key is a criteria as a string and each value
        is that criteria's measured value
    :param precision: integer, number of decimal places of precision to compute both the priority
        vector and the consistency ratio; default is 4
    :param random_index: string, the random index estimates used to compute the consistency ratio
        (see the compute_consistency_ratio function for more information regarding the different estimates);
        valid input: 'dd', 'saaty'; default is 'dd'
    :param iterations: integer, number of iterations before the compute_eigenvector function stops; default is 100
    :param tolerance: float, the stopping criteria for the cycling coordinates algorithm; the algorithm stops when the
        difference between the norms of two cycles of coordinates is less than this value; default is 0.0001
    :param cr: boolean, override to enable computing priority vectors without a consistency ratio
    """

    def __init__(self, name=None, comparisons=None,
                 precision=4, random_index='dd', iterations=100, tolerance=0.0001, cr=True):
        self.name = name
        self.comparisons = comparisons
        self.precision = precision
        self.random_index = random_index
        self.iterations = iterations
        self.tolerance = tolerance
        self.cr = cr

        self.normalize = not isinstance(next(iter(self.comparisons)), tuple)
        self.criteria = []
        self.pairs = []
        self.size = None
        self.matrix = None
        self.missing_comparisons = None
        self.consistency_ratio = None
        self.weights = None

        self.check_input()
        if self.normalize:
            self.build_normalized_criteria()
            self.build_normalized_matrix()
        else:
            self.build_criteria()
            self.insert_comparisons()
            self.build_matrix()
            self.get_missing_comparisons()
            if self.missing_comparisons:
                self.complete_matrix()

        self.compute()

    def check_input(self):
        """
        Raises a ValueError if an input value is not greater than zero;
        raises a TypeError if an input cannot be cast to a float.
        """
        for key, value in self.comparisons.items():
            try:
                if not float(value) > 0:
                    msg = f'{key}: {value} is an invalid input. All input values must be greater than zero.'
                    raise ValueError(msg)
            except TypeError:
                msg = f'{key}: {value} is an invalid input. All input values must be numeric.'
                raise TypeError(msg)

    def check_size(self):
        """
        Raises a ValueError if a consistency ratio is requested and
        the chosen random index does not support the size of the matrix.
        """
        if not self.normalize and self.cr and ((self.random_index == 'saaty' and self.size > 15) or self.size > 100):
            msg = "The input matrix is too large and a consistency ratio cannot be computed.\n" \
                  "\tThe maximum matrix size supported by the 'saaty' random index is 15 x 15;\n" \
                  "\tthe maximum matrix size supported by the 'dd' random index is 100 x 100.\n" \
                  "\tTo compute the priority vector without a consistency ratio, use the 'cr=False' argument."
            raise ValueError(msg)

    def build_criteria(self):
        """
        Creates an empty 'pairs' dictionary that contains all possible permutations
        of those criteria found within the keys of the input 'comparisons' dictionary,
        then makes sure the size of the resulting matrix will be supported by the chosen random index.
        """
        for key in self.comparisons:
            for criterion in key:
                if criterion not in self.criteria:
                    self.criteria.append(criterion)
        self.pairs = dict.fromkeys(itertools.permutations(self.criteria, 2))
        self.size = len(self.criteria)
        self.check_size()

    def build_normalized_criteria(self):
        """
        Creates a list of those criteria found within the keys of the input 'comparisons' dictionary,
        then makes sure the size of the resulting matrix will be supported by the chosen random index.
        """
        self.criteria = list(self.comparisons)
        self.size = len(self.criteria)
        self.check_size()

    def insert_comparisons(self):
        """
        Fills the entries of the 'pairs' dictionary with the corresponding comparison values
        of the input 'comparisons' dictionary or their computed reciprocals.
        """
        for key, value in self.comparisons.items():
            inverse_key = key[::-1]
            self.pairs[key] = value
            self.pairs[inverse_key] = np.reciprocal(float(value))

    def build_matrix(self):
        """
        Creates a correctly-sized numpy matrix of 1s, then fills the matrix with values from the 'pairs' dictionary.
        """
        self.matrix = np.ones((self.size, self.size))
        for pair, value in self.pairs.items():
            location = tuple(self.criteria.index(criterion) for criterion in pair)
            self.matrix.itemset(location, value)

    def build_normalized_matrix(self):
        """
        Creates a numpy matrix of values from the input 'comparisons' dictionary.
        """
        self.matrix = np.array(tuple(value for value in self.comparisons.values()), float)

    def get_missing_comparisons(self):
        """
        Creates the 'missing comparisons' dictionary by populating its keys with the unique comparisons
        missing from the input 'comparisons' dictionary and populating its values with 1s.
        """
        missing_comparisons = [key for key, value in self.pairs.items() if not value]
        for criteria in missing_comparisons:
            del missing_comparisons[missing_comparisons.index(criteria[::-1])]
        self.missing_comparisons = dict.fromkeys(missing_comparisons, 1)

    def complete_matrix(self):
        """
        Optimally completes an incomplete pairwise comparison matrix according to the algorithm described in
        Bozóki, S., Fülöp, J. and Rónyai, L., 'On optimal completion of incomplete pairwise comparison matrices,'
        Mathematical and Computer Modelling, 52:1–2, 2010, pp. 318-333. https://doi.org/10.1016/j.mcm.2010.02.047
        """
        last_iteration = np.array(tuple(self.missing_comparisons.values()))
        difference = np.inf
        while difference > self.tolerance:
            self.minimize_coordinate_values()
            current_iteration = np.array(tuple(self.missing_comparisons.values()))
            difference = np.linalg.norm(last_iteration - current_iteration)
            last_iteration = current_iteration

    def minimize_coordinate_values(self):
        """
        Computes the minimum value for each missing value from the 'missing_comparisons' dictionary
        using the cyclic coordinates method described in Bozóki et al.
        """

        def lambda_max(x, x_location):
            """
            The function to be minimized. Finds the largest eigenvalue of a matrix.
            :param x: float, the variable to be minimized
            :param x_location: tuple, the matrix location of the variable to be minimized
            """
            inverse_x_location = x_location[::-1]
            self.matrix.itemset(x_location, x)
            self.matrix.itemset(inverse_x_location, np.reciprocal(float(x)))
            return np.max(np.linalg.eigvals(self.matrix))

        # The upper bound of the solution space is 10 times the largest value of the matrix.
        upper_bound = np.nanmax(self.matrix) * 10

        for comparison in self.missing_comparisons:
            comparison_location = tuple(self.criteria.index(criterion) for criterion in comparison)
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', category=np.ComplexWarning)
                self.set_matrix(comparison)
                optimal_solution = spo.minimize_scalar(lambda_max, args=(comparison_location,),
                                                       method='bounded', bounds=(0, upper_bound))
            self.missing_comparisons[comparison] = np.real(optimal_solution.x)

    def set_matrix(self, comparison):
        """
        Sets the value of every missing comparison in the comparison matrix (other than the current comparison)
        to its current value in the 'missing_comparisons' dictionary or its reciprocal.
        :param comparison: tuple, a key from the 'missing_comparisons' dictionary
        """
        for key, value in self.missing_comparisons.items():
            if key != comparison:
                location = tuple(self.criteria.index(criterion) for criterion in key)
                inverse_location = location[::-1]
                self.matrix.itemset(location, value)
                self.matrix.itemset(inverse_location, np.reciprocal(float(value)))

    def compute(self):
        """
        Runs all functions necessary for building the weights and consistency ratio of the Compare object.
        """
        if not self.normalize:
            priority_vector = self.compute_priority_vector(self.matrix, self.iterations)
            if self.cr:
                self.compute_consistency_ratio()
        else:
            priority_vector = np.divide(self.matrix, np.sum(self.matrix, keepdims=True)).round(self.precision)
            self.consistency_ratio = 0.0
        weights = dict(zip(self.criteria, priority_vector))
        sorted_weights = dict(sorted(weights.items(), key=lambda item: item[1], reverse=True))
        self.weights = {self.name: sorted_weights}

    def compute_priority_vector(self, matrix, iterations, comp_eigenvector=None):
        """
        Returns the priority vector of the Compare object.
        :param matrix: numpy matrix, the matrix from which to derive the priority vector
        :param iterations: integer, number of iterations to run before the function stops
        :param comp_eigenvector: numpy array, a comparison eigenvector used during recursion
        """
        # Compute the principal eigenvector by normalizing the rows of a newly squared matrix
        sq_matrix = np.linalg.matrix_power(matrix, 2)
        row_sum = np.sum(sq_matrix, axis=1)
        total_sum = np.sum(sq_matrix)
        principal_eigenvector = np.divide(row_sum, total_sum)

        # Create a zero matrix as the comparison eigenvector if this is the first iteration
        if comp_eigenvector is None:
            comp_eigenvector = np.zeros(self.size)

        # Compute the difference between the principal and comparison eigenvectors
        remainder = np.subtract(principal_eigenvector, comp_eigenvector).round(self.precision)

        # If the difference between the two eigenvectors is zero (after rounding to the specified precision),
        # set the current principal eigenvector as the priority vector for the matrix...
        if not np.any(remainder):
            return principal_eigenvector.round(self.precision)

        # ...else recursively run the function until either there is no difference between
        # the principal and comparison eigenvectors, or until the predefined number of iterations has been met,
        # in which case set the last principal eigenvector as the priority vector
        iterations -= 1
        if iterations > 0:
            return self.compute_priority_vector(sq_matrix, iterations, principal_eigenvector)
        else:
            return principal_eigenvector.round(self.precision)

    def compute_consistency_ratio(self):
        """
        Sets the 'consistency_ratio' property of the Compare object, using random index estimates from
        Donegan and Dodd's 'A note on Saaty's Random Indexes' in Mathematical and Computer Modelling,
        15:10, 1991, 135-137 (doi: 10.1016/0895-7177(91)90098-R) by default (random_index='dd').
        If the random index of the object equals 'saaty', uses the estimates from
        Saaty's Theory And Applications Of The Analytic Network Process, Pittsburgh: RWS Publications, 2005, pg. 31.
        """
        # A valid, square, reciprocal matrix with only one or two rows must be consistent
        if self.size < 3:
            self.consistency_ratio = 0.0
            return

        if self.random_index == 'saaty':
            ri_dict = {3: 0.52, 4: 0.89, 5: 1.11, 6: 1.25, 7: 1.35, 8: 1.40, 9: 1.45,
                       10: 1.49, 11: 1.52, 12: 1.54, 13: 1.56, 14: 1.58, 15: 1.59}
        else:  # self.random_index == 'dd'
            ri_dict = {3: 0.4914, 4: 0.8286, 5: 1.0591, 6: 1.1797, 7: 1.2519,
                       8: 1.3171, 9: 1.3733, 10: 1.4055, 11: 1.4213, 12: 1.4497,
                       13: 1.4643, 14: 1.4822, 15: 1.4969, 16: 1.5078, 17: 1.5153,
                       18: 1.5262, 19: 1.5313, 20: 1.5371, 25: 1.5619, 30: 1.5772,
                       40: 1.5976, 50: 1.6102, 60: 1.6178, 70: 1.6237, 80: 1.6277,
                       90: 1.6213, 100: 1.6339}
        try:
            random_index = ri_dict[self.size]
        # If the size of the comparison matrix falls between two computed estimates, compute a weighted estimate
        except KeyError:
            s = tuple(ri_dict.keys())
            smaller = s[bisect.bisect_left(s, self.size) - 1]
            larger = s[bisect.bisect_right(s, self.size)]
            estimate = (ri_dict[larger] - ri_dict[smaller]) / (larger - smaller)
            random_index = estimate * (self.size - smaller) + ri_dict[smaller]

        lambda_max = np.max(np.linalg.eigvals(self.matrix))  # Find the Perron-Frobenius eigenvalue of the matrix
        consistency_index = (lambda_max - self.size) / (self.size - 1)
        self.consistency_ratio = np.real(consistency_index / random_index).round(self.precision)

    def report(self, silent=False):
        """
        Returns the key information of the Compare object as a JSON object, optionally printing it to the console.
        :param silent: boolean, if True, does not print the report to the console; default is False
        """

        def convert_to_json_format(input_dict):
            """
            Returns a dictionary as a list of JSON compatible objects.
            :param input_dict: dictionary, the dictionary to be converted
            """
            if self.normalize:
                return list({key: value} for key, value in input_dict.items())
            else:
                return list({', '.join(key): value} for key, value in input_dict.items())

        report = json.dumps({'Name': self.name,
                             'Weights': self.weights[self.name],
                             'Consistency Ratio': self.consistency_ratio,
                             'Random Index': 'Donegan & Dodd' if self.random_index == 'dd' else 'Saaty',
                             'Criteria': {
                                 'Count': len(self.criteria),
                                 'Names': self.criteria,
                             },
                             'Comparisons': {
                                 'Input': convert_to_json_format(self.comparisons),
                                 'Computed': convert_to_json_format(self.missing_comparisons)
                                 if self.missing_comparisons else None}
                             }, indent=4)
        if not silent:
            print(report)
        return report


class Compose:
    # TODO Create a doc string for this
    # TODO Create report function
    def __init__(self, name=None, parent=None, children=None):
        self.name = name
        self.parent = parent
        self.children = children

        self.precision = None
        self.weights = dict()

        self.compute_precision()
        self.compute_total_priority()
        self.normalize_total_priority()

    def compute_precision(self):
        """
        Updates the 'precision' property of the Compose object
        by selecting the lowest precision of all the input matrices.
        """
        precision = np.min([child.precision for child in self.children])
        if precision < self.parent.precision:
            self.precision = precision
        else:
            self.precision = self.parent.precision

    def compute_total_priority(self):
        """
        Computes the total priorities of the Compose object's parent criteria
        given the priority vectors of its children.
        """
        for parent_key, parent_value in self.parent.weights[self.parent.name].items():
            for child in self.children:

                if parent_key in child.weights:
                    for child_key, child_value in child.weights[parent_key].items():
                        value = parent_value * child_value
                        try:
                            self.weights[child_key] += value
                        except KeyError:
                            self.weights[child_key] = value
                    break

    def normalize_total_priority(self):
        """
        Updates the 'weights' property of the Compose object with normalized values at the object's level of precision.
        """
        total_sum = sum(self.weights.values())
        comp_dict = {key: np.divide(value, total_sum).round(self.precision) for key, value in self.weights.items()}
        self.weights = {self.name: comp_dict}

    def report(self, silent=False):
        """
        Returns the key information of the Compose object as a JSON object, optionally printing it to the console.
        :param silent: boolean, if True, does not print the report to the console; default is False
        """
        report = json.dumps({'Name': self.name,
                             'Parent': self.parent.name,
                             'Children': [child.name for child in self.children]
                             }, indent=4)
        if not silent:
            print(report)
        return report


if __name__ == '__main__':
    pass
