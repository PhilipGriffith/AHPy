import itertools

import pytest

import ahpy

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
    assert c.local_weights == {'beer': 0.116, 'coffee': 0.177, 'milk': 0.129, 'soda': 0.190,
                               'tea': 0.042, 'water': 0.327, 'wine': 0.019}


def test_drinks_weights_precision_4_dd():
    c = ahpy.Compare('Drinks', drinks, precision=4, random_index='dd')
    assert c.local_weights == {'beer': 0.1164, 'coffee': 0.1775, 'milk': 0.1288, 'soda': 0.1896,
                               'tea': 0.0418, 'water': 0.3268, 'wine': 0.0191}


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

    cr = ahpy.Compare('Goal', criteria, precision=3, random_index='Saaty')
    cr.add_children([cu, f, h, j, t])

    assert cr.target_weights == {'Bethesda': 0.229, 'Boston': 0.275, 'Pittsburgh': 0.385, 'Santa Fe': 0.111}


def test_cities_weights_dd_precision_4():
    cu = ahpy.Compare('Culture', culture, precision=4)
    f = ahpy.Compare('Family', family, precision=4)
    h = ahpy.Compare('Housing', housing, precision=4)
    j = ahpy.Compare('Jobs', jobs, precision=4)
    t = ahpy.Compare('Transportation', transportation, precision=4)

    cr = ahpy.Compare('Goal', criteria, precision=4)
    cr.add_children([cu, f, h, j, t])

    assert cr.target_weights == {'Bethesda': 0.2291, 'Boston': 0.2748, 'Pittsburgh': 0.3852, 'Santa Fe': 0.1110}


# Examples from Bozóki, S., Fülöp, J. and Rónyai, L., 'On optimal completion of incomplete
# pairwise comparison matrices,' Mathematical and Computer Modelling, 52:1–2, 2010, pp. 318-333.
# https://doi.org/10.1016/j.mcm.2010.02.047

u = {('a', 'b'): 1, ('a', 'c'): 5, ('a', 'd'): 2,
     ('b', 'c'): 3, ('b', 'd'): 4}


def test_incomplete_example_missing_comparisons():
    cu = ahpy.Compare('Incomplete Example', u)
    assert cu._missing_comparisons == {('c', 'd'): 0.730297106886979}


def test_incomplete_example_weights():
    cu = ahpy.Compare('Incomplete Example', u)
    assert cu.local_weights == {'a': 0.3738, 'b': 0.392, 'c': 0.0985, 'd': 0.1357}


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
    assert cm._missing_comparisons == {('b', 'c'): 0.3300187496240363, ('b', 'e'): 1.7197409185349517,
                                       ('b', 'g'): 0.4663515002203321, ('c', 'd'): 9.920512661898753,
                                       ('c', 'f'): 4.852486449214693, ('c', 'h'): 0.5696073301509899,
                                       ('d', 'e'): 0.5252768142894285, ('d', 'g'): 0.1424438146531802,
                                       ('e', 'f'): 0.9311973564754218, ('e', 'h'): 0.10930828182051665,
                                       ('f', 'g'): 0.2912120796181874, ('g', 'h'): 0.4030898885178746}


# Example from Haas, R. and Meixner, L., 'An Illustrated Guide to the Analytic Hierarchy Process,'
# http://www.inbest.co.il/NGO/ahptutorial.pdf

def test_normalized_weights():
    fuel = {'civic': 34, 'saturn': 27, 'escort': 24, 'clio': 28}
    cf = ahpy.Compare('Fuel Economy', fuel)
    assert cf.local_weights == {'civic': 0.3009, 'saturn': 0.2389, 'escort': 0.2124, 'clio': 0.2478}


alphabet = 'abcdefghijklmnopqrstuvwxyz'
values = {'a': 0.0385, 'b': 0.0385, 'c': 0.0385, 'd': 0.0385, 'e': 0.0385, 'f': 0.0385, 'g': 0.0385, 'h': 0.0385,
     'i': 0.0385, 'j': 0.0385, 'k': 0.0385, 'l': 0.0385, 'm': 0.0385, 'n': 0.0385, 'o': 0.0385, 'p': 0.0385,
     'q': 0.0385, 'r': 0.0385, 's': 0.0385, 't': 0.0385, 'u': 0.0385, 'v': 0.0385, 'w': 0.0385, 'x': 0.0385,
     'y': 0.0385, 'z': 0.0385}


def test_size_limit_saaty():
    with pytest.raises(ValueError):
        x = dict.fromkeys(itertools.permutations(alphabet, 2), 1)
        ahpy.Compare('CR Test', x, random_index='saaty')


def test_size_limit_override_saaty():
    x = dict.fromkeys(itertools.permutations(alphabet, 2), 1)
    cx = ahpy.Compare('CR Test', x, random_index='saaty', cr=False)
    assert cx.local_weights == values


def test_size_limit_normalize_saaty():
    y = dict.fromkeys([i[0] for i in itertools.combinations(alphabet, 1)], 1)
    cy = ahpy.Compare('CR Test', y, random_index='saaty')
    assert cy.local_weights == values


a_m = {('b', 'c'): 1}
b_m = {('d', 'e'): 4}
d_m = {('f', 'g'): 2}

c_m = {'x': 2, 'y': 4, 'z': 4}
e_m = {'x': 1, 'y': 2, 'z': 3}
f_m = {'x': 2, 'y': 4, 'z': 4}
g_m = {'x': 1, 'y': 2, 'z': 3}

a = ahpy.Compare('a', a_m)
b = ahpy.Compare('b', b_m)
c = ahpy.Compare('c', c_m)
d = ahpy.Compare('d', d_m)
e = ahpy.Compare('e', e_m)
f = ahpy.Compare('f', f_m)
g = ahpy.Compare('g', g_m)

a.add_children([b, c])
b.add_children([d, e])
d.add_children([f, g])


def test_master_a():
    assert a.report() == {'name': 'a', 'weight': 1.0, 'weights': {'local': {'b': 0.5, 'c': 0.5}, 'global': {'b': 0.5, 'c': 0.5}, 'target': {'z': 0.4233, 'y': 0.3844, 'x': 0.1922}}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'elements': {'count': 2, 'names': ['b', 'c']}, 'children': {'count': 2, 'names': ['b', 'c']}, 'comparisons': {'count': 1, 'input': {('b', 'c'): 1}, 'computed': None}}


def test_master_b():
    assert b.report() == {'name': 'b', 'weight': 0.5, 'weights': {'local': {'d': 0.8, 'e': 0.2}, 'global': {'d': 0.4, 'e': 0.1}, 'target': None}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'elements': {'count': 2, 'names': ['d', 'e']}, 'children': {'count': 2, 'names': ['d', 'e']}, 'comparisons': {'count': 1, 'input': {('d', 'e'): 4}, 'computed': None}}


def test_master_c():
    assert c.report() == {'name': 'c', 'weight': 0.5, 'weights': {'local': {'y': 0.4, 'z': 0.4, 'x': 0.2}, 'global': {'y': 0.2, 'z': 0.2, 'x': 0.1}, 'target': None}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'elements': {'count': 3, 'names': ['x', 'y', 'z']}, 'children': None, 'comparisons': {'count': 3, 'input': {'x': 2, 'y': 4, 'z': 4}, 'computed': None}}


def test_master_d():
    assert d.report() == {'name': 'd', 'weight': 0.4, 'weights': {'local': {'f': 0.6667, 'g': 0.3333}, 'global': {'f': 0.2667, 'g': 0.1333}, 'target': None}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'elements': {'count': 2, 'names': ['f', 'g']}, 'children': {'count': 2, 'names': ['f', 'g']}, 'comparisons': {'count': 1, 'input': {('f', 'g'): 2}, 'computed': None}}


def test_master_e():
    assert e.report() == {'name': 'e', 'weight': 0.1, 'weights': {'local': {'z': 0.5, 'y': 0.3333, 'x': 0.1667}, 'global': {'z': 0.05, 'y': 0.0333, 'x': 0.0167}, 'target': None}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'elements': {'count': 3, 'names': ['x', 'y', 'z']}, 'children': None, 'comparisons': {'count': 3, 'input': {'x': 1, 'y': 2, 'z': 3}, 'computed': None}}


def test_master_f():
    assert f.report() == {'name': 'f', 'weight': 0.2667, 'weights': {'local': {'y': 0.4, 'z': 0.4, 'x': 0.2}, 'global': {'y': 0.1067, 'z': 0.1067, 'x': 0.0533}, 'target': None}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'elements': {'count': 3, 'names': ['x', 'y', 'z']}, 'children': None, 'comparisons': {'count': 3, 'input': {'x': 2, 'y': 4, 'z': 4}, 'computed': None}}


def test_master_g():
    assert g.report() == {'name': 'g', 'weight': 0.1333, 'weights': {'local': {'z': 0.5, 'y': 0.3333, 'x': 0.1667}, 'global': {'z': 0.0666, 'y': 0.0444, 'x': 0.0222}, 'target': None}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'elements': {'count': 3, 'names': ['x', 'y', 'z']}, 'children': None, 'comparisons': {'count': 3, 'input': {'x': 1, 'y': 2, 'z': 3}, 'computed': None}}
