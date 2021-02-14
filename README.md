# AHPy

**AHPy** is an implementation of the Analytic Hierarchy Process (AHP), a method for structuring, synthesizing and evaluating the elements of a decision problem. Developed by Thomas Saaty in the 1970s, AHP's broad use in fields well beyond that of operational research is a testament to its simple yet powerful combination of psychology and mathematics.

The amount of available information on the AHP and its uses is legion. For a lovingly constructed and gentle tutorial, I recommend [Kardi Teknomo's 2006 Analytic Hierarchy Process (AHP) Tutorial](https://people.revoledu.com/kardi/tutorial/AHP/AHP.htm).
If you'd prefer to watch a video on the subject, I recommend Klaus Göpel's [Analytic Hierarchy Process AHP - Business Performance Management](https://www.youtube.com/watch?v=18GWVtVAAzs).
And, of course, there's always [Wikipedia](https://en.wikipedia.org/wiki/Analytic_hierarchy_process).

### Installing AHPy

AHPy is available on the Python Package Index (PyPI):

```
python -m pip install ahpy
```

AHPy requires [Python 3.7+](https://www.python.org/), as well as [numpy](https://numpy.org/) and [scipy](https://scipy.org/).


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


how to link in a hierarchy
names
order
complete()

how comparisons work
permutations
(a, b): 2 implies a over (?) b by 2
normalizing by values
missing values
link to paper
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

add_children()

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

checks for values over 0 and that all values are numeric
