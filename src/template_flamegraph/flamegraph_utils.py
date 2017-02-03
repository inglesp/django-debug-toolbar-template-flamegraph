import time


class Stack:
    def __init__(self):
        self.history = {'stack': []}

    def push(self, label, t0):
        frame = {'parent': self.history, 'label': label, 'stack': [], 't0': t0}
        self.history['stack'].append(frame)
        self.history = frame

    def pop(self, t1):
        self.history['t'] = t1 - self.history.pop('t0')
        self.history = self.history.pop('parent')

    def collapse(self):
        pass


def wrap_for_flamegraph(fn, labeller, stack):
    def inner(*args, **kwargs):
        result = None
        exception = None

        label = labeller(args, kwargs)
        stack.push(label, time.time())

        try:
            result = fn(*args, **kwargs)
        except Exception as e:
            exception = e

        stack.pop(time.time())

        if exception is not None:
            raise exception
        else:
            return result

    return inner
