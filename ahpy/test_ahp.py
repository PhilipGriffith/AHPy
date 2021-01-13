import itertools

import pytest

from ahpy import ahpy

# Example from Saaty, Thomas L., 'Decision making with the analytic hierarchy process,'
# Int. J. Services Sciences, 1:1, 2008, pp. 83-98.

drinks = {('coffee', 'wine'): 9, ('coffee', 'tea'): 5, ('coffee', 'beer'): 2, ('coffee', 'soda'): 1,
          ('coffee', 'milk'): 1,
          ('water', 'coffee'): 2, ('water', 'coffee'): 2, ('water', 'wine'): 9, ('water', 'tea'): 9,
          ('water', 'beer'): 3, ('water', 'soda'): 2, ('water', 'milk'): 3,
          ('tea', 'wine'): 3,
          ('beer', 'wine'): 9, ('beer', 'tea'): 3, ('beer', 'milk'): 1,
          ('soda', 'wine'): 9, ('soda', 'tea'): 4, ('soda', 'beer'): 2, ('soda', 'milk'): 2,
          ('milk', 'wine'): 9, ('milk', 'tea'): 3}


def test_drinks_cr_saaty():
    c = ahpy.Compare('Drinks', drinks, precision=3, random_index='saaty')
    assert c.consistency_ratio == 0.022


def test_drinks_cr_dd():
    c = ahpy.Compare('Drinks', drinks, precision=4, random_index='dd')
    assert c.consistency_ratio == 0.0235


def test_drinks_weights_precision_3_saaty():
    c = ahpy.Compare('Drinks', drinks, precision=3, random_index='saaty')
    assert c.weights == {'Drinks': {'beer': 0.116, 'coffee': 0.177, 'milk': 0.129, 'soda': 0.190,
                                    'tea': 0.042, 'water': 0.327, 'wine': 0.019}}


def test_drinks_weights_precision_4_dd():
    c = ahpy.Compare('Drinks', drinks, precision=4, random_index='dd')
    assert c.weights == {'Drinks': {'beer': 0.1164, 'coffee': 0.1775, 'milk': 0.1288, 'soda': 0.1896,
                                    'tea': 0.0418, 'water': 0.3268, 'wine': 0.0191}}


# Example from Saaty, Thomas, L., Theory and Applications of the Analytic Network Process, 2005.

criteria = {('Culture', 'Housing'): 3, ('Culture', 'Transportation'): 5,
            ('Family', 'Culture'): 5, ('Family', 'Housing'): 7, ('Family', 'Transportation'): 7,
            ('Housing', 'Transportation'): 3,
            ('Jobs', 'Culture'): 2, ('Jobs', 'Housing'): 4, ('Jobs', 'Transportation'): 7,
            ('Family', 'Jobs'): 1}

culture = {('Bethesda', 'Pittsburgh'): 1,
           ('Boston', 'Bethesda'): 2, ('Boston', 'Pittsburgh'): 2.5, ('Boston', 'Santa Fe'): 1,
           ('Pittsburgh', 'Bethesda'): 1,
           ('Santa Fe', 'Bethesda'): 2, ('Santa Fe', 'Pittsburgh'): 2.5}

family = {('Bethesda', 'Boston'): 2, ('Bethesda', 'Santa Fe'): 4,
          ('Boston', 'Santa Fe'): 2,
          ('Pittsburgh', 'Bethesda'): 3, ('Pittsburgh', 'Boston'): 8, ('Pittsburgh', 'Santa Fe'): 9}

housing = {('Bethesda', 'Boston'): 5, ('Bethesda', 'Santa Fe'): 2.5,
           ('Pittsburgh', 'Bethesda'): 2, ('Pittsburgh', 'Boston'): 9, ('Pittsburgh', 'Santa Fe'): 7,
           ('Santa Fe', 'Boston'): 4}

jobs = {('Bethesda', 'Pittsburgh'): 3, ('Bethesda', 'Santa Fe'): 4,
        ('Boston', 'Bethesda'): 2, ('Boston', 'Pittsburgh'): 6, ('Boston', 'Santa Fe'): 8,
        ('Pittsburgh', 'Santa Fe'): 1}

transportation = {('Bethesda', 'Boston'): 1.5,
                  ('Bethesda', 'Santa Fe'): 4,
                  ('Boston', 'Santa Fe'): 2.5,
                  ('Pittsburgh', 'Bethesda'): 2,
                  ('Pittsburgh', 'Boston'): 3.5,
                  ('Pittsburgh', 'Santa Fe'): 9}


def test_cities_weights_saaty_precision_3():
    cu = ahpy.Compare('Culture', culture, precision=3, random_index='Saaty')
    f = ahpy.Compare('Family', family, precision=3, random_index='Saaty')
    h = ahpy.Compare('Housing', housing, precision=3, random_index='Saaty')
    j = ahpy.Compare('Jobs', jobs, precision=3, random_index='Saaty')
    t = ahpy.Compare('Transportation', transportation, precision=3, random_index='Saaty')
    comp_matrices = [cu, f, h, j, t]

    cr = ahpy.Compare('Goal', criteria, precision=3, random_index='Saaty')

    c = ahpy.Compose('Goal', cr, comp_matrices)
    assert c.weights == {'Goal': {'Bethesda': 0.229, 'Boston': 0.275, 'Pittsburgh': 0.385, 'Santa Fe': 0.111}}


def test_cities_weights_dd_precision_4():
    cu = ahpy.Compare('Culture', culture, precision=4)
    f = ahpy.Compare('Family', family, precision=4)
    h = ahpy.Compare('Housing', housing, precision=4)
    j = ahpy.Compare('Jobs', jobs, precision=4)
    t = ahpy.Compare('Transportation', transportation, precision=4)
    comp_matrices = [cu, f, h, j, t]

    cr = ahpy.Compare('Goal', criteria, precision=4)

    c = ahpy.Compose('Goal', cr, comp_matrices)
    assert c.weights == {'Goal': {'Bethesda': 0.2291, 'Boston': 0.2747, 'Pittsburgh': 0.3852, 'Santa Fe': 0.1110}}


# Examples from Bozóki, S., Fülöp, J. and Rónyai, L., 'On optimal completion of incomplete
# pairwise comparison matrices,' Mathematical and Computer Modelling, 52:1–2, 2010, pp. 318-333.
# https://doi.org/10.1016/j.mcm.2010.02.047

u = {('a', 'b'): 1, ('a', 'c'): 5, ('a', 'd'): 2,
     ('b', 'c'): 3, ('b', 'd'): 4}


def test_incomplete_example_missing_comparisons():
    cu = ahpy.Compare('Incomplete Example', u)
    assert cu.missing_comparisons == {('c', 'd'): 0.730297106886979}


def test_incomplete_example_weights():
    cu = ahpy.Compare('Incomplete Example', u)
    assert cu.weights == {'Incomplete Example': {'a': 0.3738, 'b': 0.392, 'c': 0.0985, 'd': 0.1357}}


def test_incomplete_example_cr():
    cu = ahpy.Compare('Incomplete Example', u)
    assert cu.consistency_ratio == 0.0372


def test_incomplete_housing_missing_comparisons():
    m = {('a', 'b'): 5, ('a', 'c'): 3, ('a', 'd'): 7, ('a', 'e'): 6, ('a', 'f'): 6,
         ('b', 'd'): 5, ('b', 'f'): 3,
         ('c', 'e'): 3, ('c', 'g'): 6,
         ('f', 'd'): 4,
         ('g', 'a'): 3, ('g', 'e'): 5,
         ('h', 'a'): 4, ('h', 'b'): 7, ('h', 'd'): 8, ('h', 'f'): 6}
    cm = ahpy.Compare('Incomplete Housing', m)
    assert cm.missing_comparisons == {('b', 'c'): 0.3300187496240363, ('b', 'e'): 1.7197409185349517,
                                      ('b', 'g'): 0.4663515002203321, ('c', 'd'): 9.920512661898753,
                                      ('c', 'f'): 4.852486449214693, ('c', 'h'): 0.5696073301509899,
                                      ('d', 'e'): 0.5252768142894285, ('d', 'g'): 0.1424438146531802,
                                      ('e', 'f'): 0.9311973564754218, ('e', 'h'): 0.10930828182051665,
                                      ('f', 'g'): 0.2912120796181874, ('g', 'h'): 0.4030898885178746}


# Example from Haas, R. and Meixner, L., 'An Illustrated Guide to the Analytic Hierarchy Process,'
# http://www.inbest.co.il/NGO/ahptutorial.pdf

def test_normalized_weights():
    f = {'civic': 34, 'saturn': 27, 'escort': 24, 'clio': 28}
    cf = ahpy.Compare('Fuel Economy', f)
    assert cf.weights == {'Fuel Economy': {'civic': 0.3009, 'saturn': 0.2389, 'escort': 0.2124, 'clio': 0.2478}}


a = 'abcdefghijklmnopqrstuvwxyz'
b = {'a': 0.0385, 'b': 0.0385, 'c': 0.0385, 'd': 0.0385, 'e': 0.0385, 'f': 0.0385, 'g': 0.0385, 'h': 0.0385,
     'i': 0.0385, 'j': 0.0385, 'k': 0.0385, 'l': 0.0385, 'm': 0.0385, 'n': 0.0385, 'o': 0.0385, 'p': 0.0385,
     'q': 0.0385, 'r': 0.0385, 's': 0.0385, 't': 0.0385, 'u': 0.0385, 'v': 0.0385, 'w': 0.0385, 'x': 0.0385,
     'y': 0.0385, 'z': 0.0385}


def test_size_limit_saaty():
    with pytest.raises(ValueError):
        x = dict.fromkeys(itertools.permutations(a, 2), 1)
        ahpy.Compare('CR Test', x, random_index='saaty')


def test_size_limit_override_saaty():
    x = dict.fromkeys(itertools.permutations(a, 2), 1)
    cx = ahpy.Compare('CR Test', x, random_index='saaty', cr=False)
    assert cx.weights == {'CR Test': b}


def test_size_limit_normalize_saaty():
    y = dict.fromkeys([i[0] for i in itertools.combinations(a, 1)], 1)
    cy = ahpy.Compare('CR Test', y, random_index='saaty')
    assert cy.weights == {'CR Test': b}
