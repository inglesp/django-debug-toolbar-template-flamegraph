import time


class Stack:
    def __init__(self):
        self.history = {'stack': []}

    def push(self, label, t0):
        frame = {'parent': self.history, 'label': label, 'stack': [], 't0': t0}
        self.history['stack'].append(frame)
        self.history = frame

    def pop(self, t1):
        self.history['total_time'] = t1 - self.history.pop('t0')
        time_in_children = sum(frame['total_time'] for frame in self.history['stack'])
        self.history['time_in_self'] = self.history['total_time'] - time_in_children
        self.history = self.history.pop('parent')

    def collapsed(self):
        collapsed = []
        for frame in self.history['stack']:
            self._collapsed_helper(frame, [], collapsed)
        return collapsed

    def _collapsed_helper(self, frame, calls, collapsed):
        calls_ = calls + [frame['label']]
        time_ = frame['time_in_self']
        collapsed.append({'calls': calls_, 'time': time_})
        for frame_ in frame['stack']:
            self._collapsed_helper(frame_, calls_, collapsed)


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
