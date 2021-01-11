import bisect
import itertools
import warnings

import numpy as np
import scipy.optimize as sp


class Compare:
    # TODO redo this
    """
    This class computes the priority vector and consistency ratio of a positive
    reciprocal matrix. The 'weights' property contains the priority vector as a dictionary
    whose keys are criteria and whose values are the criteria's weights.
    The 'consistency_ratio' property contains the computed consistency ratio of the input matrix as a float.
    :param name: string, the name of the Compare object; if the object has a parent,
        this name MUST be included as a criterion of its parent
    :param comparisons:
    :param order: list of strings, the criteria of the matrix, listed in the order desired
    :param precision: integer, number of decimal places of precision to compute both the priority
        vector and the consistency ratio; default is 4
    :param iterations: integer, number of iterations before the compute_eigenvector function stops;
        default is 100
    :param random_index: string, the random index estimates used to compute the consistency ratio;
        valid input: 'dd', 'saaty'; default is 'dd'; see the compute_consistency_ratio function for more
        information regarding the different estimates
    """

    def __init__(self, name=None, comparisons=None, order=None,
                 precision=4, iterations=100, random_index='dd', tolerance=0.0001, cr=True):
        self.name = name
        self.comparisons = comparisons
        self.order = order
        self.precision = precision
        self.iterations = iterations
        self.random_index = random_index
        self.tolerance = tolerance
        self.cr = cr

        self.normalize = not isinstance(next(iter(self.comparisons)), tuple)
        self.criteria = []
        self.pairs = []
        self.size = None
        self.matrix = None
        self.missing_comparisons = None
        self.priority_vector = None
        self.consistency_ratio = None
        self.weights = None

        if self.normalize:
            self.build_normalized_criteria()
            self.build_normalized_matrix()
            self.normalize_matrix()
        else:
            self.build_criteria()
            self.insert_comparisons()
            self.build_matrix()
            self.get_missing_comparisons()
            if self.missing_comparisons:
                self.complete_matrix()

        self.compute()

        # print(self.name)
        # print(self.comparisons)# = comparisons
        # print(self.order)# = order
        # print(self.precision)# = precision
        # print(self.iterations)# = iterations
        # print(self.random_index)# = random_index.lower()
        # print(self.tolerance)# = tolerance
        # print(self.norm)# = not isinstance(tuple(self.comparisons)[0], tuple)
        # print(self.criteria)# = []
        # print(self.pairs)# = []
        # print(self.size)# = None
        # print(self.matrix)# = None
        # print(self.missing_comparisons)# = None
        # print(self.priority_vector)# = None
        # print(self.consistency_ratio)# = None
        # print(self.weights)# = None

        # TODO build report functionality that uses the order property

    def check_size(self):
        """
        Raises a Value Error if a consistency ratio is requested and the chosen random index
        will not support the size of the resulting matrix.
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
        Creates a correctly-sized numpy matrix of ones,
        then fills the matrix with values from the 'pairs' dictionary.
        """
        self.matrix = np.ones((self.size, self.size))
        for pair, value in self.pairs.items():
            location = tuple(self.criteria.index(criterion) for criterion in pair)
            self.matrix.itemset(location, value)

    def build_normalized_matrix(self):
        """
        Creates a correctly-sized numpy matrix of values from the input 'comparisons' dictionary.
        """
        self.matrix = np.array(tuple(value for value in self.comparisons.values()), float)

    def get_missing_comparisons(self):
        """
        Creates the 'missing comparisons' dictionary by populating its keys with the unique comparisons
        that are missing from the input 'comparisons' dictionary and populating its values with 1s.
        """
        missing_comparisons = [key for key, value in self.pairs.items() if not value]
        for criteria in missing_comparisons:
            del missing_comparisons[missing_comparisons.index(criteria[::-1])]
        self.missing_comparisons = dict.fromkeys(missing_comparisons, 1)

    def complete_matrix(self):
        """
        Optimally completes an incomplete pairwise comparison matrix according to the algorithm described in
        Bozóki, S., Fülöp, J. and Rónyai, L., 'On optimal completion of incomplete pairwise comparison matrices,'
        Mathematical and Computer Modelling, 52:1–2, 2010, pp. 318-333.
        https://doi.org/10.1016/j.mcm.2010.02.047
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
        using the cyclic coordinates method as described in the paper by Bozóki et al.
        """
        def lambda_max(x, x_location):
            """
            The function to be minimized. Finds the largest eigenvalue of a matrix given a missing value.
            """
            inverse_x_location = x_location[::-1]
            self.matrix.itemset(x_location, x)
            self.matrix.itemset(inverse_x_location, np.reciprocal(float(x)))
            return np.linalg.eigvals(self.matrix).max()

        # The upper bound of the solution space is 10 times the largest value of the matrix.
        upper_bound = np.nanmax(self.matrix) * 10

        for comparison in self.missing_comparisons:
            comparison_location = tuple(self.criteria.index(criterion) for criterion in comparison)
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', category=np.ComplexWarning)
                self.set_matrix(comparison)
                optimal_solution = sp.minimize_scalar(lambda_max, args=(comparison_location,),
                                                      method='bounded', bounds=(0, upper_bound)).x.real
            self.missing_comparisons[comparison] = optimal_solution

    def set_matrix(self, comparison):
        """
        Sets the value of every missing comparison in the comparison matrix (other than the current comparison)
        to its current value in the 'missing_comparisons' dictionary or its reciprocal.
        """
        for key, value in self.missing_comparisons.items():
            if key != comparison:
                location = tuple(self.criteria.index(criterion) for criterion in key)
                inverse_location = location[::-1]
                self.matrix.itemset(location, value)
                self.matrix.itemset(inverse_location, np.reciprocal(float(value)))

    def normalize_matrix(self):
        """
        Computes the priority vector of a valid matrix by normalizing the input values
        and sets the consistency ratio to 0.0.
        """
        self.priority_vector = np.divide(self.matrix, np.sum(self.matrix, keepdims=True)).round(self.precision)
        self.consistency_ratio = 0.0

    def compute(self):
        """
        Runs all functions necessary for building the weights and consistency ratio of the Compare object.
        """
        if not self.normalize:
            self.priority_vector = self.compute_priority_vector(self.matrix, self.iterations)
            if self.cr:
                self.compute_consistency_ratio()
        self.weights = {self.name: dict(zip(self.criteria, self.priority_vector))}

    def compute_priority_vector(self, matrix, iterations, comp_eigenvector=None):
        """
        Sets the 'priority_vector' property of the Compare object.
        :param matrix: numpy matrix, the matrix from which to derive the priority vector
        :param iterations: integer, number of iterations to run before the function stops
        :param comp_eigenvector: numpy array, a comparison eigenvector used during recursion
        """
        # Compute the principal eigenvector by normalizing the rows of a newly squared matrix
        sq_matrix = np.linalg.matrix_power(matrix, 2)
        row_sum = np.sum(sq_matrix, axis=1)
        total_sum = np.sum(sq_matrix)
        princ_eigenvector = np.divide(row_sum, total_sum)

        # Create a zero matrix as the comparison eigenvector if this is the first iteration
        if comp_eigenvector is None:
            comp_eigenvector = np.zeros(self.size)

        # Compute the difference between the principal and comparison eigenvectors
        remainder = np.subtract(princ_eigenvector, comp_eigenvector).round(self.precision)

        # If the difference between the two eigenvectors is zero (after rounding to the specified precision),
        # set the current principal eigenvector as the priority vector for the matrix...
        if not np.any(remainder):
            return princ_eigenvector.round(self.precision)

        # ...else recursively run the function until either there is no difference between
        # the principal and comparison eigenvectors, or until the predefined number of iterations has been met,
        # in which case set the last principal eigenvector as the priority vector
        iterations -= 1
        if iterations > 0:
            return self.compute_priority_vector(sq_matrix, iterations, princ_eigenvector)
        else:
            return princ_eigenvector.round(self.precision)

    def compute_consistency_ratio(self):
        """
        Sets the 'consistency_ratio' property of the Compare object, using random index estimates from
        Donegan and Dodd's 'A note on Saaty's Random Indexes' in Mathematical and Computer Modelling,
        15:10, 1991, 135-137 (doi: 10.1016/0895-7177(91)90098-R) by default (random_index='dd').
        If the random index of the object equals 'saaty', use the estimates from
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

        lambda_max = np.linalg.eigvals(self.matrix).max()  # Find the Perron-Frobenius eigenvalue of the matrix
        consistency_index = (lambda_max - self.size) / (self.size - 1)
        self.consistency_ratio = np.real(consistency_index / random_index).round(self.precision)


class Compose:
    # TODO Create a doc string for this
    def __init__(self, name=None, parent=None, children=None):
        self.name = name
        self.parent = parent
        self.children = children

        self.weights = dict()
        self.precision = None

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
        for pk, pv in self.parent.weights[self.parent.name].items():
            for child in self.children:

                if pk in child.weights:
                    for ck, cv in child.weights[pk].items():
                        try:
                            self.weights[ck] += np.multiply(pv, cv)
                        except KeyError:
                            self.weights[ck] = np.multiply(pv, cv)
                    break

    def normalize_total_priority(self):
        """
        Updates the 'weights' property of the Compose object with normalized values at the object's level of precision.
        """
        total_sum = sum(self.weights.values())
        comp_dict = {key: np.divide(value, total_sum).round(self.precision) for key, value in self.weights.items()}
        self.weights = {self.name: comp_dict}


if __name__ == '__main__':
    pass
