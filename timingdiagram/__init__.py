from heapq import merge
from itertools import groupby
from collections import deque
import operator
from sortedcollections import SortedDict


class TimingDiagram:
    """Two-state (True/False or 1/0) timing diagram with boolean algebra operations."""

    def __init__(self, time_state_pairs):
        """Creates a timing diagram out of a series of (time, state) pairs.

        Notes
        =====
        The input states can be any truthy/falsey values.
        The input times can be any type with a partial ordering.
        The input sequence does not need to be sorted (input is sorted during initialization).
        Compresses duplicate sequential states and stores them in the `timeline` attribute.

        Example
        =======
        >>> diagram = TimingDiagram([(0, True), (1, False), (5, False), (10, True)])
        >>> print(~diagram)
        TimingDiagram([(0, False), (1, True), (10, False)])
        """
        self.timeline = SortedDict(
            _compress(time_state_pairs, key=operator.itemgetter(1))
        )

    def __getitem__(self, item):
        return self.timeline[item]

    def __matmul__(self, time):
        """Alias for at()"""
        return self.at(time)

    def __eq__(self, other):
        """Returns a new timing diagram, True where the two diagrams are equal."""
        return self.compare(other, key=operator.eq)

    def __ne__(self, other):
        """Returns a new timing diagram, True where the two diagrams are equal."""
        return ~(self == other)

    def __and__(self, other):
        """Returns a new timing diagram, True where the two diagrams are both True."""
        return self.compare(other, key=operator.and_)

    def __or__(self, other):
        """Returns a new timing diagram, True where either diagram is True."""
        return self.compare(other, key=operator.or_)

    def __xor__(self, other):
        """Returns a new timing diagram, True where the two diagrams are not equal."""
        return self != other

    def __invert__(self):
        """Returns a new timing diagram with states flipped."""
        return TimingDiagram(((t, not s) for t, s in self.timeline.items()))

    def at(self, time):
        """Returns the state at a particular time. Uses bisection for search (binary search)."""
        idx = max(0, self.timeline.bisect(time) - 1)
        return self.timeline.values()[idx]

    def compare(self, other, key):
        """Constructs a new timing diagram based on comparisons between two diagrams,
        with (time, key(self[time], other[time])) for each time in the timelines.
        """
        # TODO: Implement linear algorithm instead of .at() for each time, which is O(n log n).
        return TimingDiagram(
            (
                (k, key(self.at(k), other.at(k)))
                for k in merge(self.timeline.keys(), other.timeline.keys())
            )
        )

    def __repr__(self):
        return f"{self.__class__.__qualname__}({list(self.timeline.items())})"


def _compress(sorted_iterable, key):
    """Yields the first value from each sequential group (grouped by key function).
    
    In other words, returns state changes. Also, always yields the last element
    (if it wasn't already yielded), even if it isn't a state change.
    """
    final = ()
    for _, g in groupby(sorted_iterable, key=key):
        yield next(g)
        final = deque(g, maxlen=1)
    yield from final  # yield final state if not already yielded
