import ahpy


class AhpData:
    """A class to contain comparisons and hierarchy for computation."""

    def __init__(self):
        self.comparisons = {}
        self.hierarchy = []

    def add_comparisons(self, dimension, comparisons):
        """Add comparisons along a certain dimension."""
        self.comparisons[dimension] = self.comparisons.get(dimension, {})
        for pair, intensity in comparisons.items():
            assert pair not in self.comparisons[dimension], (
                f'{pair} not in {dimension}')
            self.comparisons[dimension][pair] = intensity

    def run_compare(self, node, hierarchy, precision=4):
        """Run Compare for the given hierarchy with 'node' as the root.

        :param node is the name of a node in the hierarchy
        :param hierarchy is a dict mapping a name to a list of sub-criteria
        :param precision is the precision for ahpy.Compare
        """
        node_comps = self.comparisons[node]
        results = ahpy.Compare(node, node_comps, precision)
        if (node in hierarchy
                # tolerate empty sub-criteria list
                and hierarchy[node]):
            # this is not a leaf, get child results first
            child_results = []
            for child in hierarchy[node]:
                child_results.append(self.run_compare(
                    child, hierarchy, precision))
            results.add_children(child_results)
        return results
