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


def test_stack():
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

    assert stack.history == {'stack': [{
        'label': 'a1',
        'stack': [{
            'label': 'b1',
            'stack': [],
            't': 1,
        }, {
            'label': 'b2',
            'stack': [],
            't': 1,
        }],
        't': 5,
    }, {
        'label': 'a2',
        'stack': [{
            'label': 'b3',
            'stack': [],
            't': 1,
        }, {
            'label': 'b4',
            'stack': [],
            't': 1,
        }],
        't': 5,
    }]}


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

    assert stack.history['stack'] == [{
        'label': 2,
        'stack': [{
            'label': 1,
            'stack': [{
                'label': 0,
                'stack': [{
                    'label': -1,
                    'stack': [],
                    't': 1,
                }],
                't': 3,
            }],
            't': 5,
        }],
        't': 7,
    }]
