# Timing Diagram
<img src="https://raw.githubusercontent.com/alkasm/timingdiagram/readme-image/timingdiagram.svg?sanitize=true" alt="Visual timing diagram example" width="100%">

Timing diagrams provide a clean abstraction to parsing discrete state changes over time.

* Reduce data to state changes
* Easily compare states of multiple objects over time
* Query state by time
* Use any ordered index, not just time

## Getting Started

### Install

As with any other Python project, install directly into a virtual environment of choice:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install git+https://github.com/alkasm/timingdiagram
```

### Try it out

```python
>>> from timingdiagram import TimingDiagram
>>> d1 = TimingDiagram(enumerate([False, False, False, True, True, False, True]))
>>> d2 = TimingDiagram(enumerate([False, True, False, False, True, False, False]))
>>> d1 | d2
TimingDiagram([(0, False), (1, True), (2, False), (3, True), (5, False), (6, True)])
```
