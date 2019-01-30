import functools
from collections import OrderedDict

from util.ordered_set import MultiOrderedSet, ordered_pop
from node.node_type import NodeType

class DiscogsFrontier(MultiOrderedSet):
  def __init__(self, **kwargs):
    nodetype_kwarg_map = OrderedDict({
      NodeType.ARTIST : 'artists',
      NodeType.LABEL: 'labels',
      NodeType.RELEASE: 'releases'
    }.items())

    cols = [None for _ in range(len(NodeType))]
    for nodetype in NodeType.__members__.values():
      kwarg_name = nodetype_kwarg_map[nodetype]
      cols[nodetype.value] = kwargs[kwarg_name]

    super().__init__(cols,
      popper_fn=functools.partial(ordered_pop,
        [nt.value for nt in kwargs['pop_order']]))
