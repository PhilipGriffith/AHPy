import itertools

import numpy as np

from ahpy import ahpy

# Example from https://en.wikipedia.org/wiki/Analytic_hierarchy_process_%E2%80%93_leader_example

experience_comparisons = {('Moll', 'Nell'): 1 / 4, ('Moll', 'Sue'): 4, ('Nell', 'Sue'): 9}
education_comparisons = {('Moll', 'Nell'): 3, ('Moll', 'Sue'): 1 / 5, ('Nell', 'Sue'): 1 / 7}
charisma_comparisons = {('Moll', 'Nell'): 5, ('Moll', 'Sue'): 9, ('Nell', 'Sue'): 4}
age_comparisons = {('Moll', 'Nell'): 1 / 3, ('Moll', 'Sue'): 5, ('Nell', 'Sue'): 9}
criteria_comparisons = {('Experience', 'Education'): 4, ('Experience', 'Charisma'): 3, ('Experience', 'Age'): 7,
                        ('Education', 'Charisma'): 1 / 3, ('Education', 'Age'): 3,
                        ('Charisma', 'Age'): 5}

experience = ahpy.Compare('Experience', experience_comparisons, precision=3, random_index='saaty')
education = ahpy.Compare('Education', education_comparisons, precision=3, random_index='saaty')
charisma = ahpy.Compare('Charisma', charisma_comparisons, precision=3, random_index='saaty')
age = ahpy.Compare('Age', age_comparisons, precision=3, random_index='saaty')
criteria = ahpy.Compare('Criteria', criteria_comparisons, precision=3, random_index='saaty')

criteria.add_children([experience, education, charisma, age])

criteria.report(show=True)

# ----------------------------------------------------------------------------------
# Examples from Saaty, Thomas L., 'Decision making with the analytic hierarchy process,'
# Int. J. Services Sciences, 1:1, 2008, pp. 83-98.

# drinks = {('coffee', 'wine'): 9, ('coffee', 'tea'): 5, ('coffee', 'beer'): 2, ('coffee', 'soda'): 1,
#           ('coffee', 'milk'): 1, ('water', 'coffee'): 2, ('tea', 'wine'): 3, ('beer', 'wine'): 9, ('beer', 'tea'): 3,
#           ('beer', 'milk'): 1, ('soda', 'wine'): 9, ('soda', 'tea'): 4, ('soda', 'beer'): 2, ('soda', 'milk'): 2,
#           ('milk', 'wine'): 9, ('milk', 'tea'): 3, ('water', 'coffee'): 2, ('water', 'wine'): 9, ('water', 'tea'): 9,
#           ('water', 'beer'): 3, ('water', 'soda'): 2, ('water', 'milk'): 3}
# c = ahpy.Compare('Drinks', drinks, precision=4, random_index='dd')

# ----------------------------------------------------------------------------------
# Example from https://mi.boku.ac.at/ahp/ahptutorial.pdf

# cars = ('civic', 'saturn', 'escort', 'clio')
#
# gas_m = dict(zip(cars, (34, 27, 24, 28)))
# gas = Compare('gas', gas_m, precision=3)
#
# rel_m = dict(zip(itertools.combinations(cars, 2), (2, 5, 1, 3, 2, 0.25)))
# rel = Compare('rel', rel_m, 3)
#
# style_m = {('civic', 'escort'): 4,
#            ('saturn', 'civic'): 4, ('saturn', 'escort'): 4, ('saturn', 'clio'): 0.25,
#            ('clio', 'civic'): 6, ('clio', 'escort'): 5}
# style = Compare('style', style_m, precision=3)
#
# cri_m = {('style', 'rel'): 0.5, ('style', 'gas'): 3,
#          ('rel', 'gas'): 4}
# goal = Compare('goal', cri_m)
#
# goal.children([gas, rel, style])

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
#
# cr = ahpy.Compare('Goal', criteria, precision=3, random_index='Saaty')
# cr.add_children([cu, f, h, j, t])
# cr.report(True)

# ----------------------------------------------------------------------------------
# Example from https://en.wikipedia.org/wiki/Analytic_hierarchy_process_%E2%80%93_car_example


def r(x):
    return np.reciprocal(float(x))


def m(elements, judgments):
    return dict(zip(elements, judgments))


cri = ('Cost', 'Safety', 'Style', 'Capacity')
c_cri = list(itertools.combinations(cri, 2))
criteria = ahpy.Compare('Criteria', m(c_cri, (3, 7, 3, 9, 1, 1 / 7)), 3)

alt = ('Accord Sedan', 'Accord Hybrid', 'Pilot', 'CR-V', 'Element', 'Odyssey')
pairs = list(itertools.combinations(alt, 2))

costs = ('Price', 'Fuel', 'Maintenance', 'Resale')
c_pairs = list(itertools.combinations(costs, 2))
cost = ahpy.Compare('Cost', m(c_pairs, (2, 5, 3, 2, 2, .5)), precision=3)

cost_price_m = (9, 9, 1, 0.5, 5, 1, 1 / 9, 1 / 9, 1 / 7, 1 / 9, 1 / 9, 1 / 7, 1 / 2, 5, 6)
cost_price = ahpy.Compare('Price', m(pairs, cost_price_m), 3)

cost_fuel_m = (r(1.13), 1.41, 1.15, 1.24, 1.19, 1.59, 1.3, 1.4, 1.35, r(1.23), r(1.14), r(1.18), 1.08, 1.04, r(1.04))
cost_fuel = ahpy.Compare('Fuel', m(pairs, cost_fuel_m), 3)

cost_resale_m = (3, 4, 1 / 2, 2, 2, 2, 1 / 5, 1, 1, 1 / 6, 1 / 2, 1 / 2, 4, 4, 1)
cost_resale = ahpy.Compare('Resale', m(pairs, cost_resale_m), 3)

cost_maint_m = (1.5, 4, 4, 4, 5, 4, 4, 4, 5, 1, 1.2, 1, 1, 3, 2)
cost_maint = ahpy.Compare('Maintenance', m(pairs, cost_maint_m), 3)

safety_m = (1, 5, 7, 9, 1 / 3, 5, 7, 9, 1 / 3, 2, 9, 1 / 8, 2, 1 / 8, 1 / 9)
safety = ahpy.Compare('Safety', m(pairs, safety_m), 3)

style_m = (1, 7, 5, 9, 6, 7, 5, 9, 6, 1 / 6, 3, 1 / 3, 7, 5, 1 / 5)
style = ahpy.Compare('Style', m(pairs, style_m), 3)

capacity = ahpy.Compare('Capacity', {('capacity cargo', 'capacity passenger'): 0.2})

capacity_pass_m = (1, 1 / 2, 1, 3, 1 / 2, 1 / 2, 1, 3, 1 / 2, 2, 6, 1, 3, 1 / 2, 1 / 6)
capacity_pass = ahpy.Compare('capacity passenger', m(pairs, capacity_pass_m), 3)

capacity_cargo_m = (1, 1 / 2, 1 / 2, 1 / 2, 1 / 3, 1 / 2, 1 / 2, 1 / 2, 1 / 3, 1, 1, 1 / 2, 1, 1 / 2, 1 / 2)
capacity_cargo = ahpy.Compare('capacity cargo', m(pairs, capacity_cargo_m), precision=3)

# capacity_pass = ahpy.Compare('capacity passenger', {('leg room', 'seats'): 0.2})
# leg_room = ahpy.Compare('leg room', m(pairs, capacity_cargo_m))
# seats = ahpy.Compare('seats', {('top', 'bottom'): 0.2})
# top = ahpy.Compare('top', m(pairs, capacity_cargo_m))
# bottom = ahpy.Compare('bottom', m(pairs, capacity_pass_m))
# seats.add_children([top, bottom])

# capacity_pass.add_children([leg_room, seats])
cost.add_children([cost_price, cost_fuel, cost_resale, cost_maint])
capacity.add_children([capacity_pass, capacity_cargo])
criteria.add_children([cost, safety, style, capacity])

criteria.complete()
criteria.report(1)
print(criteria.target_weights)

# ----------------------------------------------------------------------------------

# u = {('alpha', 'beta'): 1, ('alpha', 'chi'): 5, ('alpha', 'delta'): 2,
#      ('beta', 'chi'): 3, ('beta', 'delta'): 4}#, ('chi', 'delta'): 3/4}
# cu = ahpy.Compare('Incomplete Test', u, cr=False)
# print(cu.target_weights)
# print(cu.consistency_ratio)
# r = cu.report(True)
# print(r)

# m = {('a', 'b'): 5, ('a', 'c'): 3, ('a', 'd'): 7, ('a', 'e'): 6, ('a', 'f'): 6,
#      ('b', 'd'): 5, ('b', 'f'): 3,
#      ('c', 'e'): 3, ('c', 'g'): 6,
#      ('f', 'd'): 4,
#      ('g', 'a'): 3, ('g', 'e'): 5,
#      ('h', 'a'): 4, ('h', 'b'): 7, ('h', 'd'): 8, ('h', 'f'): 6}
#
# cm = Compare('Incomplete Housing', m)
# cm.report()
#
# f = {'civic': 34, 'saturn': 27, 'escort': 24, 'clio': 28}
# cf = ahpy.Compare('Fuel Economy', f)
# r = cf.report(True)
# print(r)

#
# books = {('Jane Eyre', 'Moby Dick'): 5,
#          ('Jane Eyre', 'Pride & Prejudice'): 3,
#          ('Jane Eyre', 'Catcher in the Rye'): 1,
#          ('Pride & Prejudice', 'Moby Dick'): 3,
#          ('Moby Dick', 'Catcher in the Rye'): 1 / 4,
#          ('Pride & Prejudice', 'Catcher in the Rye'): 2}
#
# c = Compare('Book List', books)
# c.report()
