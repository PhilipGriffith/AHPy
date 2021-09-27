import itertools

import pytest

import ahpy

# Example from Saaty, Thomas L., 'Decision making with the analytic hierarchy process,'
# Int. J. Services Sciences, 1:1, 2008, pp. 83-98.

drinks = {('coffee', 'wine'): 9, ('coffee', 'tea'): 5, ('coffee', 'beer'): 2, ('coffee', 'soda'): 1,
          ('coffee', 'milk'): 1,
          ('water', 'coffee'): 2, ('water', 'wine'): 9, ('water', 'tea'): 9,
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


def test_cities_target_weights():
    cu = ahpy.Compare('Culture', culture, precision=4)
    f = ahpy.Compare('Family', family, precision=4)
    h = ahpy.Compare('Housing', housing, precision=4)
    j = ahpy.Compare('Jobs', jobs, precision=4)
    t = ahpy.Compare('Transportation', transportation, precision=4)

    cr = ahpy.Compare('Goal', criteria, precision=4)
    cr.add_children([cu, f, h, j, t])

    assert t.target_weights is None


# Examples from Bozóki, S., Fülöp, J. and Rónyai, L., 'On optimal completion of incomplete
# pairwise comparison matrices,' Mathematical and Computer Modelling, 52:1–2, 2010, pp. 318-333.
# https://doi.org/10.1016/j.mcm.2010.02.047

u = {('a', 'b'): 1, ('a', 'c'): 5, ('a', 'd'): 2,
     ('b', 'c'): 3, ('b', 'd'): 4}


def test_incomplete_example_missing_comparisons():
    cu = ahpy.Compare('Incomplete Example', u)
    assert cu._missing_comparisons == pytest.approx({('c', 'd'): 0.730297106886979})


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
    assert (cm._missing_comparisons ==
            pytest.approx({('b', 'c'): 0.3300187496240363, ('b', 'e'): 1.7197409185349517,
                           ('b', 'g'): 0.4663515002203321, ('c', 'd'): 9.920512661898753,
                           ('c', 'f'): 4.852486449214693, ('c', 'h'): 0.5696073301509899,
                           ('d', 'e'): 0.5252768142894285, ('d', 'g'): 0.1424438146531802,
                           ('e', 'f'): 0.9311973564754218, ('e', 'h'): 0.10930828182051665,
                           ('f', 'g'): 0.2912120796181874, ('g', 'h'): 0.4030898885178746}))


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
    assert a.report(verbose=True) == {'name': 'a', 'global_weight': 1.0, 'local_weight': 1.0,
                                      'target_weights': {'z': 0.4233, 'y': 0.3844, 'x': 0.1922},
                                      'elements': {'global_weights': {'b': 0.5, 'c': 0.5},
                                                   'local_weights': {'b': 0.5, 'c': 0.5}, 'consistency_ratio': 0.0,
                                                   'random_index': 'Donegan & Dodd', 'count': 2, 'names': ['b', 'c']},
                                      'children': {'count': 2, 'names': ['b', 'c']},
                                      'comparisons': {'count': 1, 'input': {('b', 'c'): 1}, 'computed': None}}


def test_master_b():
    assert b.report(verbose=True) == {'name': 'b', 'global_weight': 0.5, 'local_weight': 0.5, 'target_weights': None,
                                      'elements': {'global_weights': {'d': 0.4, 'e': 0.1},
                                                   'local_weights': {'d': 0.8, 'e': 0.2}, 'consistency_ratio': 0.0,
                                                   'random_index': 'Donegan & Dodd', 'count': 2, 'names': ['d', 'e']},
                                      'children': {'count': 2, 'names': ['d', 'e']},
                                      'comparisons': {'count': 1, 'input': {('d', 'e'): 4}, 'computed': None}}


def test_master_c():
    assert c.report(verbose=True) == {'name': 'c', 'global_weight': 0.5, 'local_weight': 0.5, 'target_weights': None,
                                      'elements': {'global_weights': {'y': 0.2, 'z': 0.2, 'x': 0.1},
                                                   'local_weights': {'y': 0.4, 'z': 0.4, 'x': 0.2},
                                                   'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd',
                                                   'count': 3, 'names': ['x', 'y', 'z']}, 'children': None,
                                      'comparisons': {'count': 3, 'input': {'x': 2, 'y': 4, 'z': 4}, 'computed': None}}


def test_master_d():
    assert d.report(verbose=True) == {'name': 'd', 'global_weight': 0.4, 'local_weight': 0.8, 'target_weights': None,
                                      'elements': {'global_weights': {'f': 0.2667, 'g': 0.1333},
                                                   'local_weights': {'f': 0.6667, 'g': 0.3333},
                                                   'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd',
                                                   'count': 2, 'names': ['f', 'g']},
                                      'children': {'count': 2, 'names': ['f', 'g']},
                                      'comparisons': {'count': 1, 'input': {('f', 'g'): 2}, 'computed': None}}


def test_master_e():
    assert e.report(verbose=True) == {'name': 'e', 'global_weight': 0.1, 'local_weight': 0.2, 'target_weights': None,
                                      'elements': {'global_weights': {'z': 0.05, 'y': 0.0333, 'x': 0.0167},
                                                   'local_weights': {'z': 0.5, 'y': 0.3333, 'x': 0.1667},
                                                   'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd',
                                                   'count': 3, 'names': ['x', 'y', 'z']}, 'children': None,
                                      'comparisons': {'count': 3, 'input': {'x': 1, 'y': 2, 'z': 3}, 'computed': None}}


def test_master_f():
    assert f.report(verbose=True) == {'name': 'f', 'global_weight': 0.2667, 'local_weight': 0.6667,
                                      'target_weights': None,
                                      'elements': {'global_weights': {'y': 0.1067, 'z': 0.1067, 'x': 0.0533},
                                                   'local_weights': {'y': 0.4, 'z': 0.4, 'x': 0.2},
                                                   'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd',
                                                   'count': 3, 'names': ['x', 'y', 'z']}, 'children': None,
                                      'comparisons': {'count': 3, 'input': {'x': 2, 'y': 4, 'z': 4}, 'computed': None}}


def test_master_g():
    assert g.report(verbose=True) == {'name': 'g', 'global_weight': 0.1333, 'local_weight': 0.3333,
                                      'target_weights': None,
                                      'elements': {'global_weights': {'z': 0.0666, 'y': 0.0444, 'x': 0.0222},
                                                   'local_weights': {'z': 0.5, 'y': 0.3333, 'x': 0.1667},
                                                   'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd',
                                                   'count': 3, 'names': ['x', 'y', 'z']}, 'children': None,
                                      'comparisons': {'count': 3, 'input': {'x': 1, 'y': 2, 'z': 3}, 'computed': None}}


# Example from https://en.wikipedia.org/wiki/Analytic_hierarchy_process_%E2%80%93_car_example

cri = ('Cost', 'Safety', 'Style', 'Capacity')
c_cri = list(itertools.combinations(cri, 2))

costs = ('Price', 'Fuel', 'Maintenance', 'Resale')
c_pairs = list(itertools.combinations(costs, 2))

alt = ('Accord Sedan', 'Accord Hybrid', 'Pilot', 'CR-V', 'Element', 'Odyssey')
pairs = list(itertools.combinations(alt, 2))

capacity_pass_m = (1, 1 / 2, 1, 3, 1 / 2, 1 / 2, 1, 3, 1 / 2, 2, 6, 1, 3, 1 / 2, 1 / 6)
capacity_cargo_m = (1, 1 / 2, 1 / 2, 1 / 2, 1 / 3, 1 / 2, 1 / 2, 1 / 2, 1 / 3, 1, 1, 1 / 2, 1, 1 / 2, 1 / 2)
cost_price_m = (9, 9, 1, 0.5, 5, 1, 1 / 9, 1 / 9, 1 / 7, 1 / 9, 1 / 9, 1 / 7, 1 / 2, 5, 6)
cost_fuel_m = (
    1 / 1.13, 1.41, 1.15, 1.24, 1.19, 1.59, 1.3, 1.4, 1.35, 1 / 1.23, 1 / 1.14, 1 / 1.18, 1.08, 1.04, 1 / 1.04)
cost_resale_m = (3, 4, 1 / 2, 2, 2, 2, 1 / 5, 1, 1, 1 / 6, 1 / 2, 1 / 2, 4, 4, 1)
cost_maint_m = (1.5, 4, 4, 4, 5, 4, 4, 4, 5, 1, 1.2, 1, 1, 3, 2)
safety_m = (1, 5, 7, 9, 1 / 3, 5, 7, 9, 1 / 3, 2, 9, 1 / 8, 2, 1 / 8, 1 / 9)
style_m = (1, 7, 5, 9, 6, 7, 5, 9, 6, 1 / 6, 3, 1 / 3, 7, 5, 1 / 5)

cost = ahpy.Compare('Cost', dict(zip(c_pairs, (2, 5, 3, 2, 2, .5))))
capacity = ahpy.Compare('Capacity', {('Cargo', 'Passenger'): 0.2})
capacity_cargo = ahpy.Compare('Cargo', dict(zip(pairs, capacity_cargo_m)))
safety = ahpy.Compare('Safety', dict(zip(pairs, safety_m)), 3)
style = ahpy.Compare('Style', dict(zip(pairs, style_m)), 3)

h = {'Criteria': ['Cost', 'Safety', 'Style', 'Capacity'],
     'Cost': ['Price', 'Fuel', 'Resale', 'Maintenance'],
     'Capacity': ['Passenger', 'Cargo']}

compose = ahpy.Compose()

compose.add_comparisons(capacity_cargo)
compose.add_comparisons([cost, capacity])
compose.add_comparisons((safety, style))

compose.add_comparisons('Criteria', dict(zip(c_cri, (3, 7, 3, 9, 1, 1 / 7))), 3)
compose.add_comparisons(('Passenger', dict(zip(pairs, capacity_pass_m))))

compose.add_comparisons([('Price', dict(zip(pairs, cost_price_m)), 3), ('Fuel', dict(zip(pairs, cost_fuel_m)), 3)])
compose.add_comparisons(
    (['Resale', dict(zip(pairs, cost_resale_m)), 3], ['Maintenance', dict(zip(pairs, cost_maint_m)), 3, 'saaty']))

compose.add_hierarchy(h)


def test_compose_target_weights_attr():
    assert compose.Criteria.target_weights == {'Odyssey': 0.219, 'Accord Sedan': 0.215, 'CR-V': 0.167,
                                               'Accord Hybrid': 0.15, 'Element': 0.144, 'Pilot': 0.106}


def test_compose_item():
    assert compose['Price']['local_weights'] == {'Element': 0.366, 'Accord Sedan': 0.246, 'CR-V': 0.246,
                                                 'Odyssey': 0.093, 'Accord Hybrid': 0.025, 'Pilot': 0.025}


def test_compose_verbose_report():
    assert compose.report(verbose=True) == {'Criteria': {'name': 'Criteria', 'global_weight': 1.0, 'local_weight': 1.0,
                                                         'target_weights': {'Odyssey': 0.219, 'Accord Sedan': 0.215,
                                                                            'CR-V': 0.167, 'Accord Hybrid': 0.15,
                                                                            'Element': 0.144, 'Pilot': 0.106},
                                                         'elements': {'global_weights': {'Cost': 0.51, 'Safety': 0.234,
                                                                                         'Capacity': 0.215,
                                                                                         'Style': 0.041},
                                                                      'local_weights': {'Cost': 0.51, 'Safety': 0.234,
                                                                                        'Capacity': 0.215,
                                                                                        'Style': 0.041},
                                                                      'consistency_ratio': 0.08,
                                                                      'random_index': 'Donegan & Dodd', 'count': 4,
                                                                      'names': ['Cost', 'Safety', 'Style', 'Capacity']},
                                                         'children': {'count': 4,
                                                                      'names': ['Cost', 'Safety', 'Style', 'Capacity']},
                                                         'comparisons': {'count': 6,
                                                                         'input': pytest.approx({('Cost', 'Safety'): 3,
                                                                                                 ('Cost', 'Style'): 7,
                                                                                                 (
                                                                                                     'Cost',
                                                                                                     'Capacity'): 3,
                                                                                                 ('Safety', 'Style'): 9,
                                                                                                 (
                                                                                                     'Safety',
                                                                                                     'Capacity'): 1,
                                                                                                 ('Style',
                                                                                                  'Capacity'): 0.14285714285714285}),
                                                                         'computed': None}},
                                            'Cost': {'name': 'Cost', 'global_weight': 0.51, 'local_weight': 0.51,
                                                     'target_weights': None, 'elements': {
                                                    'global_weights': {'Price': 0.2489, 'Fuel': 0.1283,
                                                                       'Resale': 0.0819, 'Maintenance': 0.0509},
                                                    'local_weights': {'Price': 0.4881, 'Fuel': 0.2515, 'Resale': 0.1605,
                                                                      'Maintenance': 0.0999},
                                                    'consistency_ratio': 0.0164, 'random_index': 'Donegan & Dodd',
                                                    'count': 4, 'names': ['Price', 'Fuel', 'Maintenance', 'Resale']},
                                                     'children': {'count': 4,
                                                                  'names': ['Price', 'Fuel', 'Resale', 'Maintenance']},
                                                     'comparisons': {'count': 6, 'input': {('Price', 'Fuel'): 2,
                                                                                           ('Price', 'Maintenance'): 5,
                                                                                           ('Price', 'Resale'): 3,
                                                                                           ('Fuel', 'Maintenance'): 2,
                                                                                           ('Fuel', 'Resale'): 2, (
                                                                                               'Maintenance',
                                                                                               'Resale'): 0.5},
                                                                     'computed': None}},
                                            'Price': {'name': 'Price', 'global_weight': 0.2489, 'local_weight': 0.4881,
                                                      'target_weights': None, 'elements': {
                                                    'global_weights': {'Element': 0.091, 'Accord Sedan': 0.061,
                                                                       'CR-V': 0.061, 'Odyssey': 0.023,
                                                                       'Accord Hybrid': 0.006, 'Pilot': 0.006},
                                                    'local_weights': {'Element': 0.366, 'Accord Sedan': 0.246,
                                                                      'CR-V': 0.246, 'Odyssey': 0.093,
                                                                      'Accord Hybrid': 0.025, 'Pilot': 0.025},
                                                    'consistency_ratio': 0.072, 'random_index': 'Donegan & Dodd',
                                                    'count': 6,
                                                    'names': ['Accord Sedan', 'Accord Hybrid', 'Pilot', 'CR-V',
                                                              'Element', 'Odyssey']}, 'children': None,
                                                      'comparisons': {'count': 15,
                                                                      'input': pytest.approx(
                                                                          {('Accord Sedan', 'Accord Hybrid'): 9,
                                                                           ('Accord Sedan', 'Pilot'): 9,
                                                                           ('Accord Sedan', 'CR-V'): 1,
                                                                           ('Accord Sedan', 'Element'): 0.5,
                                                                           ('Accord Sedan', 'Odyssey'): 5,
                                                                           ('Accord Hybrid', 'Pilot'): 1, (
                                                                               'Accord Hybrid',
                                                                               'CR-V'): 0.1111111111111111, (
                                                                               'Accord Hybrid',
                                                                               'Element'): 0.1111111111111111, (
                                                                               'Accord Hybrid',
                                                                               'Odyssey'): 0.14285714285714285,
                                                                           ('Pilot', 'CR-V'): 0.1111111111111111, (
                                                                               'Pilot', 'Element'): 0.1111111111111111,
                                                                           ('Pilot',
                                                                            'Odyssey'): 0.14285714285714285,
                                                                           ('CR-V', 'Element'): 0.5,
                                                                           ('CR-V', 'Odyssey'): 5,
                                                                           ('Element', 'Odyssey'): 6}),
                                                                      'computed': None}},
                                            'Fuel': {'name': 'Fuel', 'global_weight': 0.1283, 'local_weight': 0.2515,
                                                     'target_weights': None, 'elements': {
                                                    'global_weights': {'Accord Hybrid': 0.027, 'Accord Sedan': 0.024,
                                                                       'CR-V': 0.021, 'Odyssey': 0.02, 'Element': 0.019,
                                                                       'Pilot': 0.017},
                                                    'local_weights': {'Accord Hybrid': 0.211, 'Accord Sedan': 0.187,
                                                                      'CR-V': 0.163, 'Odyssey': 0.157, 'Element': 0.151,
                                                                      'Pilot': 0.132}, 'consistency_ratio': 0.0,
                                                    'random_index': 'Donegan & Dodd', 'count': 6,
                                                    'names': ['Accord Sedan', 'Accord Hybrid', 'Pilot', 'CR-V',
                                                              'Element', 'Odyssey']}, 'children': None,
                                                     'comparisons': {'count': 15, 'input': pytest.approx({
                                                         ('Accord Sedan', 'Accord Hybrid'): 0.8849557522123894,
                                                         ('Accord Sedan', 'Pilot'): 1.41,
                                                         ('Accord Sedan', 'CR-V'): 1.15,
                                                         ('Accord Sedan', 'Element'): 1.24,
                                                         ('Accord Sedan', 'Odyssey'): 1.19,
                                                         ('Accord Hybrid', 'Pilot'): 1.59,
                                                         ('Accord Hybrid', 'CR-V'): 1.3,
                                                         ('Accord Hybrid', 'Element'): 1.4,
                                                         ('Accord Hybrid', 'Odyssey'): 1.35,
                                                         ('Pilot', 'CR-V'): 0.8130081300813008,
                                                         ('Pilot', 'Element'): 0.8771929824561404,
                                                         ('Pilot', 'Odyssey'): 0.8474576271186441,
                                                         ('CR-V', 'Element'): 1.08, ('CR-V', 'Odyssey'): 1.04,
                                                         ('Element', 'Odyssey'): 0.9615384615384615}),
                                                                     'computed': None}},
                                            'Resale': {'name': 'Resale', 'global_weight': 0.0819,
                                                       'local_weight': 0.1605, 'target_weights': None, 'elements': {
                                                    'global_weights': {'CR-V': 0.034, 'Accord Sedan': 0.018,
                                                                       'Element': 0.009, 'Odyssey': 0.009,
                                                                       'Accord Hybrid': 0.008, 'Pilot': 0.005},
                                                    'local_weights': {'CR-V': 0.416, 'Accord Sedan': 0.225,
                                                                      'Element': 0.105, 'Odyssey': 0.105,
                                                                      'Accord Hybrid': 0.095, 'Pilot': 0.055},
                                                    'consistency_ratio': 0.005, 'random_index': 'Donegan & Dodd',
                                                    'count': 6,
                                                    'names': ['Accord Sedan', 'Accord Hybrid', 'Pilot', 'CR-V',
                                                              'Element', 'Odyssey']}, 'children': None,
                                                       'comparisons': {'count': 15,
                                                                       'input': pytest.approx(
                                                                           {('Accord Sedan', 'Accord Hybrid'): 3,
                                                                            ('Accord Sedan', 'Pilot'): 4,
                                                                            ('Accord Sedan', 'CR-V'): 0.5,
                                                                            ('Accord Sedan', 'Element'): 2,
                                                                            ('Accord Sedan', 'Odyssey'): 2,
                                                                            ('Accord Hybrid', 'Pilot'): 2,
                                                                            ('Accord Hybrid', 'CR-V'): 0.2,
                                                                            ('Accord Hybrid', 'Element'): 1,
                                                                            ('Accord Hybrid', 'Odyssey'): 1,
                                                                            ('Pilot', 'CR-V'): 0.16666666666666666,
                                                                            ('Pilot', 'Element'): 0.5,
                                                                            ('Pilot', 'Odyssey'): 0.5,
                                                                            ('CR-V', 'Element'): 4,
                                                                            ('CR-V', 'Odyssey'): 4,
                                                                            ('Element', 'Odyssey'): 1}),
                                                                       'computed': None}},
                                            'Maintenance': {'name': 'Maintenance', 'global_weight': 0.0509,
                                                            'local_weight': 0.0999, 'target_weights': None,
                                                            'elements': {'global_weights': {'Accord Sedan': 0.018,
                                                                                            'Accord Hybrid': 0.016,
                                                                                            'CR-V': 0.005,
                                                                                            'Element': 0.004,
                                                                                            'Pilot': 0.004,
                                                                                            'Odyssey': 0.003},
                                                                         'local_weights': {'Accord Sedan': 0.358,
                                                                                           'Accord Hybrid': 0.313,
                                                                                           'CR-V': 0.1,
                                                                                           'Element': 0.088,
                                                                                           'Pilot': 0.084,
                                                                                           'Odyssey': 0.057},
                                                                         'consistency_ratio': 0.023,
                                                                         'random_index': 'Saaty', 'count': 6,
                                                                         'names': ['Accord Sedan', 'Accord Hybrid',
                                                                                   'Pilot', 'CR-V', 'Element',
                                                                                   'Odyssey']}, 'children': None,
                                                            'comparisons': {'count': 15, 'input': {
                                                                ('Accord Sedan', 'Accord Hybrid'): 1.5,
                                                                ('Accord Sedan', 'Pilot'): 4,
                                                                ('Accord Sedan', 'CR-V'): 4,
                                                                ('Accord Sedan', 'Element'): 4,
                                                                ('Accord Sedan', 'Odyssey'): 5,
                                                                ('Accord Hybrid', 'Pilot'): 4,
                                                                ('Accord Hybrid', 'CR-V'): 4,
                                                                ('Accord Hybrid', 'Element'): 4,
                                                                ('Accord Hybrid', 'Odyssey'): 5, ('Pilot', 'CR-V'): 1,
                                                                ('Pilot', 'Element'): 1.2, ('Pilot', 'Odyssey'): 1,
                                                                ('CR-V', 'Element'): 1, ('CR-V', 'Odyssey'): 3,
                                                                ('Element', 'Odyssey'): 2}, 'computed': None}},
                                            'Safety': {'name': 'Safety', 'global_weight': 0.234, 'local_weight': 0.234,
                                                       'target_weights': None, 'elements': {
                                                    'global_weights': {'Odyssey': 0.102, 'Accord Sedan': 0.051,
                                                                       'Accord Hybrid': 0.051, 'Pilot': 0.018,
                                                                       'CR-V': 0.008, 'Element': 0.005},
                                                    'local_weights': {'Odyssey': 0.434, 'Accord Sedan': 0.216,
                                                                      'Accord Hybrid': 0.216, 'Pilot': 0.075,
                                                                      'CR-V': 0.036, 'Element': 0.022},
                                                    'consistency_ratio': 0.085, 'random_index': 'Donegan & Dodd',
                                                    'count': 6,
                                                    'names': ['Accord Sedan', 'Accord Hybrid', 'Pilot', 'CR-V',
                                                              'Element', 'Odyssey']}, 'children': None,
                                                       'comparisons': {'count': 15,
                                                                       'input': pytest.approx(
                                                                           {('Accord Sedan', 'Accord Hybrid'): 1,
                                                                            ('Accord Sedan', 'Pilot'): 5,
                                                                            ('Accord Sedan', 'CR-V'): 7,
                                                                            ('Accord Sedan', 'Element'): 9, (
                                                                                'Accord Sedan',
                                                                                'Odyssey'): 0.3333333333333333,
                                                                            ('Accord Hybrid', 'Pilot'): 5,
                                                                            ('Accord Hybrid', 'CR-V'): 7,
                                                                            ('Accord Hybrid', 'Element'): 9, (
                                                                                'Accord Hybrid',
                                                                                'Odyssey'): 0.3333333333333333,
                                                                            ('Pilot', 'CR-V'): 2,
                                                                            ('Pilot', 'Element'): 9,
                                                                            ('Pilot', 'Odyssey'): 0.125,
                                                                            ('CR-V', 'Element'): 2,
                                                                            ('CR-V', 'Odyssey'): 0.125, ('Element',
                                                                                                         'Odyssey'): 0.1111111111111111}),
                                                                       'computed': None}},
                                            'Style': {'name': 'Style', 'global_weight': 0.041, 'local_weight': 0.041,
                                                      'target_weights': None, 'elements': {
                                                    'global_weights': {'Accord Sedan': 0.015, 'Accord Hybrid': 0.015,
                                                                       'CR-V': 0.006, 'Odyssey': 0.003, 'Pilot': 0.002,
                                                                       'Element': 0.001},
                                                    'local_weights': {'Accord Sedan': 0.358, 'Accord Hybrid': 0.358,
                                                                      'CR-V': 0.155, 'Odyssey': 0.068, 'Pilot': 0.039,
                                                                      'Element': 0.023}, 'consistency_ratio': 0.107,
                                                    'random_index': 'Donegan & Dodd', 'count': 6,
                                                    'names': ['Accord Sedan', 'Accord Hybrid', 'Pilot', 'CR-V',
                                                              'Element', 'Odyssey']}, 'children': None,
                                                      'comparisons': {'count': 15,
                                                                      'input': pytest.approx(
                                                                          {('Accord Sedan', 'Accord Hybrid'): 1,
                                                                           ('Accord Sedan', 'Pilot'): 7,
                                                                           ('Accord Sedan', 'CR-V'): 5,
                                                                           ('Accord Sedan', 'Element'): 9,
                                                                           ('Accord Sedan', 'Odyssey'): 6,
                                                                           ('Accord Hybrid', 'Pilot'): 7,
                                                                           ('Accord Hybrid', 'CR-V'): 5,
                                                                           ('Accord Hybrid', 'Element'): 9,
                                                                           ('Accord Hybrid', 'Odyssey'): 6,
                                                                           ('Pilot', 'CR-V'): 0.16666666666666666,
                                                                           ('Pilot', 'Element'): 3, (
                                                                               'Pilot', 'Odyssey'): 0.3333333333333333,
                                                                           ('CR-V', 'Element'): 7,
                                                                           ('CR-V', 'Odyssey'): 5,
                                                                           ('Element', 'Odyssey'): 0.2}),
                                                                      'computed': None}},
                                            'Capacity': {'name': 'Capacity', 'global_weight': 0.215,
                                                         'local_weight': 0.215, 'target_weights': None, 'elements': {
                                                    'global_weights': {'Passenger': 0.1792, 'Cargo': 0.0358},
                                                    'local_weights': {'Passenger': 0.8333, 'Cargo': 0.1667},
                                                    'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd',
                                                    'count': 2, 'names': ['Cargo', 'Passenger']},
                                                         'children': {'count': 2, 'names': ['Passenger', 'Cargo']},
                                                         'comparisons': {'count': 1,
                                                                         'input': {('Cargo', 'Passenger'): 0.2},
                                                                         'computed': None}},
                                            'Passenger': {'name': 'Passenger', 'global_weight': 0.1792,
                                                          'local_weight': 0.8333, 'target_weights': None, 'elements': {
                                                    'global_weights': {'Pilot': 0.0489, 'Odyssey': 0.0489,
                                                                       'Accord Sedan': 0.0244, 'Accord Hybrid': 0.0244,
                                                                       'CR-V': 0.0244, 'Element': 0.0082},
                                                    'local_weights': {'Pilot': 0.2727, 'Odyssey': 0.2727,
                                                                      'Accord Sedan': 0.1364, 'Accord Hybrid': 0.1364,
                                                                      'CR-V': 0.1364, 'Element': 0.0455},
                                                    'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd',
                                                    'count': 6,
                                                    'names': ['Accord Sedan', 'Accord Hybrid', 'Pilot', 'CR-V',
                                                              'Element', 'Odyssey']}, 'children': None,
                                                          'comparisons': {'count': 15, 'input': pytest.approx({
                                                              ('Accord Sedan', 'Accord Hybrid'): 1,
                                                              ('Accord Sedan', 'Pilot'): 0.5,
                                                              ('Accord Sedan', 'CR-V'): 1,
                                                              ('Accord Sedan', 'Element'): 3,
                                                              ('Accord Sedan', 'Odyssey'): 0.5,
                                                              ('Accord Hybrid', 'Pilot'): 0.5,
                                                              ('Accord Hybrid', 'CR-V'): 1,
                                                              ('Accord Hybrid', 'Element'): 3,
                                                              ('Accord Hybrid', 'Odyssey'): 0.5, ('Pilot', 'CR-V'): 2,
                                                              ('Pilot', 'Element'): 6, ('Pilot', 'Odyssey'): 1,
                                                              ('CR-V', 'Element'): 3, ('CR-V', 'Odyssey'): 0.5,
                                                              ('Element', 'Odyssey'): 0.16666666666666666}),
                                                                          'computed': None}},
                                            'Cargo': {'name': 'Cargo', 'global_weight': 0.0358, 'local_weight': 0.1667,
                                                      'target_weights': None, 'elements': {
                                                    'global_weights': {'Odyssey': 0.0111, 'Pilot': 0.0061,
                                                                       'CR-V': 0.0061, 'Element': 0.0061,
                                                                       'Accord Sedan': 0.0032, 'Accord Hybrid': 0.0032},
                                                    'local_weights': {'Odyssey': 0.3106, 'Pilot': 0.1702,
                                                                      'CR-V': 0.1702, 'Element': 0.1702,
                                                                      'Accord Sedan': 0.0894, 'Accord Hybrid': 0.0894},
                                                    'consistency_ratio': 0.0023, 'random_index': 'Donegan & Dodd',
                                                    'count': 6,
                                                    'names': ['Accord Sedan', 'Accord Hybrid', 'Pilot', 'CR-V',
                                                              'Element', 'Odyssey']}, 'children': None,
                                                      'comparisons': {'count': 15,
                                                                      'input': pytest.approx(
                                                                          {('Accord Sedan', 'Accord Hybrid'): 1,
                                                                           ('Accord Sedan', 'Pilot'): 0.5,
                                                                           ('Accord Sedan', 'CR-V'): 0.5,
                                                                           ('Accord Sedan', 'Element'): 0.5, (
                                                                               'Accord Sedan',
                                                                               'Odyssey'): 0.3333333333333333,
                                                                           ('Accord Hybrid', 'Pilot'): 0.5,
                                                                           ('Accord Hybrid', 'CR-V'): 0.5,
                                                                           ('Accord Hybrid', 'Element'): 0.5, (
                                                                               'Accord Hybrid',
                                                                               'Odyssey'): 0.3333333333333333,
                                                                           ('Pilot', 'CR-V'): 1,
                                                                           ('Pilot', 'Element'): 1,
                                                                           ('Pilot', 'Odyssey'): 0.5,
                                                                           ('CR-V', 'Element'): 1,
                                                                           ('CR-V', 'Odyssey'): 0.5,
                                                                           ('Element', 'Odyssey'): 0.5}),
                                                                      'computed': None}}}
