# AHPy

:construction: UNDER CONSTRUCTION! :construction:

**AHPy** is an implementation of the Analytic Hierarchy Process ([AHP](https://en.wikipedia.org/wiki/Analytic_hierarchy_process)), a method used to structure, synthesize and evaluate the elements of a decision problem. Developed by [Thomas Saaty](http://www.creativedecisions.org/about/ThomasLSaaty.php) in the 1970s, AHP's broad use in fields well beyond that of operational research is a testament to its simple yet powerful combination of psychology and mathematics.

#### Installing AHPy

AHPy is available on the Python Package Index ([PyPI](https://pypi.org/)):

```
python -m pip install ahpy
```

AHPy requires [Python 3.7+](https://www.python.org/), as well as [numpy](https://numpy.org/) and [scipy](https://scipy.org/).

## Table of Contents

#### Examples

[Relative consumption of drinks in the United States](#relative-consumption-of-drinks-in-the-united-states)

[Choosing a leader](#choosing-a-leader)

[Purchasing a vehicle](#purchasing-a-vehicle)

#### Using AHPy

[Terminology](#terminology)

[The Compare Object](#the-compare-object)

[Compare Properties](#compare-properties)

[Compare.add_children()](#compareadd_children)

[Compare.complete()](#comparecomplete)

[Compare.report()](#comparereport)

[Missing Pairwise Comparisons](#missing-pairwise-comparisons)

---

## Examples

The easiest way to learn how to use AHPy is to *see* it used, so this README begins with three worked examples of gradually increasing complexity.

### Relative consumption of drinks in the United States

This example is often used in Saaty's expositions of the AHP as a brief but clear demonstration of the method. I think it's what first opened my eyes to the broad usefulness of the AHP, as well as the wisdom of crowds. If you're unfamiliar with the example, 30 participants were asked to compare the relative consumption of drinks in the United States. The matrix derived from their answers was as follows:

||Coffee|Wine|Tea|Beer|Sodas|Milk|Water|
|-|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|Coffee|1|9|5|2|1|1|1/2|
|Wine|1/9|1|1/3|1/9|1/9|1/9|1/9|
|Tea|1/5|2|1|1/3|1/4|1/3|1/9|
|Beer|1/2|9|3|1|1/2|1|1/3|
|Sodas|1|9|4|2|1|2|1/2|
|Milk|1|9|3|1|1/2|1|1/3|
|Water|2|9|9|3|2|3|1|

The table below shows the relative consumption of drinks as computed using the AHP, given this matrix, together with the *actual* relative consumption of drinks as obtained from U.S. Statistical Abstracts:

||Coffee|Wine|Tea|Beer|Sodas|Milk|Water|
|-|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|AHP|0.177|0.019|0.042|0.116|0.190|0.129|0.327|
|Actual|0.180|0.010|0.040|0.120|0.180|0.140|0.330|

We can recreate this analysis with AHPy using the following code:

```python
>>> drinks = {('coffee', 'wine'): 9, ('coffee', 'tea'): 5, ('coffee', 'beer'): 2, ('coffee', 'soda'): 1, ('coffee', 'milk'): 1, ('coffee', 'water'): 1/2,
('wine', 'tea'): 1/3, ('wine', 'beer'): 1/9, ('wine', 'soda'): 1/9, ('wine', 'milk'): 1/9, ('wine', 'water'): 1/9,
('tea', 'beer'): 1/3, ('tea', 'soda'): 1/4, ('tea', 'milk'): 1/3, ('tea', 'water'): 1/9,
('beer', 'soda'): 1/2, ('beer', 'milk'): 1, ('beer', 'water'): 1/3,
('soda', 'milk'): 2, ('soda', 'water'): 1/2,
('milk', 'water'): 1/3}

>>> c = ahpy.Compare(name='Drinks', comparisons=drinks, precision=3, random_index='saaty')

>>> print(c.target_weights)
{'water': 0.327, 'soda': 0.19, 'coffee': 0.177, 'milk': 0.129, 'beer': 0.116, 'tea': 0.042, 'wine': 0.019}

>>> print(c.consistency_ratio)
0.022
```

First, we create a dictionary of pairwise comparisons using the values from the matrix. We then create a Compare object, giving it a unique name and the dictionary we just made (we also change the precision and random index so that the results match those given by Saaty). Finally, we print the Compare object's target weights and consistency ratio to see the results of our analysis. Brilliant!

### Choosing a leader

This example can be found [as an appendix to the Wikipedia entry for AHPy](https://en.wikipedia.org/wiki/Analytic_hierarchy_process_%E2%80%93_leader_example). The names have been changed both to freshen things up as well as to reference [a blast from the past](https://www.grammarphobia.com/blog/2009/06/tom-dick-and-harry-part-2.html), though the input comparison values remain the same. In some cases, AHPy's results will not match those on the Wikipedia page: this is due to the imprecision of the method used to compute the values shown in the Wikipedia example, not an error in AHPy.

We'll be judging candidates by their experience, education, charisma and age. Therefore, we need to compare each potential leader to the others, given each criteria:

```python
>>> experience_comparisons = {('Moll', 'Nell'): 1/4, ('Moll', 'Sue'): 4, ('Nell', 'Sue'): 9}
>>> education_comparisons = {('Moll', 'Nell'): 3, ('Moll', 'Sue'): 1/5, ('Nell', 'Sue'): 1/7}
>>> charisma_comparisons = {('Moll', 'Nell'): 5, ('Moll', 'Sue'): 9, ('Nell', 'Sue'): 4}
>>> age_comparisons = {('Moll', 'Nell'): 1/3, ('Moll', 'Sue'): 5, ('Nell', 'Sue'): 9}
```

After that, we'll need to compare the importance of each criteria to the others:

```python
>>> criteria_comparisons = {('Experience', 'Education'): 4, ('Experience', 'Charisma'): 3, ('Experience', 'Age'): 7,
('Education', 'Charisma'): 1/3, ('Education', 'Age'): 3,
('Charisma', 'Age'): 5}
```

Now that we've created all of the necessary pairwise comparison dictionaries, we can create their corresponding Compare objects:

```python
>>> experience = ahpy.Compare('Experience', experience_comparisons, precision=3, random_index='saaty')
>>> education = ahpy.Compare('Education', education_comparisons, precision=3, random_index='saaty')
>>> charisma = ahpy.Compare('Charisma', charisma_comparisons, precision=3, random_index='saaty')
>>> age = ahpy.Compare('Age', age_comparisons, precision=3, random_index='saaty')
>>> criteria = ahpy.Compare('Criteria', criteria_comparisons, precision=3, random_index='saaty')
```

Notice that the names of the `experience`, `education`, `charisma` and `age` Compare objects are repeated in the `criteria_comparisons` dictionary above. This is necessary in order to properly link the Compare objects together into a hierarchy, as shown next.

In the final step, we need to link the Compare objects together into a hierarchy, such that `criteria` is the parent object and the other objects are its children:

```python
>>> criteria.add_children([experience, education, charisma, age])
```

Now that the hierarchy represents the decision problem, we can print the target weights of the `criteria` object to see the results of the analysis:

```python
>>> print(criteria.target_weights)
{'Nell': 0.493, 'Moll': 0.358, 'Sue': 0.15}
```

If we wanted to, we could also print the weights and consistency ratio of any of the other Compare objects:

```python
>>> print(experience.local_weights)
{'Nell': 0.717, 'Moll': 0.217, 'Sue': 0.066}
>>> print(experience.consistency_ratio)
0.035
>>> print(education.local_weights)
{'Sue': 0.731, 'Moll': 0.188, 'Nell': 0.081}
>>> print(education.consistency_ratio)
0.062
```

We could also call `report()` on a Compare object to learn more detailed information:

```python
>>> report = criteria.report(show=True)
{
    "name": "Criteria",
    "weight": 1.0,
    "target": {
        "Nell": 0.493,
        "Moll": 0.358,
        "Sue": 0.15
    },
    "weights": {
        "local": {
            "Experience": 0.548,
            "Charisma": 0.27,
            "Education": 0.127,
            "Age": 0.056
        },
        "global": {
            "Experience": 0.548,
            "Charisma": 0.27,
            "Education": 0.127,
            "Age": 0.056
        }
    },
    "consistency_ratio": 0.044,
    "random_index": "Saaty",
    "elements": {
        "count": 4,
        "names": [
            "Experience",
            "Education",
            "Charisma",
            "Age"
        ]
    },
    "children": {
        "count": 4,
        "names": [
            "Experience",
            "Education",
            "Charisma",
            "Age"
        ]
    },
    "comparisons": {
        "count": 6,
        "input": [
            {
                "Experience, Education": 4
            },
            {
                "Experience, Charisma": 3
            },
            {
                "Experience, Age": 7
            },
            {
                "Education, Charisma": 0.333
            },
            {
                "Education, Age": 3
            },
            {
                "Charisma, Age": 5
            }
        ],
        "computed": null
    }
}
```

In this case, `report` contains a Python dictionary, while `show=True` prints the same information to the console in JSON format.

### Purchasing a vehicle

## Using AHPy

### Terminology

describe "target", 'element', 'value'

https://www.edx.org/course/valoracion-de-futbolistas-con-el-metodo-ahp

### The Compare Object

The Compare class computes the priority vector and consistency ratio of a positive reciprocal matrix, created using an input dictionary of pairwise comparison values. Optimal values are computed for any missing pairwise comparisons. Compare objects can also be [linked together to form a hierarchy](#compareadd_children) representing the decision problem: global problem elements are then derived by synthesizing all levels of the hierarchy.

`Compare(name, comparisons, precision=4, random_index='dd', iterations=100, tolerance=0.0001, cr=True)`

- `name`: *str (required)*, the name of the Compare object
  - This property is used to link a child object to its parent and must be unique

- `comparisons`: *dict (required)*, the elements and values to be compared, provided in one of two forms:
  1. A dictionary of pairwise comparisons, in which each key is a tuple of two elements and each value is their pairwise comparison value
      - `{('a', 'b'): 3, ('b', 'c'): 2, ('a', 'c'): 5}`
      - **The order of the elements in the key matters: the comparison `('a', 'b'): 3` means "a is moderately more important than b"**
  2. A dictionary of measured values, in which each key is a single element and each value is that element's measured value
      - `{'a': 1.2, 'b': 2.3, 'c': 3.4}`
      - Given this form, AHPy will automatically create a consistent priority vector of normalized values

- `precision`: *int*, the number of decimal places to take into account when computing both the priority vector and the consistency ratio of the Compare object
  - The default precision value is 4

- `random_index`: *'dd'* or *'saaty'*, the set of random index estimates used to compute the priority vector's consistency ratio
  - 'dd' uses estimates from Donegan, H.A. and Dodd, F.J., 'A Note on Saaty's Random Indexes,' *Mathematical and Computer Modelling*, 15:10, 1991, pp. 135-137 (DOI: [10.1016/0895-7177(91)90098-R](https://doi.org/10.1016/0895-7177(91)90098-R))
    - 'dd' supports the computation of consistency ratios for matrices less than or equal to 100 &times; 100 in size
  - 'saaty' uses estimates from Saaty, T., *Theory And Applications Of The Analytic Network Process*, Pittsburgh: RWS Publications, 2005, p. 31
    - 'saaty' supports the computation of consistency ratios for matrices less than or equal to 15 &times; 15 in size
  - The default random index is 'dd'

- `iterations`: *int*, the stopping criterion for the algorithm used to compute the Compare object's priority vector
  - If a priority vector has not been determined after this number of iterations, the algorithm stops and the last principal eigenvector to be computed is assigned as the priority vector
  - The default number of iterations is 100

- `tolerance`: *float*, the stopping criterion for the cycling coordinates algorithm used to compute the optimal value of missing pairwise comparisons
  - The algorithm stops when the difference between the norms of two cycles of coordinates is less than this value
  - The default tolerance value is 0.0001

- `cr`: *bool*, whether to compute the priority vector's consistency ratio
  - Set `cr=False` to compute the priority vector of a matrix when a consistency ratio cannot be determined due to the size of the matrix
  - The default value is True

### Compare Properties

`consistency_ratio`
`local_weights`
`global_weights`
same as local weight if only object in hierarchy
`target_weights`

may not add up to 1 due to rounding

### Compare.add_children()

Compare objects can be linked together to form a hierarchy representing the decision problem. To link Compare objects together into a hierarchy, call `add_children()` on the Compare object intended to form the *upper* level (the *parent*) and include as an argument a list or tuple of one or more Compare objects intended to form its *lower* level (the *children*). **In order to properly synthesize the levels of the hierarchy, the `name` of each child object MUST appear as an element in its parent object's input `comparisons` dictionary.**

`Compare.add_children(children)`

- `children`: *list* or *tuple (required)*, the Compare objects that will form the lower level of the current Compare object

```python
>>> child1 = ahpy.Compare(name='child1', ...)
>>> child2 = ahpy.Compare(name='child2', ...)

>>> parent = ahpy.Compare(name='parent', comparisons={('child1', 'child2'): 5})
>>> parent.add_children([child1, child2])
```

The global and target weights of the Compare objects in a hierarchy are updated as the hierarchy is constructed: each time `add_children()` is called, the parent object's global weight is set to 1.0 and all of its descendants' global weights are updated accordingly. For this reason, the order in which the hierarchy is constructed is important. While it is possible to construct the hierarchy in any order, **it is best practice to construct the hierarchy beginning with the Compare objects on the lowest level and working up**. This will insure that the global weights of each lower level are always properly computed as the hierarchy is built.

The precision of the target weights are also updated as the hierarchy is constructed: each time `add_children()` is called, the precision of the parent object's target weights is set to equal the lowest precision of its child objects. Because lower precision propagates up through the hierarchy, the final target weights will always have the same level of precision as the hierachy's least precise Compare object. This also means that it is possible for the precision of a Compare object's target weights to be different from the precision of its local and global weights.

### Compare.complete()

**If the hierarchy is *not* constructed beginning with the Compare objects on the lowest level and working up, the final step of construction MUST be to call `complete()` on the Compare object at the hierarchy's highest level**. This will insure that both the target weights and the global weights of each Compare object in the hierarchy are correctly computed.

### Compare.report()

A report on the details of each Compare object is available. To return the report as a dictionary, call `report()` on the Compare object; to simultaneously print the information to the console in JSON format, set `show=True`.

`Compare.report(show=False)`

- `show`: *bool*, whether to print the report to the console in JSON format
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
  - `count`: *int*, the number of comparisons made by the Compare object, **not counting reciprocal comparisons**
  - `input`: *dict*, the comparisons input to the Compare object; this is identical to the input `comparisons` dictionary
  - `computed`: *dict*, the comparisons computed by the Compare object; each key is a tuple of two elements and each value is their computed pairwise comparison value; if the Compare object has no computed comparisons, this value will be `None`
    - `{('c', 'd'): 0.730297106886979}, ...}`

### Missing Pairwise Comparisons

When a Compare object is initialized, the elements forming the keys of the input `comparisons` dictionary are permuted. Permutations of elements that do not contain a value within the input `comparisons` dictionary are then optimally solved for using the cyclic coordinates algorithm described in Bozóki, S., Fülöp, J. and Rónyai, L., 'On optimal completion of incomplete pairwise comparison matrices,' *Mathematical and Computer Modelling*, 52:1–2, 2010, pp. 318-333 (DOI: [10.1016/j.mcm.2010.02.047](https://doi.org/10.1016/j.mcm.2010.02.047)).

The following example demonstrates this functionality using the matrix below. We first compute the target weights and consistency ratio for the complete matrix, then repeat the process after removing the **(c, d)** comparison marked in bold.

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