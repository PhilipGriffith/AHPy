import bisect
import copy
import itertools
import json
import warnings

import numpy as np
import scipy.optimize as spo

import ahpy


class Compare:
    """
    This class computes the priority vector and consistency ratio of a positive reciprocal matrix, created using
    an input dictionary of pairwise comparison values. Optimal values are computed for any missing pairwise comparisons.
    NB: The 'name' property is used to link a child Compare object to its parent.
    :param name: string, the name of the Compare object;
        if the object has a parent, this name MUST be included as an element of its parent
    :param comparisons: dictionary, a dictionary in one of two forms: (i) each key is a tuple of two elements and
        each value is their pairwise comparison value, or (ii) each key is a single element and each value
        is that element's measured value
        Examples: (i) {('a', 'b'): 3, ('b', 'c'): 2}, (ii) {'a': 1.2, 'b': 2.3, 'c': 3.4}
    :param precision: integer, number of decimal places used when computing both the priority
        vector and the consistency ratio; default is 4
    :param random_index: string, the random index estimates used to compute the consistency ratio;
        see '_compute_consistency_ratio()' for more information regarding the different estimates;
        valid input: 'dd', 'saaty'; default is 'dd'
    :param iterations: integer, number of iterations before '_compute_priority_vector()' stops;
        default is 100
    :param tolerance: float, the stopping criteria for the cycling coordinates algorithm instantiated by
        '_complete_matrix()'; the algorithm stops when the difference between the norms of two cycles
         of coordinates is less than this value; default is 0.0001
    :param cr: boolean, whether to compute the priority vector's consistency ratio; default is True
    """

    def __init__(self, name, comparisons, precision=4, random_index='dd', iterations=100, tolerance=0.0001, cr=True):
        self.name = name
        self.comparisons = comparisons
        self.precision = precision
        self.random_index = random_index.lower() if cr else None
        self.iterations = iterations
        self.tolerance = tolerance
        self.cr = cr

        self._normalize = not isinstance(next(iter(self.comparisons)), tuple)
        self._elements = []
        self._pairs = []
        self._size = None
        self._matrix = None
        self._missing_comparisons = None

        self._node_parent = None
        self._node_children = None
        self._node_precision = self.precision
        self._node_weights = None

        self.global_weight = 1.0
        self.local_weight = self.global_weight
        self.consistency_ratio = None
        self.global_weights = None
        self.local_weights = None
        self.target_weights = None

        self._check_input()
        if self._normalize:
            self._build_normalized_elements()
            self._check_size()
            self._build_normalized_matrix()
        else:
            self._build_elements()
            self._check_size()
            self._insert_comparisons()
            self._build_matrix()
        self._get_missing_comparisons()
        if self._missing_comparisons:
            self._complete_matrix()
        self._compute()

        self.target_weights = self._node_weights if self.global_weight == 1.0 else None

    def __getitem__(self, item):
        return getattr(self, item)

    def _check_input(self):
        """
        Raises a ValueError if an input value is not greater than zero;
        raises a TypeError if an input value cannot be cast to a float.
        """
        for key, value in self.comparisons.items():
            try:
                if not float(value) > 0:
                    msg = f'{key}: {value} is an invalid input. All input values must be greater than zero.'
                    raise ValueError(msg)
            except TypeError:
                msg = f'{key}: {value} is an invalid input. All input values must be numeric.'
                raise TypeError(msg)

    def _build_elements(self):
        """
        Creates an empty 'pairs' dictionary that contains all possible permutations
        of those elements found within the keys of the input 'comparisons' dictionary.
        """
        for key in self.comparisons:
            for element in key:
                if element not in self._elements:
                    self._elements.append(element)
        self._pairs = dict.fromkeys(itertools.permutations(self._elements, 2))
        self._size = len(self._elements)

    def _build_normalized_elements(self):
        """
        Creates a list of those elements found within the keys of the input 'comparisons' dictionary.
        """
        self._elements = list(self.comparisons)
        self._pairs = {}
        self._size = len(self._elements)

    def _check_size(self):
        """
        Raises a ValueError if a consistency ratio is requested and
        the chosen random index does not support the size of the matrix.
        """
        if not self._normalize and self.cr and \
                ((self.random_index == 'saaty' and self._size > 15) or self._size > 100):
            msg = f"The input matrix of {self._size} x {self._size} is too large for {self.random_index}" \
                  " and a consistency ratio cannot be computed.\n" \
                  "\tThe maximum matrix size supported by the 'saaty' random index is 15 x 15;\n" \
                  "\tthe maximum matrix size supported by the 'dd' random index is 100 x 100.\n" \
                  "\tTo compute the priority vector of the matrix without a consistency ratio\n," \
                  "\tuse the 'cr=False' argument."
            raise ValueError(msg)

    def _insert_comparisons(self):
        """
        Fills the entries of the 'pairs' dictionary with the corresponding comparison values
        of the input 'comparisons' dictionary or their computed reciprocals.
        """
        for key, value in self.comparisons.items():
            inverse_key = key[::-1]
            self._pairs[key] = value
            self._pairs[inverse_key] = np.reciprocal(float(value))

    def _build_matrix(self):
        """
        Creates a correctly-sized numpy matrix of 1s, then fills the matrix with values from the 'pairs' dictionary.
        """
        self._matrix = np.ones((self._size, self._size))
        for pair, value in self._pairs.items():
            location = tuple(self._elements.index(elements) for elements in pair)
            self._matrix.itemset(location, value)

    def _build_normalized_matrix(self):
        """
        Creates a numpy matrix of values from the input 'comparisons' dictionary.
        """
        self._matrix = np.array(tuple(value for value in self.comparisons.values()), float)

    def _get_missing_comparisons(self):
        """
        Creates the 'missing comparisons' dictionary by populating its keys with the unique comparisons
        missing from the input 'comparisons' dictionary and populating its values with 1s.
        """
        missing_comparisons = [key for key, value in self._pairs.items() if not value]
        for elements in missing_comparisons:
            del missing_comparisons[missing_comparisons.index(elements[::-1])]
        self._missing_comparisons = dict.fromkeys(missing_comparisons, 1)

    def _complete_matrix(self):
        """
        Optimally completes an incomplete pairwise comparison matrix according to the algorithm described in
        Bozóki, S., Fülöp, J. and Rónyai, L., 'On optimal completion of incomplete pairwise comparison matrices,'
        Mathematical and Computer Modelling, 52:1–2, 2010, pp. 318-333. (https://doi.org/10.1016/j.mcm.2010.02.047)
        """
        last_iteration = np.array(tuple(self._missing_comparisons.values()))
        difference = np.inf
        while difference > self.tolerance:
            self._minimize_coordinate_values()
            current_iteration = np.array(tuple(self._missing_comparisons.values()))
            difference = np.linalg.norm(last_iteration - current_iteration)
            last_iteration = current_iteration

    def _minimize_coordinate_values(self):
        """
        Computes the minimum value for each missing value of the 'missing_comparisons' dictionary
        using the cyclic coordinates method described in Bozóki et al.
        """

        def lambda_max(x, x_location):
            """
            The function to be minimized. Finds the largest eigenvalue of a matrix.
            :param x: float, the variable to be minimized
            :param x_location: tuple, the matrix location of the variable to be minimized
            """
            inverse_x_location = x_location[::-1]
            self._matrix.itemset(x_location, x)
            self._matrix.itemset(inverse_x_location, np.reciprocal(float(x)))
            return np.max(np.linalg.eigvals(self._matrix))

        # The upper bound of the solution space is set to be 10 times the largest value of the matrix.
        upper_bound = np.nanmax(self._matrix) * 10

        for comparison in self._missing_comparisons:
            comparison_location = tuple(self._elements.index(element) for element in comparison)
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore', category=np.ComplexWarning)
                self._set_matrix(comparison)
                optimal_solution = spo.minimize_scalar(lambda_max, args=(comparison_location,),
                                                       method='bounded', bounds=(0, upper_bound))
            self._missing_comparisons[comparison] = np.real(optimal_solution.x)

    def _set_matrix(self, comparison):
        """
        Sets the value of every missing comparison in the comparison matrix (other than the current comparison)
        to its current value in the 'missing_comparisons' dictionary or its reciprocal.
        :param comparison: tuple, a key from the 'missing_comparisons' dictionary
        """
        for key, value in self._missing_comparisons.items():
            if key != comparison:
                location = tuple(self._elements.index(element) for element in key)
                inverse_location = location[::-1]
                self._matrix.itemset(location, value)
                self._matrix.itemset(inverse_location, np.reciprocal(float(value)))

    def _compute(self):
        """
        Runs all functions necessary for building the local weights and consistency ratio of the Compare object.
        """
        if not self._normalize:
            priority_vector = self._compute_priority_vector(self._matrix, self.iterations)
            if self.cr:
                self._compute_consistency_ratio()
        else:
            priority_vector = np.divide(self._matrix, np.sum(self._matrix, keepdims=True)).round(self.precision)
            self.consistency_ratio = 0.0
        weights = dict(zip(self._elements, priority_vector))
        self.local_weights = dict(sorted(weights.items(), key=lambda item: item[1], reverse=True))
        self.global_weights = self.local_weights.copy()
        self._node_weights = self.local_weights.copy()
        self.target_weights = self._node_weights

    def _compute_priority_vector(self, matrix, iterations, comp_eigenvector=None):
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
            comp_eigenvector = np.zeros(self._size)

        # Compute the difference between the principal and comparison eigenvectors
        remainder = np.subtract(principal_eigenvector, comp_eigenvector).round(self.precision)

        # If the difference between the two eigenvectors is zero (after rounding to the specified precision),
        # set the current principal eigenvector as the priority vector for the matrix...
        if not np.any(remainder):
            return principal_eigenvector.round(self.precision)

        # ...else recursively run the function until either there is no difference between the rounded
        # principal and comparison eigenvectors, or until the predefined number of iterations has been met,
        # in which case set the last principal eigenvector as the priority vector
        iterations -= 1
        if iterations > 0:
            return self._compute_priority_vector(sq_matrix, iterations, principal_eigenvector)
        else:
            return principal_eigenvector.round(self.precision)

    def _compute_consistency_ratio(self):
        """
        Sets the 'consistency_ratio' property of the Compare object, using random index estimates from
        Donegan, H.A. and Dodd, F.J., 'A Note on Saaty's Random Indexes,' Mathematical and Computer Modelling,
        15:10, 1991, pp. 135-137 (DOI: 10.1016/0895-7177(91)90098-R) by default (random_index='dd').
        If the random index of the object is 'saaty', uses the estimates from
        Saaty's Theory And Applications Of The Analytic Network Process, Pittsburgh: RWS Publications, 2005, p. 31.
        """
        # A valid, square, reciprocal matrix with only one or two rows must be consistent
        if self._size < 3:
            self.consistency_ratio = 0.0
            return
        if self.random_index == 'saaty':
            ri_dict = {3: 0.52, 4: 0.89, 5: 1.11, 6: 1.25, 7: 1.35, 8: 1.40, 9: 1.45,
                       10: 1.49, 11: 1.52, 12: 1.54, 13: 1.56, 14: 1.58, 15: 1.59}
        elif self.random_index == 'dd':
            ri_dict = {3: 0.4914, 4: 0.8286, 5: 1.0591, 6: 1.1797, 7: 1.2519,
                       8: 1.3171, 9: 1.3733, 10: 1.4055, 11: 1.4213, 12: 1.4497,
                       13: 1.4643, 14: 1.4822, 15: 1.4969, 16: 1.5078, 17: 1.5153,
                       18: 1.5262, 19: 1.5313, 20: 1.5371, 25: 1.5619, 30: 1.5772,
                       40: 1.5976, 50: 1.6102, 60: 1.6178, 70: 1.6237, 80: 1.6277,
                       90: 1.6213, 100: 1.6339}
        else:
            return

        try:
            random_index = ri_dict[self._size]
        # If the size of the comparison matrix falls between two computed estimates, compute a weighted estimate
        except KeyError:
            s = tuple(ri_dict.keys())
            smaller = s[bisect.bisect_left(s, self._size) - 1]
            larger = s[bisect.bisect_right(s, self._size)]
            estimate = (ri_dict[larger] - ri_dict[smaller]) / (larger - smaller)
            random_index = estimate * (self._size - smaller) + ri_dict[smaller]

        # Find the Perron-Frobenius eigenvalue of the matrix
        lambda_max = np.max(np.linalg.eigvals(self._matrix))
        consistency_index = (lambda_max - self._size) / (self._size - 1)
        # The absolute value avoids confusion in those rare cases where a small negative float is rounded to -0.0
        self.consistency_ratio = np.abs(np.real(consistency_index / random_index).round(self.precision))

    def add_children(self, children):
        """
        Sets the input Compare objects as children of the current Compare object, assigns itself as their parent,
        then updates the global and target weights of the new hierarchy.
        NB: A child Compare object's name MUST be included as an element of the current Compare object.
        :param children: list or tuple, Compare objects to form the children of the current Compare object
        """
        self._node_children = children
        self._check_children()
        for child in self._node_children:
            child._node_parent = self
        self._recompute()

    def _check_children(self):
        """
        Raises a TypeError if an input child is not a Compare object.
        """
        for child in self._node_children:
            if not isinstance(child, Compare):
                msg = 'A Compare object is either misconfigured or missing from the hierarchy.'
                raise TypeError(msg)

    def _recompute(self):
        """
        Calls all functions necessary for building the target weights of the Compare object,
        given its children, as well as updating the global weights of the Compare object's descendants.
        Then calls the same function on the current Compare object's parent.
        """
        self._set_node_precision()
        self._compute_node_weights()
        self._set_target_weights()
        self._compute_global_and_local_weights()
        if self._node_parent:
            self._node_parent._recompute()

    def _set_node_precision(self):
        """
        Sets the '_node_precision' property of the Compare object by selecting the lowest precision of its children.
        """
        lowest_precision = np.min([child._node_precision for child in self._node_children])
        if lowest_precision < self.precision:
            self._node_precision = lowest_precision
        else:
            self._node_precision = self.precision

    def _compute_node_weights(self):
        """
        Builds the '_node_weights' dictionary of the Compare object, given the target weights of its children.
        """
        self._node_weights = dict()
        for parent_key, parent_value in self.local_weights.items():
            for child in self._node_children:
                if parent_key == child.name:
                    for child_key, child_value in child._node_weights.items():
                        value = parent_value * child_value
                        try:
                            self._node_weights[child_key] += value
                        except KeyError:
                            self._node_weights[child_key] = value
                    break
        self._node_weights = dict(sorted(self._node_weights.items(), key=lambda item: item[1], reverse=True))
        self._node_weights = {key: value.round(self._node_precision) for key, value in self._node_weights.items()}

    def _set_target_weights(self):
        """
        Removes the 'target_weights' property of all children, then resets the property of the current Compare object.
        """
        for child in self._node_children:
            child.target_weights = None
        self.target_weights = self._node_weights

    def _compute_global_and_local_weights(self):
        """
        Recursively updates both the global and local weights of the Compare object's immediate descendants.
        """
        if self._node_children:
            for parent_key, parent_value in self.local_weights.items():
                for child in self._node_children:
                    if parent_key == child.name:
                        child.global_weight = np.round(self.global_weight * parent_value, self.precision)
                        child.local_weight = parent_value
                        child._apply_weight()
                        child._compute_global_and_local_weights()
                        break

    def _apply_weight(self):
        """
        Updates the 'global_weights' dictionary of the Compare object, given the global weight of the node.
        """
        for key in self.global_weights:
            self.global_weights[key] = np.round(self.global_weight * self.local_weights[key], self.precision)

    def _get_report(self, params):
        """
        Climbs to the top of the hierarchy, then calls '_build_report()'.
        :param params: tuple, a nested dictionary containing reports and a boolean for the verbose argument
        """
        if self.global_weight != 1.0:
            self._node_parent._get_report(params)
        else:
            return self._build_report(params)

    def _build_report(self, params):
        """
        Creates a standard or verbose report for the Compare object, then calls itself on all of the object's children.
        :param params: tuple, a nested dictionary containing reports and a boolean for the verbose argument
        """

        def set_random_index():
            """
            Returns the full name of a valid random index as a string, else None.
            """
            random_index = None
            if self.random_index == 'dd':
                random_index = 'Donegan & Dodd'
            elif self.random_index == 'saaty':
                random_index = 'Saaty'
            return random_index

        hierarchy, verbose = params

        hierarchy[self.name] = {'name': self.name,
                                'global_weight': self.global_weight,
                                'local_weight': self._node_parent.local_weights[
                                    self.name] if self.global_weight != 1.0 else 1.0,
                                'target_weights': self._node_weights if self.global_weight == 1.0 else None,
                                'elements': {
                                    'global_weights': self.global_weights,
                                    'local_weights': self.local_weights,
                                    'consistency_ratio': self.consistency_ratio
                                }
                                }
        if verbose:
            hierarchy[self.name]['elements'].update({'random_index': set_random_index(),
                                                     'count': len(self._elements),
                                                     'names': self._elements})
            hierarchy[self.name].update({'children': {
                'count': len(self._node_children),
                'names': [child.name for child in self._node_children]
            } if self._node_children else None,
                                         'comparisons': {
                                             'count': len(self.comparisons) + len(self._missing_comparisons),
                                             'input': self.comparisons,
                                             'computed': self._missing_comparisons if self._missing_comparisons else None
                                         }
                                         })
        if self._node_children:
            for child in self._node_children:
                child._build_report(params)

        return hierarchy

    def report(self, complete=False, show=False, verbose=False):
        """
        Returns the key information of the Compare object as a dictionary, optionally prints to the console.
        :param complete: boolean, whether to return a report for every Compare object in the hierarchy; default is False
        :param show: boolean, whether to print the report to the console; default is False
        :param verbose: boolean, whether to include full details of the Compare object within the report; default is False
        """

        def convert_keys_to_json_format(input_dict):
            """
            Returns a dictionary with keys in JSON format.
            :param input_dict: dictionary, the dictionary to be converted
            """
            try:
                comparisons = {}
                for key, value in input_dict.items():
                    comparisons[', '.join(key)] = value
            except AttributeError:
                comparisons = input_dict
            return comparisons

        hierarchy = {}
        self._get_report((hierarchy, verbose))
        if not complete:
            hierarchy = dict({'name': self.name}, **hierarchy[self.name])

        if show:
            json_report = copy.deepcopy(hierarchy)
            if verbose:
                for comparison in ('input', 'computed'):
                    if complete:
                        for key in json_report.keys():
                            json_report[key]['comparisons'][comparison] = convert_keys_to_json_format(
                                json_report[key]['comparisons'][comparison])
                    else:
                        json_report['comparisons'][comparison] = convert_keys_to_json_format(
                            json_report['comparisons'][comparison])
            print(json.dumps(json_report, indent=4))

        return hierarchy


class Compose:
    """
    This class provides an alternative way to build a hierarchy of Compare objects using a dictionary
    of parent-child relationships, as well as an alternative way to build Compare objects using a list or tuple
    of the necessary inputs.
    """

    def __init__(self):
        self.nodes = []
        self.hierarchy = None

    def __getitem__(self, item):
        return self._get_node(item)

    def __getattr__(self, item):
        return self._get_node(item)

    def _get_node(self, name):
        """
        Returns the named Compare object.
        :param name: string, the name of the desired Compare object
        """
        for node in self.nodes:
            if node.name == name:
                return node

    def add_comparisons(self, item,
                        comparisons=None, precision=4, random_index='dd', iterations=100, tolerance=0.0001, cr=True):
        """
        Adds Compare objects to a stored list of nodes. Input can be either one or more Compare objects,
        one or more lists or tuples containing the inputs necessary to create a Compare object,
        or the arguments necessary to create a Compare object.
        The method signature is intended to mimic that of the Compare class for this reason.
        :param item: Compare object, list or tuple, string, either one or more Compare objects (or the data required
            to create a Compare object, stored as a list or tuple) or the 'name' argument that forms
            the first parameter required to create a new Compare object
        :param comparisons: dictionary, the elements and values to be compared, provided in one of two forms: (i) each key is a tuple of two elements and
            each value is their pairwise comparison value, or (ii) each key is a single element and each value
            is that element's measured value; default is None
            Examples: (i) {('a', 'b'): 3, ('b', 'c'): 2}, (ii) {'a': 1.2, 'b': 2.3, 'c': 3.4}
        :param precision: integer, number of decimal places used when computing both the priority
            vector and the consistency ratio; default is 4
        :param random_index: string, the random index estimates used to compute the consistency ratio;
            see '_compute_consistency_ratio()' for more information regarding the different estimates;
            valid input: 'dd', 'saaty'; default is 'dd'
        :param iterations: integer, number of iterations before '_compute_priority_vector()' stops;
            default is 100
        :param tolerance: float, the stopping criteria for the cycling coordinates algorithm instantiated by
            '_complete_matrix()'; the algorithm stops when the difference between the norms of two cycles
             of coordinates is less than this value; default is 0.0001
        :param cr: boolean, whether to compute the priority vector's consistency ratio; default is True
        """
        if isinstance(item, ahpy.Compare):
            self.nodes.append(item)
        elif isinstance(item, (list, tuple)):
            for i in item:
                if isinstance(i, ahpy.Compare):
                    self.nodes.append(i)
                elif isinstance(i, str):
                    self.nodes.append(ahpy.Compare(*item))
                    break
                else:
                    self.nodes.append(ahpy.Compare(*i))
        else:  # item is a Compare object name
            self.nodes.append(ahpy.Compare(item, comparisons, precision, random_index, iterations, tolerance, cr))

    def add_hierarchy(self, hierarchy):
        """
        Builds a hierarchy of the stored Compare objects according to the input.
        :param hierarchy: dictionary, a representation of the hierarchy in which each key of the dictionary
            is the name of a parent and each value is a list of names of one or more of its children
            Example: {'a': ['b', 'c'], 'b': ['d', 'e']}
        """
        try:
            self.hierarchy = hierarchy
            for name in self.hierarchy.keys():
                children = [self._get_node(child_name) for child_name in self.hierarchy[name]]
                self._get_node(name).add_children(children)
        except AttributeError:
            msg = 'All comparisons must be added to the Compose object before adding a hierarchy.'
            raise AttributeError(msg)

    def report(self, name=None, show=False, verbose=False):
        """
        Returns the key information of the stored Compare objects as a dictionary, optionally prints to the console.
        :param name: string, the name of the Compare object report to return; if None, returns a complete report
            for the given hierarchy; default is None
        :param show: boolean, whether to print the report to the console; default is False
        :param verbose: boolean, whether to include full details of the Compare object within the report;
            default is False
        """
        if name:
            report = self._get_node(name).report(complete=False, show=show, verbose=verbose)
        else:
            report = self._get_node(list(self.hierarchy.keys())[0]).report(complete=True, show=show, verbose=verbose)
        return report
