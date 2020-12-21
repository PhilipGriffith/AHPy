import numpy as np
from ahpy import Compare, Compose
# Example from Saaty, Thomas, L., Theory and Applications of the Analytic Network Process, 2005
# crit = np.array([[1, .2, 3, .5, 5],
#                   [5, 1, 7, 1, 7],
#                   [1/3., 1/7., 1, .25, 3],
#                   [2, 1, 4, 1, 7],
#                   [.2, 1/7., 1/3., 1/7., 1]])
#
# culture = np.array([[1, .5, 1, .5],
#                      [2, 1, 2.5, 1],
#                      [1, 1/2.5, 1, 1/2.5],
#                      [2, 1, 2.5, 1]])
#
# family = np.array([[1, 2, 1/3., 4],
#                     [.5, 1, 1/8., 2],
#                     [3, 8, 1, 9],
#                     [.25, .5, 1/9., 1]])
#
# housing = np.array([[1, 5, .5, 2.5],
#                      [.2, 1, 1/9., .25],
#                      [2, 9, 1, 7],
#                      [1/2.5, 4, 1/7., 1]])
#
# jobs = np.array([[1, .5, 3, 4],
#                   [2, 1, 6, 8],
#                   [1/3., 1/6., 1, 1],
#                   [.25, 1/8., 1, 1]])
#
# transportation = np.array([[1, 1.5, .5, 4],
#                             [1/1.5, 1, 1/3.5, 2.5],
#                             [2, 3.5, 1, 9],
#                             [.25, 1/2.5, 1/9., 1]])
#
# cities = ['Bethesda', 'Boston', 'Pittsburgh', 'Santa Fe']
# crits = ['Culture', 'Family', 'Housing', 'Jobs', 'Transportation']
#
# print('Saaty')
# cu = Compare('Culture', culture, cities, 3, random_index='Saaty')
# f = Compare('Family', family, cities, 3, random_index='Saaty')
# h = Compare('Housing', housing, cities, 3, random_index='Saaty')
# j = Compare('Jobs', jobs, cities, 3, random_index='Saaty')
# t = Compare('Transportation', transportation, cities, 3, random_index='Saaty')
#
# comp_matrices = [cu, f, h, j, t]
# cr = Compare('Goal', crit, crits, 3, random_index='Saaty')
# c = Compose('Goal', cr, comp_matrices)
# print(c.weights)
# #
# # print('=================\n')
# print('Donegan and Dodd')
# cu = Compare('Culture', culture, cities, 4)
# f = Compare('Family', family, cities, 4)
# h = Compare('Housing', housing, cities, 4)
# j = Compare('Jobs', jobs, cities, 4)
# t = Compare('Transportation', transportation, cities, 4)
#
# comp_matrices = [cu, f, h, j, t]
# cr = Compare('Goal', crit, crits, 4)
#
# c = Compose('Goal', cr, comp_matrices)
# print(c.weights)
#
# ----------------------------------------------------------------------------------
# Example from https://en.wikipedia.org/wiki/Analytic_hierarchy_process_%E2%80%93_leader_example
# experience = np.array([[1, .25, 4], [4, 1, 9], [.25, 1/9., 1]])
# education = np.array([[1, 3, .2], [1/3., 1, 1/7.], [5, 7, 1]])
# charisma = np.array([[1, 5, 9], [.2, 1, 4], [1/9., .25, 1]])
# age = np.array([[1, 1/3., 5], [3, 1, 9], [.2, 1/9., 1]])
# criteria = np.array([[1, 4, 3, 7], [.25, 1, 1/3., 3], [1/3., 3, 1, 5], [1/7., 1/3., .2, 1]])
#
# alt1 = ['Tom', 'Dick', 'Harry']
#
# exp = Compare('exp', experience, alt1, 3, random_index='saaty')
# edu = Compare('edu', education, alt1, 3, random_index='saaty')
# cha = Compare('cha', charisma, alt1, 3, random_index='saaty')
# age = Compare('age', age, alt1, 3, random_index='saaty')
#
# children = [exp, edu, cha, age]
#
# alt2 = ['exp', 'edu', 'cha', 'age']
#
# parent = Compare('goal', criteria, alt2, 3, random_index='saaty')
# Compose('goal', parent, children).report()
#
# ----------------------------------------------------------------------------------
# Examples from Saaty, Thomas L., 'Decision making with the analytic hierarchy process,'
# Int. J. Services Sciences, 1:1, 2008, pp. 83-98.
# drinks_val = np.array([[1, 9, 5, 2, 1, 1, .5],
#                     [1/9., 1, 1/3., 1/9., 1/9., 1/9., 1/9.],
#                     [.2, 3, 1, 1/3., .25, 1/3., 1/9.],
#                     [.5, 9, 3, 1, .5, 1, 1/3.],
#                     [1, 9, 4, 2, 1, 2, .5],
#                     [1, 9, 3, 1, .5, 1, 1/3.],
#                     [2, 9, 9, 3, 2, 3, 1]])
# drinks_cri = ('coffee', 'wine', 'tea', 'beer', 'sodas', 'milk', 'water')
# c = Compare('Drinks', drinks_val, drinks_cri, precision=4, random_index='dd')
#
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
#
# ----------------------------------------------------------------------------------
# Example from https://mi.boku.ac.at/ahp/ahptutorial.pdf
#
# car_cri = ('civic', 'saturn', 'escort', 'clio')
#
# gas_m = np.array([[34], [27], [24], [28]])
# gas_m2 = '34;27;24;28'
# gas = Compare('gas', gas_m2, car_cri, 3, comp_type='quant')
#
# rel_m = np.array([[1, 2, 5, 1], [.5, 1, 3, 2], [.2, 1/3., 1, .25], [1, .5, 4, 1]])
# rel = Compare('rel', rel_m, car_cri)
#
# style_m = np.array([[1, .25, 4, 1/6.], [4, 1, 4, .25], [.25, .25, 1, .2], [6, 4, 5, 1]])
# style = Compare('style', style_m, car_cri, 3)
#
# cri_m = np.array([[1, .5, 3], [2, 1, 4], [1/3., .25, 1]])
# cri_cri = ('style', 'rel', 'gas')
# parent = Compare('goal', cri_m, cri_cri)
#
# Compose('goal', parent, (style, rel, gas)).report()
#
# ----------------------------------------------------------------------------------
# Example from https://en.wikipedia.org/wiki/Analytic_hierarchy_process_%E2%80%93_car_example

# cri = ('cost', 'safety', 'style', 'capacity')
# cri_m = '3 7 3; 9 1; 1/7'
# criteria = Compare('goal', cri_m, cri)
#
# alt = ('Accord Sedan', 'Accord Hybrid', 'Pilot', 'CR-V', 'Element', 'Odyssey')
#
# cost_sub_m = '2 5 3; 2 2; .5'
# cost_sub = Compare('cost', cost_sub_m, ('cost price', 'cost fuel', 'cost maintenance', 'cost resale'))
# cost_sub.report()
#
# cost_price_m = '9 9 1 .5 5; 1 1/9 1/9 1/7; 1/9 1/9 1/7; .5 5; 6'
# cost_price = Compare('cost price', cost_price_m, alt)
#
# cost_fuel_m = '1/1.13 1.41 1.15 1.24 1.19; 1.59 1.3 1.4 1.35; 1/1.23 1/1.14 1/1.18; 1.08 1.04; 1/1.04'
# cost_fuel = Compare('cost fuel', cost_fuel_m, alt)
#
# cost_resale_m = '3 4 .5 2 2; 2 .2 1 1; 1/6 .5 .5; 4 4; 1'
# cost_resale = Compare('cost resale', cost_resale_m, alt)
#
# cost_maint_m = '1.5 4 4 4 5; 4 4 4 5; 1 1.2 1; 1 3; 2'
# cost_maint = Compare('cost maintenance', cost_maint_m, alt)
#
# safety_m = '1 5 7 9 1/3; 5 7 9 1/3; 2 9 1/8; 2 1/8; 1/9'
# safety = Compare('safety', safety_m, alt)
#
# style_m = '1 7 5 9 6; 7 5 9 6; 1/6 3 1/3; 7 5; .2'
# style = Compare('style', style_m, alt)
#
# capacity_sub_m = '.2'
# capacity_sub = Compare('capacity', capacity_sub_m, ('capacity cargo', 'capacity passenger'))
# capacity_sub.report()
#
# capacity_pass_m = '1 .5 1 3 .5; .5 1 3 .5; 2 6 1; 3 .5; 1/6'
# capacity_pass = Compare('capacity passenger', capacity_pass_m, alt)
#
# capacity_cargo_m = '1 .5 .5 .5 1/3; .5 .5 .5 1/3; 1 1 .5; 1 .5; .5'
# capacity_cargo = Compare('capacity cargo', capacity_cargo_m, alt)
#
# cost = Compose('cost', cost_sub, (cost_price, cost_fuel, cost_resale, cost_maint))
# capacity = Compose('capacity', capacity_sub, (capacity_cargo, capacity_pass))
# goal = Compose('goal', criteria, (cost, safety, style, capacity))
#
# goal.report()
