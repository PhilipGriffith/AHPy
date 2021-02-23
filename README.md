# AHPy

:construction: UNDER CONSTRUCTION! :construction:

**AHPy** is an implementation of the Analytic Hierarchy Process ([AHP](https://en.wikipedia.org/wiki/Analytic_hierarchy_process)), a method used to structure, synthesize and evaluate the elements of a decision problem. Developed by [Thomas Saaty](http://www.creativedecisions.org/about/ThomasLSaaty.php) in the 1970s, AHP's broad use in fields well beyond that of operational research is a testament to its simple yet powerful combination of psychology and mathematics.

#### Installing AHPy

AHPy is available on the Python Package Index ([PyPI](https://pypi.org/)):

```
python -m pip install ahpy
```

AHPy requires [Python 3.7+](https://www.python.org/), as well as [numpy](https://numpy.org/) and [scipy](https://scipy.org/).

## Using AHPy

### Table of Contents

[Compare()](#compare)

[Missing Pairwise Comparisons](#missing-pairwise-comparisons)

[add_children()](#add_children)

[complete()](#complete)

[report()](#report)

### Compare()

The Compare class computes the priority vector and consistency ratio of a positive reciprocal matrix, created using an input dictionary of pairwise comparison values. Optimal values are computed for any missing pairwise comparisons. Compare objects can also be linked together to form a hierarchy representing the decision problem: global problem solutions are then derived by synthesizing all levels of the hierarchy.

`Compare(name, comparisons, precision=4, random_index='dd', iterations=100, tolerance=0.0001, cr=True)`

- `name`: *str*, the name of the Compare object
  - This property is used to link a child object to its parent and must be unique

- `comparisons`: *dict*, the elements and values to be compared, provided in one of two forms:
  1. A dictionary of pairwise comparisons, in which each key is a tuple of two elements and each value is their pairwise comparison value
      - `{('a', 'b'): 3, ('b', 'c'): 2, ('a', 'c'): 5}`
      - The comparison `('a', 'b'): 3` means "a is moderately more important than b"
  2. A dictionary of measured values, in which each key is a single element and each value is that element's measured value
      - `{'a': 1.2, 'b': 2.3, 'c': 3.4}`
      - Given this form, AHPy will automatically create a priority vector of normalized values

- `precision`: *int*, the number of decimal places to consider when computing both the priority vector and the consistency ratio of the Compare object *(optional)*

- `random_index`: *'dd'* or *'saaty'*, the set of random index estimates used to compute the priority vector's consistency ratio *(optional)*
  - 'dd' uses estimates from Donegan, H.A. and Dodd, F.J., 'A Note on Saaty's Random Indexes,' *Mathematical and Computer Modelling*, 15:10, 1991, pp. 135-137 (DOI: [10.1016/0895-7177(91)90098-R](https://doi.org/10.1016/0895-7177(91)90098-R))
    - 'dd' supports the computation of consistency ratios for matrices less than or equal to 100 &times; 100 in size
  - 'saaty' uses estimates from Saaty, T., *Theory And Applications Of The Analytic Network Process*, Pittsburgh: RWS Publications, 2005, p. 31
    - 'saaty' supports the computation of consistency ratios for matrices less than or equal to 15 &times; 15 in size

- `iterations`: *int*, the stopping criterion for the algorithm used to compute the Compare object's priority vector *(optional)*
  - If the priority vector has not been determined after this number of iterations, the algorithm stops and the last principal eigenvector to be computed is assigned as the priority vector

- `tolerance`: *float*, the stopping criterion for the cycling coordinates algorithm used to compute the optimal value of missing pairwise comparisons *(optional)*
  - The algorithm stops when the difference between the norms of two cycles of coordinates is less than this value

- `cr`: *bool*, an override to compute the Compare object's priority vector even when a consistency ratio cannot be computed due to the size of the matrix *(optional)*
  - This allows for the computation of matrices greater than 100 &times; 100 in size

### Missing Pairwise Comparisons

When a Compare object is initialized, the elements forming the keys of the input `comparisons` dictionary are permuted. Permutations of elements that do not contain a value within the `comparisons` dictionary are then optimally solved for using the cyclic coordinates algorithm described in:

Bozóki, S., Fülöp, J. and Rónyai, L., 'On optimal completion of incomplete pairwise comparison matrices,' *Mathematical and Computer Modelling*, 52:1–2, 2010, pp. 318-333 (DOI: [10.1016/j.mcm.2010.02.047](https://doi.org/10.1016/j.mcm.2010.02.047))

### add_children()

Compare objects can be linked together to form a hierarchy representing the decision problem. To link two Compare objects together, call the `add_children()` method of the object in the upper level (the *parent*) and include as an argument a list or tuple of one or more Compare objects that will form the lower level (the *children*):

```python
>>> child1 = ahpy.Compare('child1', ...)
>>> child2 = ahpy.Compare('child2', ...)
>>> parent = ahpy.Compare('parent', ...)
>>> parent.add_children([child1, child2])
```

In order to synthesize the levels of the problem hierarchy, objects in the lower levels must appear as elements in their parent's pairwise comparisons dictionary.


names
order
complete()

precision
target differs from node's local/global

### complete()

### report()

structure
name
weight
weights: local, global, target
cr
ri
elements: count, names
children: count, names
comparisons: input, computed


```python
>>> import ahpy
>>> comparisons = {('a', 'b'): 1, ('a', 'c'): 5, ('a', 'd'): 2, ('b', 'c'): 3, ('b', 'd'): 4, ('c', 'd'): 3/4}
>>> complete = ahpy.Compare('complete', comparisons)
>>> print(complete.target_weights)
{'b': 0.3917, 'a': 0.3742, 'd': 0.1349, 'c': 0.0991}
>>> print(complete.consistency_ratio)
0.0372
>>> del comparisons[('c', 'd')]
>>> partial = ahpy.Compare('partial', comparisons)
>>> print(partial.target_weights)
{'b': 0.392, 'a': 0.3738, 'd': 0.1357, 'c': 0.0985}
>>> print(partial.consistency_ratio)
0.0372
```



```python
drinks = {('coffee', 'wine'): 9, ('coffee', 'tea'): 5, ('coffee', 'beer'): 2, ('coffee', 'soda'): 1, ('coffee', 'milk'): 1, ('coffee', 'water'): 1/2,
('wine', 'tea'): 1/3, ('wine', 'beer'): 1/9, ('wine', 'soda'): 1/9, ('wine', 'milk'): 1/9, ('wine', 'water'): 1/9,
('tea', 'beer'): 1/3, ('tea', 'soda'): 1/4, ('tea', 'milk'): 1/3, ('tea', 'water'): 1/9,
('beer', 'soda'): 1/2, ('beer', 'milk'): 1, ('beer', 'water'): 1/3,
('soda', 'milk'): 2, ('soda', 'water'): 1/2,
('milk', 'water'): 1/3}
c = ahpy.Compare('Drinks', drinks, precision=3, random_index='saaty')
c['target_weights']
```
