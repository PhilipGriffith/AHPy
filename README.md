# AHPy

:construction: UNDER CONSTRUCTION! :construction:

**AHPy** is an implementation of the Analytic Hierarchy Process ([AHP](https://en.wikipedia.org/wiki/Analytic_hierarchy_process)), a method used to structure, synthesize and evaluate the elements of a decision problem. Developed by [Thomas Saaty](http://www.creativedecisions.org/about/ThomasLSaaty.php) in the 1970s, AHP's broad use in fields well beyond that of operational research is a testament to its simple yet powerful combination of psychology and mathematics.

#### Installing AHPy

AHPy is available on the Python Package Index ([PyPI](https://pypi.org/)):

```
python -m pip install ahpy
```

AHPy requires [Python 3.7+](https://www.python.org/), as well as [numpy](https://numpy.org/) and [scipy](https://scipy.org/).

### Table of Contents

#### Examples

[Relative consumption of drinks in the United States](#relative-consumption-of-drinks-in-the-united-states)

[Choosing a leader](#choosing-a-leader)

[Purchasing a vehicle](#purchasing-a-vehicle)

#### Using AHPy

[Terminology](#terminology)

[Compare()](#compare)

[Compare.report()](#comparereport)

[Compare.add_children()](#compareadd_children)

[Compare.complete()](#comparecomplete)

[Missing Pairwise Comparisons](#missing-pairwise-comparisons)

---

## Examples

### Relative consumption of drinks in the United States

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

### Choosing a leader

### Purchasing a vehicle

## Using AHPy

### Terminology

describe "target", 'element', 'value'

### Compare()

The Compare class computes the priority vector and consistency ratio of a positive reciprocal matrix, created using an input dictionary of pairwise comparison values. Optimal values are computed for any missing pairwise comparisons. Compare objects can also be [linked together to form a hierarchy](#compareadd_children) representing the decision problem: global problem elements are then derived by synthesizing all levels of the hierarchy.

`Compare(name, comparisons, precision=4, random_index='dd', iterations=100, tolerance=0.0001, cr=True)`

- `name`: *str (required)*, the name of the Compare object
  - This property is used to link a child object to its parent and must be unique

- `comparisons`: *dict (required)*, the elements and values to be compared, provided in one of two forms:
  1. A dictionary of pairwise comparisons, in which each key is a tuple of two elements and each value is their pairwise comparison value
      - `{('a', 'b'): 3, ('b', 'c'): 2, ('a', 'c'): 5}`
      - The order of the key elements matters: the comparison `('a', 'b'): 3` means "a is moderately more important than b"
  2. A dictionary of measured values, in which each key is a single element and each value is that element's measured value
      - `{'a': 1.2, 'b': 2.3, 'c': 3.4}`
      - Given this form, AHPy will automatically create a consistent priority vector of normalized values

- `precision`: *int*, the number of decimal places to take into account when computing both the priority vector and the consistency ratio of the Compare object
  - The default precision is 4

- `random_index`: *'dd'* or *'saaty'*, the set of random index estimates used to compute the priority vector's consistency ratio
  - 'dd' uses estimates from Donegan, H.A. and Dodd, F.J., 'A Note on Saaty's Random Indexes,' *Mathematical and Computer Modelling*, 15:10, 1991, pp. 135-137 (DOI: [10.1016/0895-7177(91)90098-R](https://doi.org/10.1016/0895-7177(91)90098-R))
    - 'dd' supports the computation of consistency ratios for matrices less than or equal to 100 &times; 100 in size
  - 'saaty' uses estimates from Saaty, T., *Theory And Applications Of The Analytic Network Process*, Pittsburgh: RWS Publications, 2005, p. 31
    - 'saaty' supports the computation of consistency ratios for matrices less than or equal to 15 &times; 15 in size
  - The default random index is 'dd'

- `iterations`: *int*, the stopping criterion for the algorithm used to compute the Compare object's priority vector
  - If the priority vector has not been determined after this number of iterations, the algorithm stops and the last principal eigenvector to be computed is assigned as the priority vector
  - The default number of iterations is 100

- `tolerance`: *float*, the stopping criterion for the cycling coordinates algorithm used to compute the optimal value of missing pairwise comparisons
  - The algorithm stops when the difference between the norms of two cycles of coordinates is less than this value
  - The default tolerance value is 0.0001

- `cr`: *bool*, whether to compute the priority vector's consistency ratio
  - Set `cr=False` to compute the priority vector of a matrix when a consistency ratio cannot be determined due to the size of the matrix
  - The default value is True

### Compare.report()

A report on the details of each Compare object is available. To return the report as a dictionary, call `report()` on the Compare object; to simultaneously print the information to the console, set `show=True`.

`Compare.report(show=False)`

- `show`: *bool*, whether to print the report to the console
  - The default value is False

The keys of the report take the following form:

- `name`: *str*, the name of the Compare object
- `weight`: *float*, the global weight of the Compare object in the hierarchy
- `target`: *dict*, the target weights of the elements in the lowest level of the hierarchy; each key is a single element and each value is that element's computed target weight; **if the global weight of the Compare object is less than 1.0, this value will be `None`**
    - `{'a': 0.5, 'b': 0.5}`
- `weights`: *dict*, the weights of the Compare object's elements
  - `local`: *dict*, the local weights of the Compare object's elements; each key is a single element and each value is that element's computed local weight
    - `{'a': 0.5, 'b': 0.5}`
  - `global`: *dict*, the global weights of the Compare object's elements; each key is a single element and each value is that element's computed global weight
    - `{'a': 0.25, 'b': 0.25}`
- `consistency_ratio`: *float*, the consistency ratio of the Compare object
- `random_index`: *'Donegan & Dodd' or 'Saaty'*, the random index used to compute the consistency ratio
- `elements`: *dict*, the elements compared by the Compare object
  - `count`: *int*, the number of elements compared by the Compare object
  - `names`: *list*, the names of the elements compared by the Compare object
- `children`: *dict*, the children of the Compare object; if the Compare object has no children, this value will be `None`
  - `count`: *int*, the number of the Compare object's children
  - `names`: *list*, the names of the Compare object's children
- `comparisons`: *dict*, the comparisons of the Compare object
  - `count`: *int*, the number of comparisons made by the Compare object, not counting reciprocal comparisons
  - `input`: *list*, the comparisons input to the Compare object; each input comparison is a dictionary in which each key is a tuple of two elements and each value is their input pairwise comparison value
    - `[{('a', 'b'): 3}, ...]`
  - `computed`: *list*, the comparisons computed by the Compare object; each computed comparison is a dictionary in which each key is a tuple of two elements and each value is their computed pairwise comparison value; if the Compare object has no computed comparisons, this value will be `None`
    - `[{('c', 'd'): 0.7303}, ...]`

### Compare.add_children()

Compare objects can be linked together to form a hierarchy representing the decision problem. To link Compare objects together into a hierarchy, call `add_children()` on the Compare object intended to form the upper level (the *parent*) and include as an argument a list or tuple of one or more Compare objects intended to form its lower level (the *children*). **In order to properly synthesize the levels of the hierarchy, the `name` of each child object MUST appear as an element in its parent object's input `comparisons` dictionary.**

`Compare.add_children(children)`

- `children`: *list* or *tuple (required)*, the Compare objects that form the lower level of the current Compare object

```python
>>> child1 = ahpy.Compare(name='child1', ...)
>>> child2 = ahpy.Compare(name='child2', ...)

>>> parent = ahpy.Compare(name='parent', comparisons={('child1', 'child2'): 5})
>>> parent.add_children([child1, child2])
```

The global and target weights of the Compare objects in a hierarchy are updated as the hierarchy is constructed: each time `add_children()` is called, the parent object's global weight is set to 1.0 and all of its descendants' global weights are updated accordingly. For this reason, the order in which the hierarchy is constructed is important. While it is possible to construct the hierarchy in any order, **it is best practice to construct the hierarchy beginning with the Compare objects on the lowest level and working up**. This will insure that the global weights of each lower level are always properly computed as the hierarchy is built.

The precision of the target weights are also updated as the hierarchy is constructed: each time `add_children()` is called, the precision of the parent object's target weights is set to equal the lowest precision of its child objects. Because low precision propagates up through the hierarchy, this means that the final target weights will always have the same level of precision as the hierachy's least precise Compare object. This also means that it is possible for the precision of a Compare object's target weights to be different from the precision of its local and global weights.

### Compare.complete()

**If the hierarchy is *not* constructed beginning with the Compare objects on the lowest level and working up, the final step of construction MUST be to call `complete()` on the Compare object at the hierarchy's highest level**. This will insure that both the target weights and the global weights of each Compare object in the hierarchy are correctly computed.

### Missing Pairwise Comparisons

When a Compare object is initialized, the elements forming the keys of the input `comparisons` dictionary are permuted. Permutations of elements that do not contain a value within the input `comparisons` dictionary are then optimally solved for using the cyclic coordinates algorithm described in:

Bozóki, S., Fülöp, J. and Rónyai, L., 'On optimal completion of incomplete pairwise comparison matrices,' *Mathematical and Computer Modelling*, 52:1–2, 2010, pp. 318-333 (DOI: [10.1016/j.mcm.2010.02.047](https://doi.org/10.1016/j.mcm.2010.02.047))

The following example demonstrates this functionality using the matrix below. We first compute the target weights and consistency ratio for the complete matrix, then repeat the process after removing the **(c, d)** entry marked in bold.

||a|b|c|d|
|-|:-:|:-:|:-:|:-:|
|a|1|1|5|2|
|b|1|1|3|4|
|c|1/5|1/3|1|**3/4**|
|d|1/2|1/4|**4/3**|1|

```python
>>> comparisons = {('a', 'b'): 1, ('a', 'c'): 5, ('a', 'd'): 2, ('b', 'c'): 3, ('b', 'd'): 4, ('c', 'd'): 3/4}

>>> complete = ahpy.Compare('complete', comparisons)
>>> print(complete.target_weights)
{'b': 0.3917, 'a': 0.3742, 'd': 0.1349, 'c': 0.0991}
>>> print(complete.consistency_ratio)
0.0372

>>> del comparisons[('c', 'd')]

>>> missing_cd = ahpy.Compare('missing_cd', comparisons)
>>> print(missing_cd.target_weights)
{'b': 0.392, 'a': 0.3738, 'd': 0.1357, 'c': 0.0985}
>>> print(missing_cd.consistency_ratio)
0.0372
```