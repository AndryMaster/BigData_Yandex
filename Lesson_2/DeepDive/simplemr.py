from typing import Iterable, Callable, Any
from itertools import groupby


def flatten(inp: Iterable[Iterable[Any]]) -> Iterable[Any]:
    for it in inp:
        for item in it:
            yield item


def run_map(mapper: Callable[[Any], Iterable[Any]], input_stream: Iterable[Any]):
    return flatten(map(mapper, input_stream))


def run_reduce(reducer: Callable[[Iterable[Any]], Any],
               input_stream: Iterable[Any],
               key: [str]) -> Iterable[Any]:
    def key_func(item):
        return tuple(getattr(item, k) for k in key)

    sorted_stream = sorted(input_stream, key=key_func)
    grouped_stream = groupby(sorted_stream, key=key_func)
    return flatten(map(lambda x: reducer(x[1]), grouped_stream))


class SimpleMapReduce:
    def __init__(self, stream):
        self._stream = stream

    def map(self, mapper):
        self._stream = run_map(mapper, self._stream)
        return self

    def reduce(self, reducer, key):
        self._stream = run_reduce(reducer, self._stream, key)
        return self

    def output(self):
        return self._stream
