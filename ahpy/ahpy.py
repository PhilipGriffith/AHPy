import operator
import numpy as np
import itertools


class Compare(object):
    """
    This class computes the priority vector and consistency ratio of a positive
    reciprocal matrix. The 'weights' property contains the priority vector as a dictionary
    whose keys are criteria and whose values are the criteria's weights.
    The 'consistency_ratio' property contains the computed consistency ratio of the input matrix as a float.
    :param name: string, the name of the Compare object; if the object has a parent,
        this name MUST be included as a criterion of its parent
    :param matrix: numpy matrix, the matrix from which to derive the priority vector
    :param criteria: list of strings, the criteria of the matrix, listed in the same left-to-right
        order as their corresponding values in the input matrix
    :param precision: integer, number of decimal places of precision to compute both the priority
        vector and the consistency ratio; default is 4
    :param comp_type: string, the comparison type of the values in the input matrix, being either
        qualitative or quantitative; valid input: 'quant', 'qual'; default is 'qual'
    :param iters: integer, number of iterations before the compute_eigenvector function stops;
        default is 100
    :param random_index: string, the random index estimates used to compute the consistency ratio;
        valid input: 'dd', 'saaty'; default is 'dd'; see the compute_consistency_ratio function for more
        information regarding the different estimates
    """

    def __init__(self, name=None, comparisons=None, order=None,
                 precision=4, comp_type='qual', iters=100, random_index='dd'):
        self.name = name
        self.comparisons = comparisons
        self.order = order
        self.elements = []
        self.size = None
        self.pairs = []
        self.matrix = None

        self.shape = None
        self.type = comp_type
        self.precision = precision
        self.iterations = iters
        self.random_index = random_index.lower()
        self.priority_vector = None
        self.consistency_ratio = None
        self.weights = None

        self.permute_elements()
        self.insert_elements()
        self.build_matrix()

        self.compute()

    def permute_elements(self):
        for pair in self.comparisons:
            for element in pair:
                if element not in self.elements:
                    self.elements.append(element)
        self.size = len(self.elements)
        self.pairs = dict.fromkeys(itertools.permutations(self.elements, 2))

    def insert_elements(self):
        for pair, value in self.comparisons.items():
            inverse_pair = []
            for element in pair:
                inverse_pair.insert(0, element)
            self.pairs[pair] = value
            self.pairs[tuple(inverse_pair)] = np.reciprocal(float(value))

    def build_matrix(self):
        self.matrix = np.ones((self.size, self.size))
        for pair, value in self.pairs.items():
            location = []
            for element in pair:
                location.append(self.elements.index(element))
            self.matrix.itemset(tuple(location), value)

    def check_size_for_cr(self):
        """
        Insures that the matrix does not exceed 15 or 100 rows, depending on the chosen random index,
        so that every Compare object will have a consistency ratio.
        """
        return False if (self.random_index == 'saaty' and self.size > 15) or self.size > 100 else True

    def compute(self):
        try:
            # If the comparison type is quantitative, normalize the input values
            if self.type == 'quant':
                self.normalize()
            # If the comparison type is qualitative, compute both the priority vector and the
            # consistency ratio
            else:
                self.compute_priority_vector(self.matrix, self.iterations)
                self.compute_consistency_ratio()
            # Create the weights dictionary
            comp_dict = dict(zip(self.elements, self.priority_vector))
            self.weights = {self.name: comp_dict}
        except Exception as error:
            raise AHPException(error)

    def compute_priority_vector(self, matrix, iterations, comp_eigenvector=None):
        """
        Computes the priority vector of a matrix. Sets the 'remainder' and
        'priority_vector' properties of the Compare object.
        :param matrix: numpy matrix, the matrix from which to derive the priority vector
        :param iterations: integer, number of iterations to run before the function stops
        :param comp_eigenvector: numpy array, a comparison eigenvector used during
            recursion; DO NOT MODIFY
        """
        # Compute the principal eigenvector by normalizing the rows of a newly squared matrix
        sq_matrix = np.linalg.matrix_power(matrix, 2)
        row_sum = np.sum(sq_matrix, 1)
        total_sum = np.sum(row_sum)
        princ_eigenvector = np.divide(row_sum, total_sum).round(self.precision)
        # Create a zero matrix as the comparison eigenvector if this is the first iteration
        if comp_eigenvector is None:
            comp_eigenvector = np.zeros(self.shape)
        # Compute the difference between the principal and comparison eigenvectors
        remainder = np.subtract(princ_eigenvector, comp_eigenvector).round(self.precision)
        # If the difference between the two eigenvectors is zero (after rounding to the self.precision variable),
        # set the current principal eigenvector as the priority vector for the matrix
        if not np.any(remainder):
            self.priority_vector = princ_eigenvector
            return
        # Recursively run the function until either there is no difference between the principal and
        # comparison eigenvectors, or until the predefined number of iterations has been met, in which
        # case set the last principal eigenvector as the priority vector
        iterations -= 1
        if iterations > 0:
            return self.compute_priority_vector(sq_matrix, iterations, princ_eigenvector)
        else:
            self.priority_vector = princ_eigenvector
            return

    def compute_consistency_ratio(self):
        """
        Computes the consistency ratio of the matrix, using random index estimates from
        Donegan and Dodd's 'A note on Saaty's Random Indexes' in Mathematical and Computer
        Modelling, 15:10, 1991, 135-137 (doi: 10.1016/0895-7177(91)90098-R).
        If the random index of the object is set to 'saaty', use the estimates from
        Saaty, Thomas L. 2005. Theory And Applications Of The Analytic Network Process.
        Pittsburgh: RWS Publications, pg. 31.
        Sets the 'consistency_ratio' property of the Compare object.
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
        except KeyError:

            import bisect
            s = sorted(ri_dict)
            smaller = s[bisect.bisect_left(s, self.size) - 1]
            larger = s[bisect.bisect_right(s, self.size)]
            estimate = (ri_dict[larger] - ri_dict[smaller]) / (larger - smaller)
            random_index = estimate * (self.size - smaller) + ri_dict[smaller]

        try:
            # Find the Perron-Frobenius eigenvalue of the matrix
            lambda_max = np.linalg.eigvals(self.matrix).max()
            # Compute the consistency index
            consistency_index = (lambda_max - self.size) / (self.size - 1)
            # Compute the consistency ratio
            self.consistency_ratio = np.real(consistency_index / random_index).round(self.precision)
        except np.linalg.LinAlgError as error:
            raise AHPException(error)

    def report(self):
        print('Name:', self.name)
        print('CR:', self.consistency_ratio)
        print('Weights:')
        sorted_weights = sorted(self.weights[self.name].items(), key=operator.itemgetter(1), reverse=True)
        for k, v in sorted_weights:
            print('\t{}: {}'.format(k, round(v, self.precision)))
        print()


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
        Updates the 'precision' property of the Compose object by selecting
        the lowest precision of all input matrices.
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
        Updates the 'weights' property of the Compose object with
        their normalized values.
        """

        total_sum = sum(self.weights.values())
        comp_dict = {key: np.divide(value, total_sum) for key, value in self.weights.items()}
        self.weights = {self.name: comp_dict}

    def report(self):
        print('Name:', self.name)
        sorted_weights = sorted(self.weights[self.parent.name].items(), key=operator.itemgetter(1), reverse=True)
        for k, v in sorted_weights:
            print('\t{}: {}'.format(k, np.round(v, self.precision)))
        print()

        # print(self.parent.weights)
        # for child in self.children:
        #     print(child.weights)
        # print(self.weights)
        # print()


class AHPException(Exception):
    """
    The custom Exception class of the AHP module
    """
    def __init__(self, msg):
        print(msg)
        exit(1)


if __name__ == '__main__':
    pass
