import itertools
import time

import ahpy


def test_ahp_data():
    t1 = time.time()

    ahp_data = ahpy.AhpData()
    ahp_data.add_comparisons(
        'Criteria',
        {
            ('Cost', 'Safety'): 3, ('Cost', 'Style'): 7,
            ('Cost', 'Capacity'): 3,
            ('Safety', 'Style'): 9, ('Safety', 'Capacity'): 1,
            ('Style', 'Capacity'): 1/7,
        })

    ahp_data.add_comparisons(
        'Cost',
        {
            ('Price', 'Fuel'): 2, ('Price', 'Maintenance'): 5,
            ('Price', 'Resale'): 3,
            ('Fuel', 'Maintenance'): 2, ('Fuel', 'Resale'): 2,
            ('Maintenance', 'Resale'): 1/2,
        })

    ahp_data.add_comparisons(
        'Capacity',
        {
            ('Cargo', 'Passenger'): 1/5
        })

    vehicles = (
        'Accord Sedan', 'Accord Hybrid', 'Pilot', 'CR-V', 'Element', 'Odyssey')
    vehicle_pairs = list(itertools.combinations(vehicles, 2))

    for dimension, the_values in (
            ('Price', (9, 9, 1, 1/2, 5, 1, 1/9, 1/9,
                       1/7, 1/9, 1/9, 1/7, 1/2, 5, 6)),
            ('Safety', (1, 5, 7, 9, 1/3, 5, 7, 9, 1/3, 2, 9, 1/8, 2, 1/8, 1/9)),
            ('Passenger', (1, 1/2, 1, 3, 1/2, 1/2, 1, 3,
                           1/2, 2, 6, 1, 3, 1/2, 1/6)),
            ('Fuel', (1/1.13, 1.41, 1.15, 1.24, 1.19, 1.59, 1.3, 1.4,
                      1.35, 1/1.23, 1/1.14, 1/1.18, 1.08, 1.04, 1/1.04)),
            ('Resale', (3, 4, 1/2, 2, 2, 2, 1/5, 1, 1, 1/6, 1/2, 1/2, 4, 4, 1)),
            ('Maintenance', (1.5, 4, 4, 4, 5, 4, 4, 4, 5, 1, 1.2, 1, 1, 3, 2)),
            ('Style', (1, 7, 5, 9, 6, 7, 5, 9, 6, 1/6, 3, 1/3, 7, 5, 1/5)),
            ('Cargo', (1, 1/2, 1/2, 1/2, 1/3, 1/2, 1/2,
                       1/2, 1/3, 1, 1, 1/2, 1, 1/2, 1/2)),
    ):
        ahp_data.add_comparisons(dimension, dict(zip(vehicle_pairs, the_values)))

    hierarchy = {'Cost': ['Price', 'Fuel', 'Maintenance', 'Resale'],
                 'Capacity': ['Cargo', 'Passenger'],
                 'Criteria': ['Cost', 'Safety', 'Style', 'Capacity']}

    # run through the hierarchy to get target_weights from comparisons
    results = ahp_data.run_compare('Criteria', hierarchy)

    assert results.target_weights == (
        {'Odyssey': 0.219, 'Accord Sedan': 0.215, 'CR-V': 0.167,
         'Accord Hybrid': 0.15, 'Element': 0.144, 'Pilot': 0.106})

    # Less than 100 ms to run.
    assert (time.time() - t1) < 0.1
