import itertools
import pytest

from ahpy import ahpy

# Example from https://en.wikipedia.org/wiki/Analytic_hierarchy_process_%E2%80%93_leader_example

# experience_comparisons = {('Moll', 'Nell'): 1 / 4, ('Moll', 'Sue'): 4, ('Nell', 'Sue'): 9}
# education_comparisons = {('Moll', 'Nell'): 3, ('Moll', 'Sue'): 1 / 5, ('Nell', 'Sue'): 1 / 7}
# charisma_comparisons = {('Moll', 'Nell'): 5, ('Moll', 'Sue'): 9, ('Nell', 'Sue'): 4}
# age_comparisons = {('Moll', 'Nell'): 1 / 3, ('Moll', 'Sue'): 5, ('Nell', 'Sue'): 9}
# criteria_comparisons = {('Experience', 'Education'): 4, ('Experience', 'Charisma'): 3, ('Experience', 'Age'): 7,
#                         ('Education', 'Charisma'): 1 / 3, ('Education', 'Age'): 3,
#                         ('Charisma', 'Age'): 5}
#
# experience = ahpy.Compare('Experience', experience_comparisons, precision=3, random_index='saaty')
# education = ahpy.Compare('Education', education_comparisons, precision=3, random_index='saaty')
# charisma = ahpy.Compare('Charisma', charisma_comparisons, precision=3, random_index='saaty')
# age = ahpy.Compare('Age', age_comparisons, precision=3, random_index='saaty')
# criteria = ahpy.Compare('Criteria', criteria_comparisons, precision=3, random_index='saaty')
#
# criteria.add_children([experience, education, charisma, age])

# ----------------------------------------------------------------------------------
# Example from Saaty, Thomas L., 'Decision making with the analytic hierarchy process,'
# Int. J. Services Sciences, 1:1, 2008, pp. 83-98.

# drinks_m = {('coffee', 'wine'): 9, ('coffee', 'tea'): 5, ('coffee', 'beer'): 2, ('coffee', 'soda'): 1,
#           ('coffee', 'milk'): 1, ('water', 'coffee'): 2, ('tea', 'wine'): 3, ('beer', 'wine'): 9, ('beer', 'tea'): 3,
#           ('beer', 'milk'): 1, ('soda', 'wine'): 9, ('soda', 'tea'): 4, ('soda', 'beer'): 2, ('soda', 'milk'): 2,
#           ('milk', 'wine'): 9, ('milk', 'tea'): 3, ('water', 'coffee'): 2, ('water', 'wine'): 9, ('water', 'tea'): 9,
#           ('water', 'beer'): 3, ('water', 'soda'): 2, ('water', 'milk'): 3}
# drinks = ahpy.Compare('Drinks', drinks_m, precision=3, random_index='saaty')

# drinks_missing = {('coffee', 'wine'): 9, ('coffee', 'tea'): 5, ('coffee', 'beer'): 2,
#             ('coffee', 'milk'): 1,
#             ('wine', 'tea'): 1 / 3, ('wine', 'beer'): 1 / 9,
#             ('wine', 'milk'): 1 / 9,
#             ('tea', 'beer'): 1 / 3, ('tea', 'soda'): 1 / 4,
#             ('tea', 'water'): 1 / 9,
#             ('beer', 'soda'): 1 / 2, ('beer', 'milk'): 1,
#             ('soda', 'milk'): 2,
#             ('milk', 'water'): 1 / 3
#           }
# drinks_missing = ahpy.Compare('Drinks', drinks_missing, precision=3, random_index='saaty')

# ----------------------------------------------------------------------------------
# Example from https://mi.boku.ac.at/ahp/ahptutorial.pdf

# cars = ('civic', 'saturn', 'escort', 'clio')
#
# gas_m = dict(zip(cars, (34, 27, 24, 28)))
# gas = ahpy.Compare('gas', gas_m, precision=3)
#
# rel_m = dict(zip(itertools.combinations(cars, 2), (2, 5, 1, 3, 2, 0.25)))
# rel = ahpy.Compare('rel', rel_m, 3)
#
# style_m = {('civic', 'escort'): 4,
#            ('saturn', 'civic'): 4, ('saturn', 'escort'): 4, ('saturn', 'clio'): 0.25,
#            ('clio', 'civic'): 6, ('clio', 'escort'): 5}
# style = ahpy.Compare('style', style_m, precision=3)
#
# cri_m = {('style', 'rel'): 0.5, ('style', 'gas'): 3,
#          ('rel', 'gas'): 4}
# goal = ahpy.Compare('goal', cri_m)
#
# goal.add_children([gas, rel, style])

# ----------------------------------------------------------------------------------
# Example from Saaty, Thomas, L., Theory and Applications of the Analytic Network Process, 2005.
# Also at https://www.passagetechnology.com/what-is-the-analytic-hierarchy-process

# criteria = {('Culture', 'Housing'): 3, ('Culture', 'Transportation'): 5,
#             ('Family', 'Culture'): 5, ('Family', 'Housing'): 7, ('Family', 'Transportation'): 7,
#             ('Housing', 'Transportation'): 3,
#             ('Jobs', 'Culture'): 2, ('Jobs', 'Housing'): 4, ('Jobs', 'Transportation'): 7,
#             ('Family', 'Jobs'): 1}
#
# culture = {('Bethesda', 'Pittsburgh'): 1,
#            ('Boston', 'Bethesda'): 2, ('Boston', 'Pittsburgh'): 2.5, ('Boston', 'Santa Fe'): 1,
#            ('Pittsburgh', 'Bethesda'): 1,
#            ('Santa Fe', 'Bethesda'): 2, ('Santa Fe', 'Pittsburgh'): 2.5}
#
# family = {('Bethesda', 'Boston'): 2, ('Bethesda', 'Santa Fe'): 4,
#           ('Boston', 'Santa Fe'): 2,
#           ('Pittsburgh', 'Bethesda'): 3, ('Pittsburgh', 'Boston'): 8, ('Pittsburgh', 'Santa Fe'): 9}
#
# housing = {('Bethesda', 'Boston'): 5, ('Bethesda', 'Santa Fe'): 2.5,
#            ('Pittsburgh', 'Bethesda'): 2, ('Pittsburgh', 'Boston'): 9, ('Pittsburgh', 'Santa Fe'): 7,
#            ('Santa Fe', 'Boston'): 4}
#
# jobs = {('Bethesda', 'Pittsburgh'): 3, ('Bethesda', 'Santa Fe'): 4,
#         ('Boston', 'Bethesda'): 2, ('Boston', 'Pittsburgh'): 6, ('Boston', 'Santa Fe'): 8,
#         ('Pittsburgh', 'Santa Fe'): 1}
#
# transportation = {('Bethesda', 'Boston'): 1.5,
#                   ('Bethesda', 'Santa Fe'): 4,
#                   ('Boston', 'Santa Fe'): 2.5,
#                   ('Pittsburgh', 'Bethesda'): 2,
#                   ('Pittsburgh', 'Boston'): 3.5,
#                   ('Pittsburgh', 'Santa Fe'): 9}
#
# cu = ahpy.Compare('Culture', culture, precision=3, random_index='Saaty')
# f = ahpy.Compare('Family', family, precision=3, random_index='Saaty')
# h = ahpy.Compare('Housing', housing, precision=3, random_index='Saaty')
# j = ahpy.Compare('Jobs', jobs, precision=3, random_index='Saaty')
# t = ahpy.Compare('Transportation', transportation, precision=3, random_index='Saaty')
# cr = ahpy.Compare('Goal', criteria, precision=3, random_index='Saaty')
# cr.add_children([cu, f, h, j, t])

# ----------------------------------------------------------------------------------
# Example from https://en.wikipedia.org/wiki/Analytic_hierarchy_process_%E2%80%93_car_example


# def m(elements, judgments):
#     return dict(zip(elements, judgments))
#
#
# cri = ('Cost', 'Safety', 'Style', 'Capacity')
# c_cri = list(itertools.combinations(cri, 2))
# criteria = ahpy.Compare('Criteria', m(c_cri, (3, 7, 3, 9, 1, 1 / 7)), 3)
#
# alt = ('Accord Sedan', 'Accord Hybrid', 'Pilot', 'CR-V', 'Element', 'Odyssey')
# pairs = list(itertools.combinations(alt, 2))
#
# costs = ('Price', 'Fuel', 'Maintenance', 'Resale')
# c_pairs = list(itertools.combinations(costs, 2))
# cost = ahpy.Compare('Cost', m(c_pairs, (2, 5, 3, 2, 2, .5)), precision=3)
#
# cost_price_m = (9, 9, 1, 0.5, 5, 1, 1 / 9, 1 / 9, 1 / 7, 1 / 9, 1 / 9, 1 / 7, 1 / 2, 5, 6)
# cost_price = ahpy.Compare('Price', m(pairs, cost_price_m), 3)
#
# # cost_fuel_m = (1/1.13, 1.41, 1.15, 1.24, 1.19, 1.59, 1.3, 1.4, 1.35, 1/1.23, 1/1.14, 1/1.18, 1.08, 1.04, 1/1.04)
# cost_fuel_m = (31, 35, 22, 27, 25, 26)
# # cost_fuel = ahpy.Compare('Fuel', m(pairs, cost_fuel_m), 3)
# cost_fuel = ahpy.Compare('Fuel', m(alt, cost_fuel_m), 3)
#
# # cost_resale_m = (3, 4, 1 / 2, 2, 2, 2, 1 / 5, 1, 1, 1 / 6, 1 / 2, 1 / 2, 4, 4, 1)
# cost_resale_m = (0.52, 0.46, 0.44, 0.55, 0.48, 0.48)
# # cost_resale = ahpy.Compare('Resale', m(pairs, cost_resale_m), 3)
# cost_resale = ahpy.Compare('Resale', m(alt, cost_resale_m), 3)
#
# cost_maint_m = (1.5, 4, 4, 4, 5, 4, 4, 4, 5, 1, 1.2, 1, 1, 3, 2)
# cost_maint = ahpy.Compare('Maintenance', m(pairs, cost_maint_m), 3)
#
# safety_m = (1, 5, 7, 9, 1 / 3, 5, 7, 9, 1 / 3, 2, 9, 1 / 8, 2, 1 / 8, 1 / 9)
# safety = ahpy.Compare('Safety', m(pairs, safety_m), 3)
#
# style_m = (1, 7, 5, 9, 6, 7, 5, 9, 6, 1 / 6, 3, 1 / 3, 7, 5, 1 / 5)
# style = ahpy.Compare('Style', m(pairs, style_m), 3)
#
# capacity = ahpy.Compare('Capacity', {('Cargo', 'Passenger'): 0.2})
#
# # capacity_pass_m = (1, 1 / 2, 1, 3, 1 / 2, 1 / 2, 1, 3, 1 / 2, 2, 6, 1, 3, 1 / 2, 1 / 6)
# capacity_pass_m = (5, 5, 8, 5, 4, 8)
# # capacity_pass = ahpy.Compare('Passenger', m(pairs, capacity_pass_m), 3)
# capacity_pass = ahpy.Compare('Passenger', m(alt, capacity_pass_m), 3)
#
# # capacity_cargo_m = (1, 1 / 2, 1 / 2, 1 / 2, 1 / 3, 1 / 2, 1 / 2, 1 / 2, 1 / 3, 1, 1, 1 / 2, 1, 1 / 2, 1 / 2)
# capacity_cargo_m = (14, 14, 87.6, 72.9, 74.6, 147.4)
# # capacity_cargo = ahpy.Compare('Cargo', m(pairs, capacity_cargo_m), precision=3)
# capacity_cargo = ahpy.Compare('Cargo', m(alt, capacity_cargo_m), precision=3)
#
# cost.add_children([cost_price, cost_fuel, cost_maint, cost_resale])
# capacity.add_children([capacity_cargo, capacity_pass])
# criteria.add_children([cost, safety, style, capacity])
#
# compose = ahpy.Compose()
# compose.add_comparisons('Criteria', m(c_cri, (3, 7, 3, 9, 1, 1 / 7)), 3)
# compose.add_comparisons([cost, capacity])
# compose.add_comparisons('Passenger', m(pairs, capacity_pass_m), 3)
# compose.add_comparisons([capacity_cargo, cost_price, cost_fuel, cost_resale, cost_maint])
# # a.add_comparisons([('Price', m(pairs, cost_price_m), 3), ('Fuel', m(pairs, cost_fuel_m), 3)])
# # a.add_comparisons([['Resale', m(pairs, cost_resale_m), 3], ['Maintenance', m(pairs, cost_maint_m), 3, 'saaty']])
# compose.add_comparisons((safety, style))
# h = {'Criteria': ['Cost', 'Safety', 'Style', 'Capacity'],
#      'Cost': ['Price', 'Fuel', 'Resale', 'Maintenance'],
#      'Capacity': ['Passenger', 'Cargo']}
# compose.add_hierarchy(h)

# ----------------------------------------------------------------------------------
# Examples from Bozóki, S., Fülöp, J. and Rónyai, L., 'On optimal completion of incomplete pairwise comparison matrices,'
# Mathematical and Computer Modelling, 52:1–2, 2010, pp. 318-333. (https://doi.org/10.1016/j.mcm.2010.02.047)

# u = {('alpha', 'beta'): 1, ('alpha', 'chi'): 5, ('alpha', 'delta'): 2,
#      ('beta', 'chi'): 3, ('beta', 'delta'): 4}  # , ('chi', 'delta'): 3/4}
# cu = ahpy.Compare('Incomplete Test', u)
#
# m = {('a', 'b'): 5, ('a', 'c'): 3, ('a', 'd'): 7, ('a', 'e'): 6, ('a', 'f'): 6,
#      ('b', 'd'): 5, ('b', 'f'): 3,
#      ('c', 'e'): 3, ('c', 'g'): 6,
#      ('f', 'd'): 4,
#      ('g', 'a'): 3, ('g', 'e'): 5,
#      ('h', 'a'): 4, ('h', 'b'): 7, ('h', 'd'): 8, ('h', 'f'): 6}
#
# cm = ahpy.Compare('Incomplete Housing', m)

# ----------------------------------------------------------------------------------
# Example from Haas, R. and Meixner, L., 'An Illustrated Guide to the Analytic Hierarchy Process,'
# http://www.inbest.co.il/NGO/ahptutorial.pdf

# f = {'civic': 34, 'saturn': 27, 'escort': 24, 'clio': 28}
# cf = ahpy.Compare('Fuel Economy', f)

# ----------------------------------------------------------------------------------
# Master Test

# a_m = {('b', 'c'): 1}
# b_m = {('d', 'e'): 4}
# c_m = {('f', 'g'): 1, ('g', 'h'): 1/2}
# d_m = {('i', 'j'): 2}
# e_m = {'x': 1, 'y': 2, 'z': 3}
# f_m = {('k', 'l'): 1/9}
# g_m = {'x': 1, 'y': 3, 'z': 6}
# h_m = {'x': 2, 'y': 4, 'z': 4}
# i_m = {'x': 2, 'y': 4, 'z': 4}
# j_m = {'x': 1, 'y': 2, 'z': 3}
# k_m = {'x': 2, 'y': 4, 'z': 4}
# l_m = {('m', 'n'): 1}
# m_m = {'x': 1, 'y': 2, 'z': 3}
# n_m = {'x': 1, 'y': 3, 'z': 6}
#
# a = ahpy.Compare('a', a_m, precision=4)
# b = ahpy.Compare('b', b_m, precision=4)
# c = ahpy.Compare('c', c_m, precision=4)
# d = ahpy.Compare('d', d_m, precision=4)
# e = ahpy.Compare('e', e_m, precision=4)
# f = ahpy.Compare('f', f_m, precision=4)
# g = ahpy.Compare('g', g_m, precision=4)
# h = ahpy.Compare('h', h_m, precision=4)
# i = ahpy.Compare('i', i_m, precision=4)
# j = ahpy.Compare('j', j_m, precision=4)
# k = ahpy.Compare('k', k_m, precision=4)
# l = ahpy.Compare('l', l_m, precision=4)
# m = ahpy.Compare('m', m_m, precision=4)
# n = ahpy.Compare('n', n_m, precision=4)
#
# # l.add_children([m, n])
# # d.add_children([i, j])
# # f.add_children([l, k])
# # b.add_children([d, e])
# # c.add_children([h, f, g])
# # a.add_children([b, c])
#
# nodes = [(a, [b, c]), (b, [d, e]), (c, [f, g, h]), (d, [i, j]), (f, [k, l]), (l, [m, n])]
# permutations = itertools.permutations(nodes)
# for permutation in permutations:
#     for node in permutation:
#         node[0].add_children(node[1])
#
# h.report()
#
# assert a.report(verbose=True) == {'name': 'a', 'global_weight': 1.0, 'local_weight': 1.0, 'target_weights': {'z': 0.4652, 'y': 0.3626, 'x': 0.1723}, 'elements': {'global_weights': {'b': 0.5, 'c': 0.5}, 'local_weights': {'b': 0.5, 'c': 0.5}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'count': 2, 'names': ['b', 'c']}, 'children': {'count': 2, 'names': ['b', 'c']}, 'comparisons': {'count': 1, 'input': {('b', 'c'): 1}, 'computed': None}}
# assert b.report(verbose=True) == {'name': 'b', 'global_weight': 0.5, 'local_weight': 0.5, 'target_weights': None, 'elements': {'global_weights': {'d': 0.4, 'e': 0.1}, 'local_weights': {'d': 0.8, 'e': 0.2}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'count': 2, 'names': ['d', 'e']}, 'children': {'count': 2, 'names': ['d', 'e']}, 'comparisons': {'count': 1, 'input': {('d', 'e'): 4}, 'computed': None}}
# assert c.report(verbose=True) == {'name': 'c', 'global_weight': 0.5, 'local_weight': 0.5, 'target_weights': None, 'elements': {'global_weights': {'h': 0.25, 'f': 0.125, 'g': 0.125}, 'local_weights': {'h': 0.5, 'f': 0.25, 'g': 0.25}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'count': 3, 'names': ['f', 'g', 'h']}, 'children': {'count': 3, 'names': ['f', 'g', 'h']}, 'comparisons': {'count': 3, 'input': {('f', 'g'): 1, ('g', 'h'): 0.5}, 'computed': pytest.approx({('f', 'h'): 0.5000007807004769})}}
# assert d.report(verbose=True) == {'name': 'd', 'global_weight': 0.4, 'local_weight': 0.8, 'target_weights': None, 'elements': {'global_weights': {'i': 0.2667, 'j': 0.1333}, 'local_weights': {'i': 0.6667, 'j': 0.3333}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'count': 2, 'names': ['i', 'j']}, 'children': {'count': 2, 'names': ['i', 'j']}, 'comparisons': {'count': 1, 'input': {('i', 'j'): 2}, 'computed': None}}
# assert e.report(verbose=True) == {'name': 'e', 'global_weight': 0.1, 'local_weight': 0.2, 'target_weights': None, 'elements': {'global_weights': {'z': 0.05, 'y': 0.0333, 'x': 0.0167}, 'local_weights': {'z': 0.5, 'y': 0.3333, 'x': 0.1667}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'count': 3, 'names': ['x', 'y', 'z']}, 'children': None, 'comparisons': {'count': 3, 'input': {'x': 1, 'y': 2, 'z': 3}, 'computed': None}}
# assert f.report(verbose=True) == {'name': 'f', 'global_weight': 0.125, 'local_weight': 0.25, 'target_weights': None, 'elements': {'global_weights': {'l': 0.1125, 'k': 0.0125}, 'local_weights': {'l': 0.9, 'k': 0.1}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'count': 2, 'names': ['k', 'l']}, 'children': {'count': 2, 'names': ['k', 'l']}, 'comparisons': {'count': 1, 'input': {('k', 'l'): 0.1111111111111111}, 'computed': None}}
# assert g.report(verbose=True) == {'name': 'g', 'global_weight': 0.125, 'local_weight': 0.25, 'target_weights': None, 'elements': {'global_weights': {'z': 0.075, 'y': 0.0375, 'x': 0.0125}, 'local_weights': {'z': 0.6, 'y': 0.3, 'x': 0.1}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'count': 3, 'names': ['x', 'y', 'z']}, 'children': None, 'comparisons': {'count': 3, 'input': {'x': 1, 'y': 3, 'z': 6}, 'computed': None}}
# assert h.report(verbose=True) == {'name': 'h', 'global_weight': 0.25, 'local_weight': 0.5, 'target_weights': None, 'elements': {'global_weights': {'y': 0.1, 'z': 0.1, 'x': 0.05}, 'local_weights': {'y': 0.4, 'z': 0.4, 'x': 0.2}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'count': 3, 'names': ['x', 'y', 'z']}, 'children': None, 'comparisons': {'count': 3, 'input': {'x': 2, 'y': 4, 'z': 4}, 'computed': None}}
# assert i.report(verbose=True) == {'name': 'i', 'global_weight': 0.2667, 'local_weight': 0.6667, 'target_weights': None, 'elements': {'global_weights': {'y': 0.1067, 'z': 0.1067, 'x': 0.0533}, 'local_weights': {'y': 0.4, 'z': 0.4, 'x': 0.2}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'count': 3, 'names': ['x', 'y', 'z']}, 'children': None, 'comparisons': {'count': 3, 'input': {'x': 2, 'y': 4, 'z': 4}, 'computed': None}}
# assert j.report(verbose=True) == {'name': 'j', 'global_weight': 0.1333, 'local_weight': 0.3333, 'target_weights': None, 'elements': {'global_weights': {'z': 0.0666, 'y': 0.0444, 'x': 0.0222}, 'local_weights': {'z': 0.5, 'y': 0.3333, 'x': 0.1667}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'count': 3, 'names': ['x', 'y', 'z']}, 'children': None, 'comparisons': {'count': 3, 'input': {'x': 1, 'y': 2, 'z': 3}, 'computed': None}}
# assert k.report(verbose=True) == {'name': 'k', 'global_weight': 0.0125, 'local_weight': 0.1, 'target_weights': None, 'elements': {'global_weights': {'y': 0.005, 'z': 0.005, 'x': 0.0025}, 'local_weights': {'y': 0.4, 'z': 0.4, 'x': 0.2}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'count': 3, 'names': ['x', 'y', 'z']}, 'children': None, 'comparisons': {'count': 3, 'input': {'x': 2, 'y': 4, 'z': 4}, 'computed': None}}
# assert l.report(verbose=True) == {'name': 'l', 'global_weight': 0.1125, 'local_weight': 0.9, 'target_weights': None, 'elements': {'global_weights': {'m': 0.0562, 'n': 0.0562}, 'local_weights': {'m': 0.5, 'n': 0.5}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'count': 2, 'names': ['m', 'n']}, 'children': {'count': 2, 'names': ['m', 'n']}, 'comparisons': {'count': 1, 'input': {('m', 'n'): 1}, 'computed': None}}
# assert m.report(verbose=True) == {'name': 'm', 'global_weight': 0.0562, 'local_weight': 0.5, 'target_weights': None, 'elements': {'global_weights': {'z': 0.0281, 'y': 0.0187, 'x': 0.0094}, 'local_weights': {'z': 0.5, 'y': 0.3333, 'x': 0.1667}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'count': 3, 'names': ['x', 'y', 'z']}, 'children': None, 'comparisons': {'count': 3, 'input': {'x': 1, 'y': 2, 'z': 3}, 'computed': None}}
# assert n.report(verbose=True) == {'name': 'n', 'global_weight': 0.0562, 'local_weight': 0.5, 'target_weights': None, 'elements': {'global_weights': {'z': 0.0337, 'y': 0.0169, 'x': 0.0056}, 'local_weights': {'z': 0.6, 'y': 0.3, 'x': 0.1}, 'consistency_ratio': 0.0, 'random_index': 'Donegan & Dodd', 'count': 3, 'names': ['x', 'y', 'z']}, 'children': None, 'comparisons': {'count': 3, 'input': {'x': 1, 'y': 3, 'z': 6}, 'computed': None}}
