import bisect
import itertools

import numpy as np
import scipy.optimize as sp


class Compare(object):
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
    :param iters: integer, number of iterations before the compute_eigenvector function stops;
        default is 100
    :param random_index: string, the random index estimates used to compute the consistency ratio;
        valid input: 'dd', 'saaty'; default is 'dd'; see the compute_consistency_ratio function for more
        information regarding the different estimates
    """

    def __init__(self, name=None, comparisons=None, order=None,
                 precision=4, iters=100, random_index='dd'):
        self.name = name
        self.comparisons = comparisons
        # TODO allow for ordering of the elements in a report
        self.order = order
        self.precision = precision
        self.iterations = iters
        self.random_index = random_index.lower()

        self.criteria = []
        self.pairs = []
        self.size = None
        self.matrix = None
        self.missing_comparisons = None
        self.priority_vector = None
        self.consistency_ratio = None
        self.weights = None

        self.permute_criteria()
        self.insert_comparisons()
        self.build_matrix()

        # print(self.matrix)
        print(self.pairs)
        self.get_missing_comparisons()
        if self.missing_comparisons:
            self.complete_matrix()

        print(self.pairs)
        # print(self.matrix)

        # self.compute()

        # TODO build report functionality

    def permute_criteria(self):
        """
        Creates an empty 'pairs' dictionary that contains all possible permutations
        of those criteria found within the keys of the input 'comparisons' dictionary.
        """
        for key in self.comparisons:
            for criterion in key:
                if criterion not in self.criteria:
                    self.criteria.append(criterion)
        self.pairs = dict.fromkeys(itertools.permutations(self.criteria, 2))
        self.size = len(self.criteria)

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
        self.matrix = np.ones((self.size, self.size))
        for pair, value in self.pairs.items():
            location = tuple(self.criteria.index(criterion) for criterion in pair)
            self.matrix.itemset(location, value)

    def set_matrix(self, comparison):
        for key, value in self.missing_comparisons.items():
            if key != comparison:
                location = tuple(self.criteria.index(criterion) for criterion in key)
                inverse_location = location[::-1]
                self.matrix.itemset(location, value)
                self.matrix.itemset(inverse_location, np.reciprocal(float(value)))

    @staticmethod
    def matprint(mat, fmt="g"):
        col_maxes = [max([len(("{:" + fmt + "}").format(x)) for x in col]) for col in mat.T]
        for x in mat:
            for i, y in enumerate(x):
                print(("{:" + str(col_maxes[i]) + fmt + "}").format(y), end="  ")
            print("")

    def complete_matrix(self):

        def lambda_max(x, x_location):
            inverse_x_location = x_location[::-1]
            self.matrix.itemset(x_location, x)
            self.matrix.itemset(inverse_x_location, np.reciprocal(float(x)))
            return np.linalg.eigvals(self.matrix).max()

        upper_solution_bound = np.nanmax(self.matrix) * 10

        for comparison in self.missing_comparisons:
            self.set_matrix(comparison)
            location = tuple(self.criteria.index(criterion) for criterion in comparison)

            self.matrix.itemset(location, None)
            self.matrix.itemset(location[::-1], None)
            self.matprint(self.matrix)
            print('---')

            optimal_solution = sp.minimize_scalar(lambda_max, args=(location,),
                                                  method='bounded', bounds=(1, upper_solution_bound)).x
            self.missing_comparisons[comparison] = optimal_solution

            self.matprint(self.matrix)
            print('-----------')

    def get_missing_comparisons(self):
        missing_comparisons = [key for key, value in self.pairs.items() if not value]
        for criteria in missing_comparisons:
            del missing_comparisons[missing_comparisons.index(criteria[::-1])]
        self.missing_comparisons = dict.fromkeys(missing_comparisons, 1)

    # TODO not yet used
    # TODO also check for all inputs being float or int >= 1
    def check_size_for_cr(self):
        """
        Returns True if the comparison matrix does not exceed either 15 or 100 rows, depending on the
        chosen random index. This is required to insure that the Compare object has a consistency ratio.
        """
        return False if (self.random_index == 'saaty' and self.size > 15) or self.size > 100 else True

    def compute(self):
        """
        Runs all functions necessary for building the weights and consistency ratio of the Compare object.
        """
        priority_vector = self.compute_priority_vector(self.matrix, self.iterations)
        self.weights = {self.name: dict(zip(self.criteria, priority_vector))}
        self.compute_consistency_ratio()

    def compute_priority_vector(self, matrix, iterations, comp_eigenvector=None):
        """
        Sets the 'priority_vector' property of the Compare object.
        :param matrix: numpy matrix, the matrix from which to derive the priority vector
        :param iterations: integer, number of iterations to run before the function stops
        :param comp_eigenvector: numpy array, a comparison eigenvector used during recursion; DO NOT MODIFY
        """
        # Compute the principal eigenvector by normalizing the rows of a newly squared matrix
        sq_matrix = np.linalg.matrix_power(matrix, 2)
        row_sum = np.sum(sq_matrix, 1)
        total_sum = np.sum(row_sum)
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
            s = sorted(ri_dict)
            smaller = s[bisect.bisect_left(s, self.size) - 1]
            larger = s[bisect.bisect_right(s, self.size)]
            estimate = (ri_dict[larger] - ri_dict[smaller]) / (larger - smaller)
            random_index = estimate * (self.size - smaller) + ri_dict[smaller]

        lambda_max = np.linalg.eigvals(self.matrix).max()  # Find the Perron-Frobenius eigenvalue of the matrix
        consistency_index = (lambda_max - self.size) / (self.size - 1)
        self.consistency_ratio = np.real(consistency_index / random_index).round(self.precision)


class Compose(object):

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
