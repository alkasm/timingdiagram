from bisect import bisect
from heapq import merge
from collections import namedtuple
from itertools import groupby
from collections import deque
import operator


class State(namedtuple("State", "state, time")):
    def __str__(self):
        return f"{self.__class__}({self.state:<5}, {str(self.time)})"


class TimingDiagram:
    """Two-state (True/False or 1/0) timing diagram with boolean algebra operations."""

    def __init__(self, *state_time_pairs):
        """Creates a timing diagram out of a sequence of (state, time) pairs.
        The input states can be any truthy/falsey values.
        The input times can be any type with a partial ordering.
        The input sequence does not need to be sorted (input is sorted during initialization).
        Compresses duplicate sequential states and stores them in the timeline attribute.

        Example
        =======
        >>> diagram = TimingDiagram((True, 0), (False, 1), (False, 5), (True, 10))
        >>> print(~diagram)
        TimingDiagram((False, 0), (True, 1), (False, 10))
        """
        states = sorted(
            (State(bool(s), t) for s, t in state_time_pairs),
            key=operator.attrgetter("time"),
        )
        self._timeline = tuple(_compress(states, key=operator.attrgetter("state")))
        self._breakpoints = [s.time for s in self.timeline[1:]]

    @property
    def timeline(self):
        return self._timeline

    @timeline.setter
    def timeline(self, val):
        raise AttributeError(f"{self.__class__.__qualname__} is immutable.")

    def __len__(self):
        """Number of events in the compressed timeline."""
        return len(self.timeline)

    def __getitem__(self, slice):
        return self.timeline[slice]

    def __matmul__(self, time):
        """Alias for at()"""
        return self.at(time)

    def __iter__(self):
        """Iterator through the compressed timeline."""
        return iter(self.timeline)

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
        return TimingDiagram(*(State(not s, t) for s, t in self))

    def __str__(self):
        args = ", ".join((str(tuple(t)) for t in self))
        return f"{self.__class__.__qualname__}({args})"

    def __repr__(self):
        return f"{self.__class__.__qualname__}{tuple(self.timeline)}"

    def at(self, time):
        """Returns the state at a particular time."""
        return self.timeline[bisect(self._breakpoints, time)]

    def compare(self, other, key):
        """Constructs a new timing diagram based on comparisons between two diagrams.
        True when key(self[time], other[time]) is truthy for each time in the timelines.
        """
        try:
            return TimingDiagram(
                *(
                    State(key((self @ s.time).state, (other @ s.time).state), s.time)
                    for s in merge(self, other, key=operator.attrgetter("time"))
                )
            )
        except IndexError:
            raise ValueError(f"Cannot compare against an empty ```")


def _compress(sorted_iterable, key):
    """Yields the first value from each sequential group (grouped by key function).
    
    In other words, returns state changes. Also, always yields the last element
    (if it wasn't already yielded), even if it isn't a state change.
    """
    g = ()
    for _, g in groupby(sorted_iterable, key=key):
        yield next(g)
    yield from deque(g, maxlen=1)  # yield final state if not already yielded
