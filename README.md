# Timing Diagrams

            0123456789
        a = ____----__
        b = _-----___-
       ~a = ----____--
    a & b = ____--____
    a | b = _-------_-
    a ^ b = _---__--_-
    
# Above examples in code

```python
from timingdiagrams import TimingDiagram

def fromstring(s):
    return TimingDiagram([(i, c == "-") for i, c in enumerate(s)])

def tostring(diagram):
    tl = diagram.timeline.items()
    chars = ["_-"[s1] * (t2 - t1) for (t1, s1), (t2, _) in zip(tl, tl[1:])]
    if len(diagram.timeline) > 1:
        chars.append("_-"[tl[-1][1]])
    return "".join(chars)

a = fromstring("____----__")
b = fromstring("_-----___-")
assert tostring(a) == "____----__"
assert tostring(b) == "_-----___-"
assert tostring(~a) == "----____--"
assert tostring(a & b) == "____--____"
assert tostring(a | b) == "_-------_-"
assert tostring(a ^ b) == "_---__--_-"
```
