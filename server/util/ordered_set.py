import itertools

class OrderedSet(object):
  def pop(self):
    raise NotImplementedError()

  def extend(self, other):
    raise NotImplementedError()

  def __repr__(self):
    raise NotImplementedError()

class MultiOrderedSet(OrderedSet):
  def __init__(self, cols, popper_fn=None):
    self.cols = cols
    self.popper_fn = popper_fn

  def __index__(self):
    return sum([len(col) for col in self.cols])

  def __iter__(self):
    return itertools.chain(*self.cols)

  def extend(self, other):
    for cid, other_col in enumerate(other.cols):
      self.cols[cid].extend(other_col)

  def pop(self):
    return self.popper_fn(self.cols)

  @property
  def num_cols(self):
    return len(self.cols)

  def __repr__(self):
    return str(self.cols)

def ordered_pop(order, cols):
  for index in order:
    curcol = cols[index]
    if curcol:
      return curcol.pop()

  return None

