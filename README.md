# AHPy

:construction: UNDER CONSTRUCTION! :construction:

**AHPy** is an implementation of the Analytic Hierarchy Process (AHP), a method used to structure, synthesize and evaluate the elements of a decision problem. Developed by [Thomas Saaty](http://www.creativedecisions.org/about/ThomasLSaaty.php) in the 1970s, AHP's broad use in fields well beyond that of operational research is a testament to its simple yet powerful combination of psychology and mathematics.

#### Installing AHPy

AHPy is available on the Python Package Index ([PyPI](https://pypi.org/)):

```
python -m pip install ahpy
```

AHPy requires [Python 3.7+](https://www.python.org/), as well as [numpy](https://numpy.org/) and [scipy](https://scipy.org/).

## Using AHPy

### Compare()

The Compare class computes the priority vector and consistency ratio of a positive reciprocal matrix, created using an input dictionary of pairwise comparison values. Optimal values are computed for any missing pairwise comparisons. Compare objects can be linked together to form a hierarchy representing the decision problem: global problem solutions are then derived by synthesizing all levels of the hierarchy.

`Compare(name, comparisons, precision=4, random_index='dd', iterations=100, tolerance=0.0001, cr=True)`

- `name`: *str*, the name of the Compare object

  - This property is used to link a child object to its parent and must be unique.

- `comparisons`: *dict*, the elements and values to be compared

  - The dictionary can be provided in one of two forms:

    1. A dictionary of pairwise comparisons, in which each key is a tuple of two elements and each value is their pairwise comparison value
        - `{('a', 'b'): 3, ('b', 'c'): 2, ('a', 'c'): 5}`
        - The comparison `('a', 'b'): 3` means "a is moderately more important than b"
    2. A dictionary of measured values, in which each key is a single element and each value is that element's measured value
      - `{'a': 1.2, 'b': 2.3, 'c': 3.4}`
      - AHPy automatically creates a priority vector of normalized values, given this form

- `precision`: *int*, the number of decimal places to consider when computing both the priority vector and the consistency ratio
- `random_index`: *'dd' or 'saaty'*, the set of random index estimates used to compute the priority vector's consistency ratio
- `iterations`: *int*, the stopping criteria for the algorithm used to compute the priority vector; the algorithm stops when the number of iterations is equal to this value
- `tolerance`: *float*, the stopping criteria for the cycling coordinates algorithm used to compute the optimal value of missing pairwise comparisons; the algorithm stops when the difference between the norms of two cycles of coordinates is less than this value
- `cr`: *bool*, an override to compute the object's priority vector when a consistency ratio cannot be determined due to the size of the matrix



permutations

missing values

Optimally completes an incomplete pairwise comparison matrix according to the cyclic coordinates algorithm described in
        Bozóki, S., Fülöp, J. and Rónyai, L., 'On optimal completion of incomplete pairwise comparison matrices,'
        Mathematical and Computer Modelling, 52:1–2, 2010, pp. 318-333. (https://doi.org/10.1016/j.mcm.2010.02.047)
        

precision
target differs from node's local/global

Random indices
Sets the 'consistency_ratio' property of the Compare object, using random index estimates from
        Donegan and Dodd's 'A note on Saaty's Random Indexes' in Mathematical and Computer Modelling,
        15:10, 1991, pp. 135-137 (doi: 10.1016/0895-7177(91)90098-R) by default (random_index='dd').
        If the random index of the object equals 'saaty', uses the estimates from
        Saaty's Theory And Applications Of The Analytic Network Process, Pittsburgh: RWS Publications, 2005, p. 31.
        
link to paper
when to use saaty

iterations

tolerance

cr override
saaty <= 15
dd <= 100


### add_children()

how to link in a hierarchy
names
order

add_children()


### complete()

### report()

complete()

report()
structure
json
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
