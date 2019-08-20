# Timing Diagrams

            0123456789
        a = ____----__
        b = _-----___-
       ~a = ----____--
    a & b = ____--____
    a | b = _-------_-
    a ^ b = _---__--_-
    
# Above examples in code

    from timingdiagrams import TimingDiagram

    def fromstring(s):
        return TimingDiagram(*((c == '-', i) for i, c in enumerate(s)))

    def view(diagram):
        chars = ['_-'[e1.state] * (e2.time - e1.time) for e1, e2 in zip(diagram, diagram[1:])]
        if len(diagram) > 1:
            chars.append('_-'[diagram[-1].state])
        print(''.join(chars))

    >>> a = fromstring('____----__')
    >>> b = fromstring('_-----___-')
    >>> view(a)
    ____----__
    >>> view(b)
    _-----___-
    >>> view(~a)
    ----____--
    >>> view(a & b)
    ____--____
    >>> view(a | b)
    _-------_-
    >>> view(a ^ b)
    _---__--_-
