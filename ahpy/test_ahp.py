import numpy as np
from ahpy import ahpy


drinks_cri = ('coffee', 'wine', 'tea', 'beer', 'sodas', 'milk', 'water')
drinks_val = np.array([[1, 9, 5, 2, 1, 1, .5],
                    [1/9., 1, 1/3., 1/9., 1/9., 1/9., 1/9.],
                    [.2, 3, 1, 1/3., .25, 1/3., 1/9.],
                    [.5, 9, 3, 1, .5, 1, 1/3.],
                    [1, 9, 4, 2, 1, 2, .5],
                    [1, 9, 3, 1, .5, 1, 1/3.],
                    [2, 9, 9, 3, 2, 3, 1]])


def test_drinks():
    """
    Examples from Saaty, Thomas L., 'Decision making with the analytic hierarchy process,'
    Int. J. Services Sciences, 1:1, 2008, pp. 83-98.
    """
    c = ahpy.Compare('Drinks', drinks_val, drinks_cri, precision=3, random_index='saaty')
    assert c.consistency_ratio == 0.022
