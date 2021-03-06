import time
import pytest

from django.conf import settings
settings.configure()

from template_flamegraph.flamegraph_utils import Stack, wrap_for_flamegraph


@pytest.fixture
def patch_time(monkeypatch):
    class mocked_time:
        def __init__(self):
            self._time = 0

        def __call__(self):
            self._time += 1
            return self._time

    monkeypatch.setattr(time, 'time', mocked_time())


@pytest.fixture
def stack():
    stack = Stack()
    stack.push('a1', 1)
    stack.push('b1', 2)
    stack.pop(3)
    stack.push('b2', 4)
    stack.pop(5)
    stack.pop(6)
    stack.push('a2', 7)
    stack.push('b3', 8)
    stack.pop(9)
    stack.push('b4', 10)
    stack.pop(11)
    stack.pop(12)
    return stack


def test_stack(stack):
    assert stack.history == {'stack': [{
        'label': 'a1',
        'stack': [{
            'label': 'b1',
            'stack': [],
            'total_time': 1,
            'time_in_self': 1,
        }, {
            'label': 'b2',
            'stack': [],
            'total_time': 1,
            'time_in_self': 1,
        }],
        'total_time': 5,
        'time_in_self': 3,
    }, {
        'label': 'a2',
        'stack': [{
            'label': 'b3',
            'stack': [],
            'total_time': 1,
            'time_in_self': 1,
        }, {
            'label': 'b4',
            'stack': [],
            'total_time': 1,
            'time_in_self': 1,
        }],
        'total_time': 5,
        'time_in_self': 3,
    }]}


def test_stack_collapsed(stack):
    assert stack.collapsed() == [
        {'calls': ['a1'], 'time': 3},
        {'calls': ['a1', 'b1'], 'time': 1},
        {'calls': ['a1', 'b2'], 'time': 1},
        {'calls': ['a2'], 'time': 3},
        {'calls': ['a2', 'b3'], 'time': 1},
        {'calls': ['a2', 'b4'], 'time': 1},
    ]


def test_stack_as_flamegraph_pl_input(stack):
    assert stack.as_flamegraph_pl_input() == '''
a1 3
a1;b1 1
a1;b2 1
a2 3
a2;b3 1
a2;b4 1
    '''.strip()


def test_stack_to_svg(stack):
    assert 'svg version' in stack.to_svg()


def test_wrap_for_flamegraph(patch_time):
    class C:
        def m(self, x):
            if x < 0:
                return x
            else:
                return 1 + self.m(x - 1)

    def labeller(args, kwargs):
        return args[1]

    stack = Stack()

    C.m = wrap_for_flamegraph(C.m, labeller, stack)

    c = C()
    c.m(2)

    assert stack.collapsed() == [
        {'calls': [2], 'time': 2},
        {'calls': [2, 1], 'time': 2},
        {'calls': [2, 1, 0], 'time': 2},
        {'calls': [2, 1, 0, -1], 'time': 1},
    ]
