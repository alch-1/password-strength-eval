import collections
from itertools import islice

def sliding_window(iterable, n):
  # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
  it = iter(iterable)
  window = collections.deque(islice(it, n), maxlen=n)
  if len(window) == n:
    yield tuple(window)
  for x in it:
    window.append(x)
    yield tuple(window)

def get_all_windows(s):
  all_windows = []
  n = len(s)
  while n > 2:
    all_windows += ["".join(x) for x in sliding_window(s, n)]
    n = n - 1
  return all_windows

print(get_all_windows("DYpmCgPt")) # => ['DYpmCgPt', 'DYpmCgP', 'YpmCgPt', 'DYpmCg', 'YpmCgP', 'pmCgPt', 'DYpmC', 'YpmCg', 'pmCgP', 'mCgPt', 'DYpm', 'YpmC', 'pmCg', 'mCgP', 'CgPt', 'DYp', 'Ypm', 'pmC', 'mCg', 'CgP', 'gPt']