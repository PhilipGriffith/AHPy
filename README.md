# AHPy

**AHPy** is an implementation of the Analytic Hierarchy Process ([AHP](https://en.wikipedia.org/wiki/Analytic_hierarchy_process)), a method used to structure, synthesize and evaluate the elements of a decision problem. Developed by [Thomas Saaty](http://www.creativedecisions.org/about/ThomasLSaaty.php) in the 1970s, AHP's broad use in fields well beyond that of operational research is a testament to its simple yet powerful combination of psychology and mathematics.

 AHPy attempts to provide a library that is not only simple to use, but also capable of intuitively working within the numerous conceptual frameworks to which the AHP can be applied. For this reason, general terms have been preferred to more specific ones within the programming interface.

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

[Purchasing a vehicle reprised: normalized weights and the Compose class](#purchasing-a-vehicle-reprised-normalized-weights-and-the-compose-class)


#### Details

[The Compare Class](#the-compare-class)

[Compare.add_children()](#compareadd_children)

[Compare.report()](#comparereport)

[The Compose Class](#the-compose-class)

[Compose.add_comparisons()](#composeadd_comparisons)

[Compose.add_hierarchy()](#composeadd_hierarchy)

[Compose.report()](#composereport)

[A Note on Weights](#a-note-on-weights)

[Missing Pairwise Comparisons](#missing-pairwise-comparisons)

[Development and Testing](#development-and-testing)

---

## Examples

The easiest way to learn how to use AHPy is to *see* it used, so this README begins with worked examples of gradually increasing complexity.

### Relative consumption of drinks in the United States

This example is often used in Saaty's expositions of the AHP as a brief but clear demonstration of the method; it's what first opened my eyes to the broad usefulness of the AHP (as well as the wisdom of crowds!). The version I'm using here is from his 2008 article '[Decision making with the analytic hierarchy process](https://doi.org/10.1504/IJSSCI.2008.017590)'. If you're unfamiliar with the example, 30 participants were asked to compare the relative consumption of drinks in the United States. For instance, they believed that coffee was consumed *much* more than wine, but at the same rate as milk. The matrix derived from their answers was as follows:

||Coffee|Wine|Tea|Beer|Soda|Milk|Water|
|-|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|Coffee|1|9|5|2|1|1|1/2|
|Wine|1/9|1|1/3|1/9|1/9|1/9|1/9|
|Tea|1/5|3|1|1/3|1/4|1/3|1/9|
|Beer|1/2|9|3|1|1/2|1|1/3|
|Soda|1|9|4|2|1|2|1/2|
|Milk|1|9|3|1|1/2|1|1/3|
|Water|2|9|9|3|2|3|1|

The table below shows the relative consumption of drinks as computed using the AHP, given this matrix, together with the *actual* relative consumption of drinks as obtained from U.S. Statistical Abstracts:

|:exploding_head:|Coffee|Wine|Tea|Beer|Soda|Milk|Water|
|-|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|AHP|0.177|0.019|0.042|0.116|0.190|0.129|0.327|
|Actual|0.180|0.010|0.040|0.120|0.180|0.140|0.330|

We can recreate this analysis with AHPy using the following code:

```python
>>> drink_comparisons = {('coffee', 'wine'): 9, ('coffee', 'tea'): 5, ('coffee', 'beer'): 2, ('coffee', 'soda'): 1,
						 ('coffee', 'milk'): 1, ('coffee', 'water'): 1 / 2,
                         ('wine', 'tea'): 1 / 3, ('wine', 'beer'): 1 / 9, ('wine', 'soda'): 1 / 9,
                         ('wine', 'milk'): 1 / 9, ('wine', 'water'): 1 / 9,
                         ('tea', 'beer'): 1 / 3, ('tea', 'soda'): 1 / 4, ('tea', 'milk'): 1 / 3,
                         ('tea', 'water'): 1 / 9,
                         ('beer', 'soda'): 1 / 2, ('beer', 'milk'): 1, ('beer', 'water'): 1 / 3,
                         ('soda', 'milk'): 2, ('soda', 'water'): 1 / 2,
                         ('milk', 'water'): 1 / 3}

>>> drinks = ahpy.Compare(name='Drinks', comparisons=drink_comparisons, precision=3, random_index='saaty')

>>> print(drinks.target_weights)
{'water': 0.327, 'soda': 0.19, 'coffee': 0.177, 'milk': 0.129, 'beer': 0.116, 'tea': 0.042, 'wine': 0.019}

>>> print(drinks.consistency_ratio)
0.022
```

1. First, we create a dictionary of pairwise comparisons using the values from the matrix above.<br>
2. We then create a **Compare** object, initializing it with a unique name and the dictionary we just made. We also change the precision and random index so that the results match those provided by Saaty.<br>
3. Finally, we print the Compare object's target weights and consistency ratio to see the results of our analysis.

Brilliant!

### Choosing a leader

This example can be found [in an appendix to the Wikipedia entry for AHP](https://en.wikipedia.org/wiki/Analytic_hierarchy_process_-_leader_example). The names have been changed in a nod to [the original saying](https://www.grammarphobia.com/blog/2009/06/tom-dick-and-harry-part-2.html), but the input comparison values remain the same.

#### N.B.

You may notice that in some cases AHPy's results will not match those on the Wikipedia page. This is not an error in AHPy's calculations, but rather a result of [the method used to compute the values shown in the Wikipedia examples](https://en.wikipedia.org/wiki/Analytic_hierarchy_process_–_car_example#Pairwise_comparing_the_criteria_with_respect_to_the_goal):

> You can duplicate this analysis at this online demonstration site...**IMPORTANT: The demo site is designed for convenience, not accuracy. The priorities it returns may differ somewhat from those returned by rigorous AHP calculations.**

In this example, we'll be judging job candidates by their experience, education, charisma and age. Therefore, we need to compare each potential leader to the others, given each criterion...

```python
>>> experience_comparisons = {('Moll', 'Nell'): 1/4, ('Moll', 'Sue'): 4, ('Nell', 'Sue'): 9}
>>> education_comparisons = {('Moll', 'Nell'): 3, ('Moll', 'Sue'): 1/5, ('Nell', 'Sue'): 1/7}
>>> charisma_comparisons = {('Moll', 'Nell'): 5, ('Moll', 'Sue'): 9, ('Nell', 'Sue'): 4}
>>> age_comparisons = {('Moll', 'Nell'): 1/3, ('Moll', 'Sue'): 5, ('Nell', 'Sue'): 9}
```

...as well as compare the importance of each criterion to the others:

```python
>>> criteria_comparisons = {('Experience', 'Education'): 4, ('Experience', 'Charisma'): 3, ('Experience', 'Age'): 7,
							('Education', 'Charisma'): 1/3, ('Education', 'Age'): 3,
							('Charisma', 'Age'): 5}
```

Before moving on, it's important to note that the *order* of the elements that form the dictionaries' keys is meaningful. For example, using Saaty's scale, the comparison `('Experience', 'Education'): 4` means that "Experience is *moderately+ more important than* Education." 

Now that we've created all of the necessary pairwise comparison dictionaries, we'll create their corresponding Compare objects and use the dictionaries as input:

```python
>>> experience = ahpy.Compare('Experience', experience_comparisons, precision=3, random_index='saaty')
>>> education = ahpy.Compare('Education', education_comparisons, precision=3, random_index='saaty')
>>> charisma = ahpy.Compare('Charisma', charisma_comparisons, precision=3, random_index='saaty')
>>> age = ahpy.Compare('Age', age_comparisons, precision=3, random_index='saaty')
>>> criteria = ahpy.Compare('Criteria', criteria_comparisons, precision=3, random_index='saaty')
```

Notice that the names of the Experience, Education, Charisma and Age objects are repeated in the `criteria_comparisons` dictionary above. This is necessary in order to properly link the Compare objects together into a hierarchy, as shown next.

In the final step, we need to link the Compare objects together into a hierarchy, such that Criteria is the *parent* object and the other objects form its *children*:

```python
>>> criteria.add_children([experience, education, charisma, age])
```

Now that the hierarchy represents the decision problem, we can print the target weights of the parent Criteria object to see the results of the analysis:

```python
>>> print(criteria.target_weights)
{'Nell': 0.493, 'Moll': 0.358, 'Sue': 0.15}
```

We can also print the local and global weights of the elements within any of the other Compare objects, as well as the consistency ratio of their comparisons:

```python
>>> print(experience.local_weights)
{'Nell': 0.717, 'Moll': 0.217, 'Sue': 0.066}
>>> print(experience.consistency_ratio)
0.035

>>> print(education.global_weights)
{'Sue': 0.093, 'Moll': 0.024, 'Nell': 0.01}
>>> print(education.consistency_ratio)
0.062
```

The global and local weights of the Compare objects themselves are likewise available:

```python
>>> print(experience.global_weight)
0.548

>>> print(education.local_weight)
0.127
```

Calling `report()` on a Compare object provides a standard way to learn information about the object. In the code below, the variable `report` contains a [Python dictionary](#comparereport) of important information, while the `show=True` argument prints the same information to the console in JSON format:

```python
>>> report = criteria.report(show=True)
{
    "Criteria": {
        "global_weight": 1.0,
        "local_weight": 1.0,
        "target_weights": {
            "Nell": 0.493,
            "Moll": 0.358,
            "Sue": 0.15
        },
        "elements": {
            "global_weights": {
                "Experience": 0.548,
                "Charisma": 0.27,
                "Education": 0.127,
                "Age": 0.056
            },
            "local_weights": {
                "Experience": 0.548,
                "Charisma": 0.27,
                "Education": 0.127,
                "Age": 0.056
            },
            "consistency_ratio": 0.044
        }
    }
}
```

### Purchasing a vehicle

This example can also be found [in an appendix to the Wikipedia entry for AHP](https://en.wikipedia.org/wiki/Analytic_hierarchy_process_–_car_example). Like before, in some cases AHPy's results will not match those on the Wikipedia page, even though the input comparison values are identical. To reiterate, this is due to a difference in methods, not an error in AHPy.

In this example, we'll be choosing a vehicle to purchase based on its cost, safety, style and capacity. Cost will further depend on a combination of the vehicle's purchase price, fuel costs, maintenance costs and resale value; capacity will depend on a combination of the vehicle's cargo and passenger capacity.

First, we compare the high-level criteria to one another:

```python
>>> criteria_comparisons = {('Cost', 'Safety'): 3, ('Cost', 'Style'): 7, ('Cost', 'Capacity'): 3,
							('Safety', 'Style'): 9, ('Safety', 'Capacity'): 1,
							('Style', 'Capacity'): 1/7}
```

If we create a Compare object for the criteria, we can view its report:

```python
>>> criteria = ahpy.Compare('Criteria', criteria_comparisons, precision=3)
>>> report = criteria.report(show=True)
{
    "Criteria": {
        "global_weight": 1.0,
        "local_weight": 1.0,
        "target_weights": {
            "Cost": 0.51,
            "Safety": 0.234,
            "Capacity": 0.215,
            "Style": 0.041
        },
        "elements": {
            "global_weights": {
                "Cost": 0.51,
                "Safety": 0.234,
                "Capacity": 0.215,
                "Style": 0.041
            },
            "local_weights": {
                "Cost": 0.51,
                "Safety": 0.234,
                "Capacity": 0.215,
                "Style": 0.041
            },
            "consistency_ratio": 0.08
        }
    }
}
```

Next, we compare the *sub*criteria of Cost to one another...

```python
>>> cost_comparisons = {('Price', 'Fuel'): 2, ('Price', 'Maintenance'): 5, ('Price', 'Resale'): 3,
						('Fuel', 'Maintenance'): 2, ('Fuel', 'Resale'): 2,
						('Maintenance', 'Resale'): 1/2}
```

...as well as the subcriteria of Capacity:

```python
>>> capacity_comparisons = {('Cargo', 'Passenger'): 1/5}
```

We also need to compare each of the potential vehicles to the others, given each criterion. We'll begin by building a list of all possible two-vehicle combinations:

```python
>>> import itertools
>>> vehicles = ('Accord Sedan', 'Accord Hybrid', 'Pilot', 'CR-V', 'Element', 'Odyssey')
>>> vehicle_pairs = list(itertools.combinations(vehicles, 2))
>>> print(vehicle_pairs)
[('Accord Sedan', 'Accord Hybrid'), ('Accord Sedan', 'Pilot'), ('Accord Sedan', 'CR-V'), ('Accord Sedan', 'Element'), ('Accord Sedan', 'Odyssey'), ('Accord Hybrid', 'Pilot'), ('Accord Hybrid', 'CR-V'), ('Accord Hybrid', 'Element'), ('Accord Hybrid', 'Odyssey'), ('Pilot', 'CR-V'), ('Pilot', 'Element'), ('Pilot', 'Odyssey'), ('CR-V', 'Element'), ('CR-V', 'Odyssey'), ('Element', 'Odyssey')]
```

Then we can simply zip together the vehicle pairs and their pairwise comparison values for each criterion:

```python
>>> price_values = (9, 9, 1, 1/2, 5, 1, 1/9, 1/9, 1/7, 1/9, 1/9, 1/7, 1/2, 5, 6)
>>> price_comparisons = dict(zip(vehicle_pairs, price_values))
>>> print(price_comparisons)
{('Accord Sedan', 'Accord Hybrid'): 9, ('Accord Sedan', 'Pilot'): 9, ('Accord Sedan', 'CR-V'): 1, ('Accord Sedan', 'Element'): 0.5, ('Accord Sedan', 'Odyssey'): 5, ('Accord Hybrid', 'Pilot'): 1, ('Accord Hybrid', 'CR-V'): 0.1111111111111111, ('Accord Hybrid', 'Element'): 0.1111111111111111, ('Accord Hybrid', 'Odyssey'): 0.14285714285714285, ('Pilot', 'CR-V'): 0.1111111111111111, ('Pilot', 'Element'): 0.1111111111111111, ('Pilot', 'Odyssey'): 0.14285714285714285, ('CR-V', 'Element'): 0.5, ('CR-V', 'Odyssey'): 5, ('Element', 'Odyssey'): 6}

>>> safety_values = (1, 5, 7, 9, 1/3, 5, 7, 9, 1/3, 2, 9, 1/8, 2, 1/8, 1/9)
>>> safety_comparisons = dict(zip(vehicle_pairs, safety_values))

>>> passenger_values = (1, 1/2, 1, 3, 1/2, 1/2, 1, 3, 1/2, 2, 6, 1, 3, 1/2, 1/6)
>>> passenger_comparisons = dict(zip(vehicle_pairs, passenger_values))

>>> fuel_values = (1/1.13, 1.41, 1.15, 1.24, 1.19, 1.59, 1.3, 1.4, 1.35, 1/1.23, 1/1.14, 1/1.18, 1.08, 1.04, 1/1.04)
>>> fuel_comparisons = dict(zip(vehicle_pairs, fuel_values))

>>> resale_values = (3, 4, 1/2, 2, 2, 2, 1/5, 1, 1, 1/6, 1/2, 1/2, 4, 4, 1)
>>> resale_comparisons = dict(zip(vehicle_pairs, resale_values))

>>> maintenance_values = (1.5, 4, 4, 4, 5, 4, 4, 4, 5, 1, 1.2, 1, 1, 3, 2)
>>> maintenance_comparisons = dict(zip(vehicle_pairs, maintenance_values))

>>> style_values = (1, 7, 5, 9, 6, 7, 5, 9, 6, 1/6, 3, 1/3, 7, 5, 1/5)
>>> style_comparisons = dict(zip(vehicle_pairs, style_values))

>>> cargo_values = (1, 1/2, 1/2, 1/2, 1/3, 1/2, 1/2, 1/2, 1/3, 1, 1, 1/2, 1, 1/2, 1/2)
>>> cargo_comparisons = dict(zip(vehicle_pairs, cargo_values))
```

Now that we've created all of the necessary pairwise comparison dictionaries, we can create their corresponding Compare objects:

```python
>>> cost = ahpy.Compare('Cost', cost_comparisons, precision=3)
>>> capacity = ahpy.Compare('Capacity', capacity_comparisons, precision=3)
>>> price = ahpy.Compare('Price', price_comparisons, precision=3)
>>> safety = ahpy.Compare('Safety', safety_comparisons, precision=3)
>>> passenger = ahpy.Compare('Passenger', passenger_comparisons, precision=3)
>>> fuel = ahpy.Compare('Fuel', fuel_comparisons, precision=3)
>>> resale = ahpy.Compare('Resale', resale_comparisons, precision=3)
>>> maintenance = ahpy.Compare('Maintenance', maintenance_comparisons, precision=3)
>>> style = ahpy.Compare('Style', style_comparisons, precision=3)
>>> cargo = ahpy.Compare('Cargo', cargo_comparisons, precision=3)
```

The final step is to link all of the Compare objects into a hierarchy. First, we'll make the Price, Fuel, Maintenance and Resale objects the children of the Cost object...

```python
>>> cost.add_children([price, fuel, maintenance, resale])
```

...and do the same to link the Cargo and Passenger objects to the Capacity object...

```python
>>> capacity.add_children([cargo, passenger])
```

...then finally make the Cost, Safety, Style and Capacity objects the children of the Criteria object:

```python
>>> criteria.add_children([cost, safety, style, capacity])
```

Now that the hierarchy represents the decision problem, we can print the target weights of the *highest level* Criteria object to see the results of the analysis:

```python
>>> print(criteria.target_weights)
{'Odyssey': 0.219, 'Accord Sedan': 0.215, 'CR-V': 0.167, 'Accord Hybrid': 0.15, 'Element': 0.144, 'Pilot': 0.106}
```

For detailed information about any of the Compare objects in the hierarchy, we can call that object's `report()` with the `verbose=True` argument:

```python
>>> report = criteria.report(show=True, verbose=True)
{
    "name": "Criteria",
    "global_weight": 1.0,
    "local_weight": 1.0,
    "target_weights": {
        "Odyssey": 0.219,
        "Accord Sedan": 0.215,
        "CR-V": 0.167,
        "Accord Hybrid": 0.15,
        "Element": 0.144,
        "Pilot": 0.106
    },
    "elements": {
        "global_weights": {
            "Cost": 0.51,
            "Safety": 0.234,
            "Capacity": 0.215,
            "Style": 0.041
        },
        "local_weights": {
            "Cost": 0.51,
            "Safety": 0.234,
            "Capacity": 0.215,
            "Style": 0.041
        },
        "consistency_ratio": 0.08,
        "random_index": "Donegan & Dodd",
        "count": 4,
        "names": [
            "Cost",
            "Safety",
            "Style",
            "Capacity"
        ]
    },
    "children": {
        "count": 4,
        "names": [
            "Cost",
            "Safety",
            "Style",
            "Capacity"
        ]
    },
    "comparisons": {
        "count": 6,
        "input": {
            "Cost, Safety": 3,
            "Cost, Style": 7,
            "Cost, Capacity": 3,
            "Safety, Style": 9,
            "Safety, Capacity": 1,
            "Style, Capacity": 0.14285714285714285
        },
        "computed": null
    }
}
```

Calling `report(show=True, verbose=True)` on Compare objects at lower levels of the hierarchy will provide different information, depending on the level they're in:

```python
>>> report = cost.report(show=True, verbose=True)
{
    "name": "Cost",
    "global_weight": 0.51,
    "local_weight": 0.51,
    "target_weights": null,
    "elements": {
        "global_weights": {
            "Price": 0.249,
            "Fuel": 0.129,
            "Resale": 0.082,
            "Maintenance": 0.051
        },
        "local_weights": {
            "Price": 0.488,
            "Fuel": 0.252,
            "Resale": 0.161,
            "Maintenance": 0.1
        },
        "consistency_ratio": 0.016,
        "random_index": "Donegan & Dodd",
        "count": 4,
        "names": [
            "Price",
            "Fuel",
            "Maintenance",
            "Resale"
        ]
    },
    "children": {
        "count": 4,
        "names": [
            "Price",
            "Fuel",
            "Resale",
            "Maintenance"
        ]
    },
    "comparisons": {
        "count": 6,
        "input": {
            "Price, Fuel": 2,
            "Price, Maintenance": 5,
            "Price, Resale": 3,
            "Fuel, Maintenance": 2,
            "Fuel, Resale": 2,
            "Maintenance, Resale": 0.5
        },
        "computed": null
    }
}

>>> report = price.report(show=True, verbose=True)
{
    "name": "Price",
    "global_weight": 0.249,
    "local_weight": 0.488,
    "target_weights": null,
    "elements": {
        "global_weights": {
            "Element": 0.091,
            "Accord Sedan": 0.061,
            "CR-V": 0.061,
            "Odyssey": 0.023,
            "Accord Hybrid": 0.006,
            "Pilot": 0.006
        },
        "local_weights": {
            "Element": 0.366,
            "Accord Sedan": 0.246,
            "CR-V": 0.246,
            "Odyssey": 0.093,
            "Accord Hybrid": 0.025,
            "Pilot": 0.025
        },
        "consistency_ratio": 0.072,
        "random_index": "Donegan & Dodd",
        "count": 6,
        "names": [
            "Accord Sedan",
            "Accord Hybrid",
            "Pilot",
            "CR-V",
            "Element",
            "Odyssey"
        ]
    },
    "children": null,
    "comparisons": {
        "count": 15,
        "input": {
            "Accord Sedan, Accord Hybrid": 9,
            "Accord Sedan, Pilot": 9,
            "Accord Sedan, CR-V": 1,
            "Accord Sedan, Element": 0.5,
            "Accord Sedan, Odyssey": 5,
            "Accord Hybrid, Pilot": 1,
            "Accord Hybrid, CR-V": 0.1111111111111111,
            "Accord Hybrid, Element": 0.1111111111111111,
            "Accord Hybrid, Odyssey": 0.14285714285714285,
            "Pilot, CR-V": 0.1111111111111111,
            "Pilot, Element": 0.1111111111111111,
            "Pilot, Odyssey": 0.14285714285714285,
            "CR-V, Element": 0.5,
            "CR-V, Odyssey": 5,
            "Element, Odyssey": 6
        },
        "computed": null
    }
}
```

Finally, calling `report(complete=True)` on any Compare object in the hierarchy will return a dictionary containing a report for *every* Compare object in the hierarchy, with the keys of the dictionary being the names of the Compare objects:

```python
>>> complete_report = cargo.report(complete=True)
>>> print([key for key in complete_report])
['Criteria', 'Cost', 'Price', 'Fuel', 'Maintenance', 'Resale', 'Safety', 'Style', 'Capacity', 'Cargo', 'Passenger']
>>> print(complete_report['Cargo'])
{'name': 'Cargo', 'global_weight': 0.0358, 'local_weight': 0.1667, 'target_weights': None, 'elements': {'global_weights': {'Odyssey': 0.011, 'Pilot': 0.006, 'CR-V': 0.006, 'Element': 0.006, 'Accord Sedan': 0.003, 'Accord Hybrid': 0.003}, 'local_weights': {'Odyssey': 0.311, 'Pilot': 0.17, 'CR-V': 0.17, 'Element': 0.17, 'Accord Sedan': 0.089, 'Accord Hybrid': 0.089}, 'consistency_ratio': 0.002}}

>>> print(complete_report['Criteria']['target_weights'])
{'Odyssey': 0.219, 'Accord Sedan': 0.215, 'CR-V': 0.167, 'Accord Hybrid': 0.15, 'Element': 0.144, 'Pilot': 0.106}
```

Calling `report(complete=True, verbose=True)` will return a similar dictionary, but with the detailed version of the reports.

```python
>>> complete_report = style.report(complete=True, verbose=True)
>>> print(complete_report['Price']['comparisons']['count'])
15
```

We could also print this report to the console with the `show=True` argument.

### Purchasing a vehicle reprised: normalized weights and the Compose class

After reading through the explanation of the [vehicle decision problem on Wikipedia](https://en.wikipedia.org/wiki/Analytic_hierarchy_process_–_car_example), you may have wondered whether the data used to represent purely numeric criteria (such as passenger capacity) could be used *directly* when comparing the vehicles to one another, rather than requiring tranformation into judgments of "intensity." In this example, we'll solve the same decision problem as before, except now we'll normalize the measured values for passenger capacity, fuel costs, resale value and cargo capacity in order to arrive at a different set of weights for these criteria.

We'll also use a **Compose** object to structure the decision problem. The Compose object allows us to work with an abstract representation of the problem hierarchy, rather than build it dynamically with code, which is valuable when we're not using AHPy in an interactive setting. To use the Compose object, we'll need to first add the comparison information, then the hierarchy, *in that order*. But more on that later.

Using the list of vehicles from the previous example, we'll first zip together the vehicles and their measured values, then create a Compare object for each of our normalized criteria:

```python
>>> passenger_measured_values = (5, 5, 8, 5, 4, 8)
>>> passenger_data = dict(zip(vehicles, passenger_measured_values))
>>> print(passenger_data)
{'Accord Sedan': 5, 'Accord Hybrid': 5, 'Pilot': 8, 'CR-V': 5, 'Element': 4, 'Odyssey': 8}
>>> passenger_normalized = ahp.Compare('Passenger', passenger_data, precision=3)

>>> fuel_measured_values = (31, 35, 22, 27, 25, 26)
>>> fuel_data = dict(zip(vehicles, fuel_measured_values))
>>> fuel_normalized = ahp.Compare('Fuel', fuel_data, precision=3)

>>> resale_measured_values = (0.52, 0.46, 0.44, 0.55, 0.48, 0.48)
>>> resale_data = dict(zip(vehicles, resale_measured_values))
>>> resale_normalized = ahp.Compare('Resale', resale_data, precision=3)

>>> cargo_measured_values = (14, 14, 87.6, 72.9, 74.6, 147.4)
>>> cargo_data = dict(zip(vehicles, cargo_measured_values))
>>> cargo_normalized = ahp.Compare('Cargo', cargo_data, precision=3)
```

Let's print the normalized local weights of the new Passenger object to compare them to the local weights in the previous example:

```python
>>> print(passenger_normalized.local_weights)
{'Pilot': 0.229, 'Odyssey': 0.229, 'Accord Sedan': 0.143, 'Accord Hybrid': 0.143, 'CR-V': 0.143, 'Element': 0.114}

>>> print(passenger.local_weights)
{'Accord Sedan': 0.493, 'Accord Hybrid': 0.197, 'Odyssey': 0.113, 'Element': 0.091, 'CR-V': 0.057, 'Pilot': 0.049}
```

When we use the measured values directly, we see that the rankings for the vehicles are different than they were before. Whether this will affect the *synthesized* rankings of the target variables remains to be seen, however.

We next create a Compose object and begin to add the comparison information:

```python
>>> compose = ahpy.Compose()

>>> compose.add_comparisons([passenger_normalized, fuel_normalized, resale_normalized, cargo_normalized])
```

We can add comparison information to the Compose object in a few different ways. As shown above, we can provide a list of Compare objects; we can also provide them one at a time or stored in a tuple. Using Compare objects from our previous example:

```python
>>> compose.add_comparisons(cost)
>>> compose.add_comparisons((safety, style, capacity))
```

We can even treat the Compose object like a Compare object and add the data directly. Again using code from the previous example:

```python
>>> compose.add_comparisons('Price', price_comparisons, precision=3)
```

Finally, we can provide an ordered list or tuple containing the data needed to construct a Compare object:

```python
>>> comparisons = [('Maintenance', maintenance_comparisons, 3), ('Criteria', criteria_comparisons)]
>>> compose.add_comparisons(comparisons)
```

Now that all of the comparison information has been added, we next need to create the hierarchy and add it to the Compose object. A hierarchy is simply a dictionary in which the keys are the names of *parent* Compare objects and the values are lists of the names of their *children*:

```python
>>> hierarchy = {'Criteria': ['Cost', 'Safety', 'Style', 'Capacity'],
				 'Cost': ['Price', 'Fuel', 'Resale', 'Maintenance'],
				 'Capacity': ['Passenger', 'Cargo']}
>>> compose.add_hierarchy(hierarchy)
```

With these two steps complete, we can now view the synthesized results of the analysis.

We view a report for a Compose object in the same way we do for a Compare object. The only difference is that the Compose object displays a complete report by default; in order to view the report of a single Compare object in the hierarchy, we need to specify its name:

```python
>>> criteria_report = compose.report('Criteria', show=True)
{
    "name": "Criteria",
    "global_weight": 1.0,
    "local_weight": 1.0,
    "target_weights": {
        "Odyssey": 0.218,
        "Accord Sedan": 0.21,
        "Element": 0.161,
        "Accord Hybrid": 0.154,
        "CR-V": 0.149,
        "Pilot": 0.108
    },
    "elements": {
        "global_weights": {
            "Cost": 0.51,
            "Safety": 0.234,
            "Capacity": 0.215,
            "Style": 0.041
        },
        "local_weights": {
            "Cost": 0.51,
            "Safety": 0.234,
            "Capacity": 0.215,
            "Style": 0.041
        },
        "consistency_ratio": 0.08
    }
}
```

We can access the public properties of any of the comparison information that we've added to the Compose object using either dot or bracket notation:

```python
>>> print(compose.Criteria.target_weights)
{'Odyssey': 0.218, 'Accord Sedan': 0.21, 'Element': 0.161, 'Accord Hybrid': 0.154, 'CR-V': 0.149, 'Pilot': 0.108}

>>> print(compose['Resale']['local_weights']
{'CR-V': 0.188, 'Accord Sedan': 0.177, 'Element': 0.164, 'Odyssey': 0.164, 'Accord Hybrid': 0.157, 'Pilot': 0.15}
```

We can see that normalizing the numeric criteria leads to a slightly different set of target weights, though the Odyssey and the Accord Sedan remain the top two vehicles to consider for purchase.

## Details

Keep reading to learn the details of the AHPy library's API...

### The Compare Class

The Compare class computes the weights and consistency ratio of a positive reciprocal matrix, created using an input dictionary of pairwise comparison values. Optimal values are computed for any [missing pairwise comparisons](#missing-pairwise-comparisons). Compare objects can also be [linked together to form a hierarchy](#compareadd_children) representing the decision problem: the target weights of the problem elements are then derived by synthesizing all levels of the hierarchy.

`Compare(name, comparisons, precision=4, random_index='dd', iterations=100, tolerance=0.0001, cr=True)`

`name`: *str (required)*, the name of the Compare object
- This property is used to link a child object to its parent and must be unique

`comparisons`: *dict (required)*, the elements and values to be compared, provided in one of two forms:

1. A dictionary of pairwise comparisons, in which each key is a tuple of two elements and each value is their pairwise comparison value
    - `{('a', 'b'): 3, ('b', 'c'): 2, ('a', 'c'): 5}`
    - **The order of the elements in the key matters: the comparison `('a', 'b'): 3` means "a is moderately more important than b"**

2. A dictionary of measured values, in which each key is a single element and each value is that element's measured value
    - `{'a': 1.2, 'b': 2.3, 'c': 3.4}`
    - Given this form, AHPy will automatically create consistent, normalized target weights

`precision`: *int*, the number of decimal places to take into account when computing both the target weights and the consistency ratio of the Compare object
- The default precision value is 4

`random_index`: *'dd'* or *'saaty'*, the set of random index estimates used to compute the Compare object's consistency ratio
- 'dd' supports the computation of consistency ratios for matrices less than or equal to 100 &times; 100 in size and uses estimates from:

  >Donegan, H.A. and Dodd, F.J., 'A Note on Saaty's Random Indexes,' *Mathematical and Computer Modelling*, 15:10, 1991, pp. 135-137 (DOI: [10.1016/0895-7177(91)90098-R](https://doi.org/10.1016/0895-7177(91)90098-R))
- 'saaty' supports the computation of consistency ratios for matrices less than or equal to 15 &times; 15 in size and uses estimates from:

  >Saaty, T., *Theory And Applications Of The Analytic Network Process*, Pittsburgh: RWS Publications, 2005, p. 31
- The default random index is 'dd'

`iterations`: *int*, the stopping criterion for the algorithm used to compute the Compare object's target weights
- If target weights have not been determined after this number of iterations, the algorithm stops and the last principal eigenvector to be computed is used as the target weights
- The default number of iterations is 100

`tolerance`: *float*, the stopping criterion for the cycling coordinates algorithm used to compute the optimal value of missing pairwise comparisons
- The algorithm stops when the difference between the norms of two cycles of coordinates is less than this value
- The default tolerance value is 0.0001

`cr`: *bool*, whether to compute the target weights' consistency ratio
- Set `cr=False` to compute the target weights of a matrix when a consistency ratio cannot be determined due to the size of the matrix
- The default value is True

The properties used to initialize the Compare class are intended to be accessed directly, along with a few others:

`Compare.global_weight`: *float*, the global weight of the Compare object within the hierarchy

`Compare.local_weight`: *float*, the local weight of the Compare object within the hierarchy

`Compare.consistency_ratio`: *float*, the consistency ratio of the Compare object's pairwise comparisons

`Compare.global_weights`: *dict*, the global weights of the Compare object's elements; each key is an element and each value is that element's computed global weight
- `{'a': 0.25, 'b': 0.25}`

`Compare.local_weights`: *dict*, the local weights of the Compare object's elements; each key is an element and each value is that element's computed local weight
- `{'a': 0.5, 'b': 0.5}`

`Compare.target_weights`: *dict*, the target weights of the elements in the lowest level of the hierarchy; each key is an element and each value is that element's computed target weight; *if the global weight of the Compare object is less than 1.0, the value will be `None`*
- `{'a': 0.5, 'b': 0.5}`

### Compare.add_children()

Compare objects can be linked together to form a hierarchy representing the decision problem. To link Compare objects together into a hierarchy, call `add_children()` on the Compare object intended to form the *upper* level (the *parent*) and include as an argument a list or tuple of one or more Compare objects intended to form its *lower* level (the *children*).

**In order to properly synthesize the levels of the hierarchy, the `name` of each child object MUST appear as an element in its parent object's input `comparisons` dictionary.**

`Compare.add_children(children)`

`children`: *list* or *tuple (required)*, the Compare objects that will form the lower level of the current Compare object

```python
>>> child1 = ahpy.Compare(name='child1', ...)
>>> child2 = ahpy.Compare(name='child2', ...)

>>> parent = ahpy.Compare(name='parent', comparisons={('child1', 'child2'): 5})
>>> parent.add_children([child1, child2])
```

The precision of the target weights is updated as the hierarchy is constructed: each time `add_children()` is called, the precision of the target weights is set to equal that of the Compare object with the lowest precision in the hierarchy. Because lower precision propagates up through the hierarchy, *the target weights will always have the same level of precision as the hierarchy's least precise Compare object*. This also means that it is possible for the precision of a Compare object's target weights to be different from the precision of its local and global weights.

### Compare.report()

A standard report on the details of a Compare object is available. To return the report as a dictionary, call `report()` on the Compare object; to simultaneously print the information to the console in JSON format, set `show=True`. The report is available in two levels of detail; to return the most detailed report, set `verbose=True`.

`Compare.report(complete=False, show=False, verbose=False)`

`complete`: *bool*, whether to return a report for every Compare object in the hierarchy
- This returns a dictionary of reports, with the keys of the dictionary being the names of the Compare objects
  - `{'a': {'name': 'a', ...}, 'b': {'name': 'b', ...}}`
- The default value is False
`show`: *bool*, whether to print the report to the console in JSON format
- The default value is False
`verbose`: *bool*, whether to include full details of the Compare object within the report
- The default value is False

The keys of the report take the following form:

`name`: *str*, the name of the Compare object

`global_weight`: *float*, the global weight of the Compare object within the hierarchy

`local_weight`: *float*, the local weight of the Compare object within the hierarchy

`target_weights`: *dict*, the target weights of the elements in the lowest level of the hierarchy; each key is an element and each value is that element's computed target weight
- *If the global weight of the Compare object is less than 1.0, the value will be `None`*
- `{'a': 0.5, 'b': 0.5}`

`elements`: *dict*, information regarding the elements compared by the Compare object
- `global_weights`: *dict*, the global weights of the Compare object's elements; each key is an element and each value is that element's computed global weight
  - `{'a': 0.25, 'b': 0.25}`
- `local_weights`: *dict*, the local weights of the Compare object's elements; each key is an element and each value is that element's computed local weight
  - `{'a': 0.5, 'b': 0.5}`
- `consistency_ratio`: *float*, the consistency ratio of the Compare object's pairwise comparisons

The remaining dictionary keys are only displayed when `verbose=True`:

- `random_index`: *'Donegan & Dodd' or 'Saaty'*, the random index used to compute the consistency ratio
- `count`: *int*, the number of elements compared by the Compare object
- `names`: *list*, the names of the elements compared by the Compare object

`children`: *dict*, the children of the Compare object
  - If the Compare object has no children, the value will be `None`
- `count`: *int*, the number of the Compare object's children
- `names`: *list*, the names of the Compare object's children

`comparisons`: *dict*, the comparisons of the Compare object
- `count`: *int*, the number of comparisons made by the Compare object, *not counting reciprocal comparisons*
- `input`: *dict*, the comparisons input to the Compare object; this is identical to the input `comparisons` dictionary
- `computed`: *dict*, the comparisons computed by the Compare object; each key is a tuple of two elements and each value is their computed pairwise comparison value
  - `{('c', 'd'): 0.730297106886979}, ...}`
  - If the Compare object has no computed comparisons, the value will be `None`

### The Compose Class

The Compose class can store and structure all of the information making up a decision problem. After first [adding comparison information](#composeadd_comparisons) to the object, then [adding the problem hierarchy](#composeadd_hierarchy), the analysis results of the multiple different Compare objects can be accessed through the single Compose object.

`Compose()`
 
After adding all necessary information, the public properties of any stored Compare object can be accessed directly using either dot or bracket notation:

```python
>>> my_compose_object.a.global_weights

>>> my_compose_object['a']['global_weights']
```

### Compose.add_comparisons()

The comparison information of a decision problem can be added to a Compose object in any of the several ways listed below. Always add comparisons *before* adding the problem hierarchy.

`Compose.add_comparisons(item, comparisons=None, precision=4, random_index='dd', iterations=100, tolerance=0.0001, cr=True)`

`item`: *Compare object, list or tuple, or string (required)*, this argument allows for multiple input types:

1. A single Compare object
    - `Compare('a', comparisons=a, ...)`

2. A list or tuple of Compare objects
    - `[Compare('a', ...), Compare('b', ...)]`
  
3. The data necessary to create a Compare object
    - `Compose.add_comparisons('a', comparisons=a, ...)`
    - The method signature mimics that of the Compare class to support this use case.

4. A nested list or tuple of the data necessary to create a Compare object
    - `(('a', a, ...), ('b', b, ...))`

All other arguments are identical to those of the [Compare class](#the-compare-class).

### Compose.add_hierarchy()

The Compose class uses an abstract representation of the problem hierarchy to automatically link its Compare objects together. When a hierarchy is added, the elements of the decision problem are synthesized and the analysis results are immediately available.

**`Compose.add_hierarchy()` should only be called AFTER all comparison information has been added to the Compose object.**

`Compose.add_hierarchy(hierarchy)`

`hierarchy`: *dict*, a representation of the hierarchy as a dictionary, in which the keys are the names of parent Compare objects and the values are lists of the names of their children
- `{'a': ['b', 'c'], 'b': ['d', 'e']}`

### Compose.report()

The standard report available for a Compare object can be accessed through the Compose object. Calling `report()` on a Compose object is equivalent to calling `report(complete=True)` on a Compare object and will return a dictionary of all the reports within the hierarchy; calling `report(name='a')` on a Compose object is equivalent to calling `a.report()` on the named Compare object.

`Compose.report(name=None, show=False, verbose=False)`

`name`: *str*, the name of a Compare object report to return; if None, returns a dictionary of reports, with the keys of the dictionary being the names of the Compare objects in the hierarchy
- `{'a': {'name': 'a', ...}, 'b': {'name': 'b', ...}}`
- The default value is None

All other arguments are identical to the [Compare class's `report()` method](#comparereport).

### A Note on Weights

Compare objects compute up to three kinds of weights for their elements: global weights, local weights and target weights.
Compare objects also compute their own global and local weight, given their parent.

- **Global** weights display the computed weights of a Compare object's elements **dependent on** that object's global weight within the current hierarchy
  - Global weights are derived by multiplying the local weights of the elements within a Compare object by that object's *own* global weight in the current hierarchy

- **Local** weights display the computed weights of a Compare object's elements **independent of** that object's global weight within the current hierarchy
  - The local weights of the elements within a Compare object will always (approximately) sum to 1.0

- **Target** weights display the synthesized weights of the problem elements described in the *lowest level* of the current hierarchy
  - Target weights are only computed by the Compare object at the highest level of the hierarchy (*i.e.* the only Compare object without a parent)

#### N.B.

A Compare object that does not have a parent will have identical global and local weights; a Compare object that has neither a parent nor children will have identical global, local and target weights.

In many instances, the sum of the local or target weights of a Compare object will not equal 1.0 *exactly*. This is due to rounding. If it's critical that the sum of the weights equals 1.0, it's recommended to simply divide the weights by their cumulative sum: `x = x / np.sum(x)`. Note, however, that the resulting values will contain a false level of precision, given their inputs.

### Missing Pairwise Comparisons

When a Compare object is initialized, the elements forming the keys of the input `comparisons` dictionary are permuted. Permutations of elements that do not contain a value within the input `comparisons` dictionary are then optimally solved for using the cyclic coordinates algorithm described in:

>Bozóki, S., Fülöp, J. and Rónyai, L., 'On optimal completion of incomplete pairwise comparison matrices,' *Mathematical and Computer Modelling*, 52:1–2, 2010, pp. 318-333 (DOI: [10.1016/j.mcm.2010.02.047](https://doi.org/10.1016/j.mcm.2010.02.047))

As the paper notes, "The number of *necessary* pairwise comparisons ... depends on the characteristics of the real decision problem and provides an exciting topic of future research" (29). In other words, don't rely on the algorithm to fill in a comparison dictionary that has a large number of missing values: it certainly might, but it also very well might not. **Caveat emptor!**

The example below demonstrates this functionality of AHPy using the following matrix:

||a|b|c|d|
|-|:-:|:-:|:-:|:-:|
|a|1|1|5|2|
|b|1|1|3|4|
|c|1/5|1/3|1|**3/4**|
|d|1/2|1/4|**4/3**|1|

We'll first compute the target weights and consistency ratio for the complete matrix, then repeat the process after removing the **(c, d)** comparison marked in bold. We can view the computed value in the Compare object's detailed report:

```python
>>> comparisons = {('a', 'b'): 1, ('a', 'c'): 5, ('a', 'd'): 2, ('b', 'c'): 3, ('b', 'd'): 4, ('c', 'd'): 3 / 4}

>>> complete = ahpy.Compare('Complete', comparisons)
>>> print(complete.target_weights)
{'b': 0.3917, 'a': 0.3742, 'd': 0.1349, 'c': 0.0991}
>>> print(complete.consistency_ratio)
0.0372

>>> del comparisons[('c', 'd')]

>>> missing_cd = ahpy.Compare('Missing_CD', comparisons)
>>> print(missing_cd.target_weights)
{'b': 0.392, 'a': 0.3738, 'd': 0.1357, 'c': 0.0985}
>>> print(missing_cd.consistency_ratio)
0.0372
>>> report = missing_cd.report(verbose=True)
>>> print(report['comparisons']['computed'])
{('c', 'd'): 0.7302971068355002}
```

## Development and Testing

To set up a development environment and run the included tests, you can use the following commands:

```
virtualenv .venv
source .venv/bin/activate
python setup.py develop
pip install pytest
pytest
```