import numpy as np
from ahpy import ahpy

# Example from Saaty, Thomas L., 'Decision making with the analytic hierarchy process,'
#   Int. J. Services Sciences, 1:1, 2008, pp. 83-98.
drinks_cri = ('coffee', 'wine', 'tea', 'beer', 'sodas', 'milk', 'water')
drinks_val = np.array([[1, 9, 5, 2, 1, 1, .5],
                    [1/9., 1, 1/3., 1/9., 1/9., 1/9., 1/9.],
                    [.2, 3, 1, 1/3., .25, 1/3., 1/9.],
                    [.5, 9, 3, 1, .5, 1, 1/3.],
                    [1, 9, 4, 2, 1, 2, .5],
                    [1, 9, 3, 1, .5, 1, 1/3.],
                    [2, 9, 9, 3, 2, 3, 1]])


def test_drinks_cr_saaty():
    c = ahpy.Compare('Drinks', drinks_val, drinks_cri, precision=3, random_index='saaty')
    assert c.consistency_ratio == 0.022


def test_drinks_cr_dd():
    c = ahpy.Compare('Drinks', drinks_val, drinks_cri, precision=4, random_index='dd')
    assert c.consistency_ratio == 0.0235


def test_drinks_weights_saaty():
    c = ahpy.Compare('Drinks', drinks_val, drinks_cri, precision=3, random_index='saaty')
    assert c.weights == {'Drinks': {'coffee': 0.177, 'wine': 0.019, 'tea': 0.042, 'beer': 0.116, 'sodas': 0.19,
                                    'milk': 0.129, 'water': 0.327}}


def test_drinks_weights_dd():
    c = ahpy.Compare('Drinks', drinks_val, drinks_cri, precision=4, random_index='dd')
    assert c.weights == {'Drinks': {'coffee': 0.1775, 'wine': 0.0191, 'tea': 0.0418, 'beer': 0.1164, 'sodas': 0.1896,
                                    'milk': 0.1288, 'water': 0.3268}}


# Example from Saaty, Thomas, L., Theory and Applications of the Analytic Network Process, 2005.
crit = np.array([[1, .2, 3, .5, 5],
                  [5, 1, 7, 1, 7],
                  [1/3., 1/7., 1, .25, 3],
                  [2, 1, 4, 1, 7],
                  [.2, 1/7., 1/3., 1/7., 1]])

culture = np.array([[1, .5, 1, .5],
                     [2, 1, 2.5, 1],
                     [1, 1/2.5, 1, 1/2.5],
                     [2, 1, 2.5, 1]])

family = np.array([[1, 2, 1/3., 4],
                    [.5, 1, 1/8., 2],
                    [3, 8, 1, 9],
                    [.25, .5, 1/9., 1]])

housing = np.array([[1, 5, .5, 2.5],
                     [.2, 1, 1/9., .25],
                     [2, 9, 1, 7],
                     [1/2.5, 4, 1/7., 1]])

jobs = np.array([[1, .5, 3, 4],
                  [2, 1, 6, 8],
                  [1/3., 1/6., 1, 1],
                  [.25, 1/8., 1, 1]])

transportation = np.array([[1, 1.5, .5, 4],
                            [1/1.5, 1, 1/3.5, 2.5],
                            [2, 3.5, 1, 9],
                            [.25, 1/2.5, 1/9., 1]])

cities = ['Bethesda', 'Boston', 'Pittsburgh', 'Santa Fe']
crits = ['Culture', 'Family', 'Housing', 'Jobs', 'Transportation']


def test_cities_weights_saaty_precision_3():
    cu = ahpy.Compare('Culture', culture, cities, 3, random_index='Saaty')
    f = ahpy.Compare('Family', family, cities, 3, random_index='Saaty')
    h = ahpy.Compare('Housing', housing, cities, 3, random_index='Saaty')
    j = ahpy.Compare('Jobs', jobs, cities, 3, random_index='Saaty')
    t = ahpy.Compare('Transportation', transportation, cities, 3, random_index='Saaty')
    comp_matrices = [cu, f, h, j, t]

    cr = ahpy.Compare('Goal', crit, crits, 3, random_index='Saaty')

    c = ahpy.Compose('Goal', cr, comp_matrices)
    assert c.weights == {'Goal': {'Bethesda': 0.229161832598555, 'Boston': 0.2747607636360727,
                                  'Pittsburgh': 0.3851065361935014, 'Santa Fe': 0.11097086757187091}}


def test_cities_weights_dd_precision_4():
    cu = ahpy.Compare('Culture', culture, cities, 4)
    f = ahpy.Compare('Family', family, cities, 4)
    h = ahpy.Compare('Housing', housing, cities, 4)
    j = ahpy.Compare('Jobs', jobs, cities, 4)
    t = ahpy.Compare('Transportation', transportation, cities, 4)
    comp_matrices = [cu, f, h, j, t]

    cr = ahpy.Compare('Goal', crit, crits, 4)

    c = ahpy.Compose('Goal', cr, comp_matrices)
    assert c.weights == {'Goal': {'Bethesda': 0.22910249043701017, 'Boston': 0.274737184265749,
                                  'Pittsburgh': 0.3851800475463718, 'Santa Fe': 0.11098027775086894}}
