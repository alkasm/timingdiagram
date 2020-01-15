<img src="https://raw.githubusercontent.com/alkasm/timingdiagram/master/timingdiagram.svg?sanitize=true" alt="Visual timing diagram example" width="100%">

# timingdiagram

Timing diagrams provide a clean abstraction to work with discrete state changes over time.

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

## Example

Suppose you had a log of users signing in and out of a service, and the log included the time, user id, and action the user took. We can view each user's login/logout history as a timing diagram, and simply `&` them all together to see when all users were logged in at the same time:

```python
log = """2019-08-27T19:38:50 001768bf-af44-46a6-890d-048f2c50aa29 login
2019-08-27T19:51:11 084c07f0-dd0d-46a3-8eb5-1d4cb13756a4 logout
2019-08-27T19:55:25 001768bf-af44-46a6-890d-048f2c50aa29 logout
2019-08-27T19:58:37 001768bf-af44-46a6-890d-048f2c50aa29 login
2019-08-27T20:17:21 a8118353-eb81-4ce0-8d10-6f3f9de6d7ca login
2019-08-27T20:45:19 001768bf-af44-46a6-890d-048f2c50aa29 logout
2019-08-27T21:01:45 001768bf-af44-46a6-890d-048f2c50aa29 login
2019-08-27T21:18:09 001768bf-af44-46a6-890d-048f2c50aa29 logout
2019-08-27T22:02:37 084c07f0-dd0d-46a3-8eb5-1d4cb13756a4 login
2019-08-27T22:55:54 001768bf-af44-46a6-890d-048f2c50aa29 login
2019-08-27T23:08:07 001768bf-af44-46a6-890d-048f2c50aa29 logout
2019-08-27T23:23:04 a8118353-eb81-4ce0-8d10-6f3f9de6d7ca logout
2019-08-27T23:47:50 001768bf-af44-46a6-890d-048f2c50aa29 login
2019-08-27T23:55:10 084c07f0-dd0d-46a3-8eb5-1d4cb13756a4 logout
2019-08-27T23:56:33 001768bf-af44-46a6-890d-048f2c50aa29 logout""".split("\n")


from collections import defaultdict
from functools import reduce
from timingdiagram import TimingDiagram


sessions = defaultdict(list)
for row in log:
    ts, userid, action = row.split()
    sessions[userid].append((ts, action == "login"))

all_logged_in = reduce(lambda d1, d2: d1 & d2, map(TimingDiagram, sessions.values()))
```

From just a few lines of code, we get a timing diagram corresponding to when all the users were logged in:

```
TimingDiagram([
  ('2019-08-27T19:38:50', False), 
  ('2019-08-27T22:55:54', True), 
  ('2019-08-27T23:08:07', False), 
  ('2019-08-27T23:56:33', False)
 ])
 ```
 
So all users were logged in between `22:55:54` and `23:08:07` on `2019-08-27`. The additional states at the beginning and end signify the start and end times of the logs.
