import itertools

import numpy as np

from ahpy import Compare, Compose

# Example from https://en.wikipedia.org/wiki/Analytic_hierarchy_process_%E2%80%93_leader_example

# experience = {('Tom', 'Dick'): 0.25, ('Tom', 'Harry'): 4, ('Dick', 'Harry'): 9}
# education = {('Tom', 'Dick'): 3, ('Tom', 'Harry'): 0.2, ('Harry', 'Dick'): 7}
# charisma = {('Tom', 'Dick'): 5, ('Tom', 'Harry'): 9, ('Dick', 'Harry'): 4}
# age = {('Dick', 'Tom'): 3, ('Tom', 'Harry'): 5, ('Dick', 'Harry'): 9}
# criteria = {('exp', 'edu'): 4, ('exp', 'cha'): 3, ('exp', 'age'): 7,
#             ('edu', 'age'): 3,
#             ('cha', 'edu'): 3, ('cha', 'age'): 5}
#
# exp = Compare('exp', experience, precision=3, random_index='saaty')
# edu = Compare('edu', education, precision=3, random_index='saaty')
# cha = Compare('cha', charisma, precision=3, random_index='saaty')
# age = Compare('age', age, precision=3, random_index='saaty')
#
# children = [exp, edu, cha, age]
#
# parent = Compare('goal', criteria, precision=3, random_index='saaty')
# c = Compose('goal', parent, children)

# ----------------------------------------------------------------------------------
# Examples from Saaty, Thomas L., 'Decision making with the analytic hierarchy process,'
# Int. J. Services Sciences, 1:1, 2008, pp. 83-98.
# drinks = {('coffee', 'wine'): 9, ('coffee', 'tea'): 5, ('coffee', 'beer'): 2, ('coffee', 'soda'): 1,
#           ('coffee', 'milk'): 1, ('water', 'coffee'): 2, ('tea', 'wine'): 3, ('beer', 'wine'): 9, ('beer', 'tea'): 3,
#           ('beer', 'milk'): 1, ('soda', 'wine'): 9, ('soda', 'tea'): 4, ('soda', 'beer'): 2, ('soda', 'milk'): 2,
#           ('milk', 'wine'): 9, ('milk', 'tea'): 3, ('water', 'coffee'): 2, ('water', 'wine'): 9, ('water', 'tea'): 9,
#           ('water', 'beer'): 3, ('water', 'soda'): 2, ('water', 'milk'): 3}
# c = Compare('Drinks', drinks, precision=3, random_index='dd')

# ----------------------------------------------------------------------------------
# Example from  Triantaphyllou, E. and Mann, S., 'Using the Analytic Hierarchy Process
# for Decision Making in Engineering Applications: Some Challenges,' Int. J. of Industrial
# Engineering: Applications and Practice, 2:1, 1995, pp.35-44.
#
# alt = ('a', 'b', 'c')
#
# expand_m = '1 6 8; 1/6 1 4; 1/8 1/4 1'
# expand = Compare('expand', expand_m, alt, random_index='saaty')
#
# maintain_m = '1 7 1/5; 1/7 1 1/8; 5 8 1'
# maintain = Compare('maintain', maintain_m, alt, random_index='saaty')
#
# finance_m = '1 8 6; 1/8 1 1/4; 1/6 4 1'
# finance = Compare('finance', finance_m, alt, random_index='saaty')
#
# user_m = '1 5 4; 1/5 1 1/3; 1/4 3 1'
# user = Compare('user', user_m, alt, random_index='saaty')
#
# cri_n = ('expand', 'maintain', 'finance', 'user')
# cri_m = '1 5 3 7; 1/5 1 1/3 5; 1/3 3 1 6; 1/7 1/5 1/6 1'
# cri = Compare('goal', cri_m, cri_n, random_index='saaty')
#
# Compose('goal', cri, [maintain, user, finance, expand]).report()

# ----------------------------------------------------------------------------------
# Example from https://mi.boku.ac.at/ahp/ahptutorial.pdf

# cars = ('civic', 'saturn', 'escort', 'clio')
#
# gas_m = dict(zip(cars, (34, 27, 24, 28)))
# gas = Compare('gas', gas_m, precision=3)
#
# rel_m = dict(zip(itertools.combinations(cars, 2), (2, 5, 1, 3, 2, 0.25)))
# rel = Compare('rel', rel_m)
#
# style_m = {('civic', 'escort'): 4,
#            ('saturn', 'civic'): 4, ('saturn', 'escort'): 4, ('saturn', 'clio'): 0.25,
#            ('clio', 'civic'): 6, ('clio', 'escort'): 5}
# style = Compare('style', style_m, precision=4)
#
# cri_m = {('style', 'rel'): 0.5, ('style', 'gas'): 3,
#          ('rel', 'gas'): 4}
# parent = Compare('goal', cri_m)
#
# c = Compose('goal', parent, (style, rel, gas))

# ----------------------------------------------------------------------------------
# Example from https://en.wikipedia.org/wiki/Analytic_hierarchy_process_%E2%80%93_car_example


def r(x):
    return np.reciprocal(float(x))


def m(elements, judgments):
    return dict(zip(elements, judgments))


cri = ('cost', 'safety', 'style', 'capacity')
c_cri = list(itertools.combinations(cri, 2))
criteria = Compare('goal', m(c_cri, (3, 7, 3, 9, 1, np.reciprocal(float(7)))))

alt = ('Accord Sedan', 'Accord Hybrid', 'Pilot', 'CR-V', 'Element', 'Odyssey')
pairs = list(itertools.combinations(alt, 2))

costs = ('cost price', 'cost fuel', 'cost maintenance', 'cost resale')
c_pairs = list(itertools.combinations(costs, 2))
cost_sub = Compare('cost', m(c_pairs, (2, 5, 3, 2, 2, .5)), precision=3)

cost_price_m = (9, 9, 1, 0.5, 5, 1, r(9), r(9), r(7), r(9), r(9), r(7), .5, 5, 6)
cost_price = Compare('cost price', m(pairs, cost_price_m))

cost_fuel_m = (r(1.13), 1.41, 1.15, 1.24, 1.19, 1.59, 1.3, 1.4, 1.35, r(1.23), r(1.14), r(1.18), 1.08, 1.04, r(1.04))
cost_fuel = Compare('cost fuel', m(pairs, cost_fuel_m))

cost_resale_m = (3, 4, .5, 2, 2, 2, .2, 1, 1, r(6), .5, .5, 4, 4, 1)
cost_resale = Compare('cost resale', m(pairs, cost_resale_m))

cost_maint_m = (1.5, 4, 4, 4, 5, 4, 4, 4, 5, 1, 1.2, 1, 1, 3, 2)
cost_maint = Compare('cost maintenance', m(pairs, cost_maint_m))

safety_m = (1, 5, 7, 9, r(3), 5, 7, 9, r(3), 2, 9, r(8), 2, r(8), r(9))
safety = Compare('safety', m(pairs, safety_m))

style_m = (1, 7, 5, 9, 6, 7, 5, 9, 6, r(6), 3, r(3), 7, 5, .2)
style = Compare('style', m(pairs, style_m))

capacity_sub = Compare('capacity', {('capacity cargo', 'capacity passenger'): 0.2})

capacity_pass_m = (1, .5, 1, 3, .5, .5, 1, 3, .5, 2, 6, 1, 3, .5, r(6))
capacity_pass = Compare('capacity passenger', m(pairs, capacity_pass_m))

capacity_cargo_m = (1, .5, .5, .5, r(3), .5, .5, .5, r(3), 1, 1, .5, 1, .5, .5)
capacity_cargo = Compare('capacity cargo', m(pairs, capacity_cargo_m), precision=3)

cost = Compose('cost', cost_sub, (cost_price, cost_fuel, cost_resale, cost_maint))
capacity = Compose('capacity', capacity_sub, (capacity_cargo, capacity_pass))
goal = Compose('goal', criteria, (cost, safety, style, capacity))


# ----------------------------------------------------------------------------------

u = {('alpha', 'beta'): 1, ('alpha', 'chi'): 5, ('alpha', 'delta'): 2,
     ('beta', 'chi'): 3, ('beta', 'delta'): 4}
# cu = Compare('Incomplete Test', u)

m = {('a', 'b'): 5, ('a', 'c'): 3, ('a', 'd'): 7, ('a', 'e'): 6, ('a', 'f'): 6,
     ('b', 'd'): 5, ('b', 'f'): 3,
     ('c', 'e'): 3, ('c', 'g'): 6,
     ('f', 'd'): 4,
     ('g', 'a'): 3, ('g', 'e'): 5,
     ('h', 'a'): 4, ('h', 'b'): 7, ('h', 'd'): 8, ('h', 'f'): 6}

cm = Compare('Incomplete Housing', m)

f = {'civic': 34, 'saturn': 27, 'escort': 24, 'clio': 28}
cf = Compare('Fuel Economy', f)
cf.report()