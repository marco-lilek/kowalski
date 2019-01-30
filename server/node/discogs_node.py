import logging
import math
from discogs_client.models import Master

from util.ordered_set import MultiOrderedSet, ordered_pop
from util.search import SearchNode
from util.network.network_node import NetworkNode
from discogs_frontier import DiscogsFrontier
import throttling

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DiscogsNode(SearchNode, NetworkNode):
  model = None

  @classmethod
  def from_item(cls, discogs_item, runner):
    '''
    Initialize using a discogs item.
    Will pick the correct node type based on the item type
    '''
    from node.artist_node import ArtistNode
    from node.label_node import LabelNode
    from node.release_node import ReleaseNode
    item_node_map = {
      node.model : node for node in
        [ArtistNode, LabelNode, ReleaseNode]
    }
    return item_node_map[type(discogs_item)](
      discogs_item, runner)

  def __init__(self, discogs_item, runner):
    self.item = discogs_item # Allows for lazy loading
    self.runner = runner
    self.cache = {}

  def isvalid(self):
    return True

  def _text(self):
    return '{}: {}'.format(
      self.item.__class__.__name__.capitalize(), self._name())

  def _name(self):
    raise NotImplementedError()

  def _title(self):
    return '<a target="_blank" href="{}">link</a>, score: {}, title: {}'.format(
      self._get('url'),
      round(self._score(), 5),
      self._text())

  def _score(self):
    return 0

  def _color(self):
    raise NotImplementedError()

  def _get(self, attr):
    self.cache[attr] = throttling.safeget(self.item, attr)

    return self.cache[attr] # Assumes attrs dont change

  def _getlist(self, attr):
    return [x for x in self._safeiter(self._get(attr))] # Avoid putting in the cache to save memory

  def _fetch(self, attr):
    self.cache[attr] = throttling.wrap(self.item.fetch)(attr)

    return self.cache[attr] # Assumes attrs dont change

  def __str__(self):
    return '{}-{}'.format(str(type(self.item).__name__).lower(), self.item.id)

  def __hash__(self):
    return hash(str(self))

  def _filter_masters(self, items):
    return [
      throttling.safeget(x, 'main_release')
      if type(x) == Master else x for x in items
    ]

  def related(self):
    return DiscogsFrontier(
      artists=self._related_artistnodes(),
      labels=self._related_labelnodes(),
      releases=self._related_releasenodes(),
      pop_order=self.runner.selection_order
    )

  def _to_nodes(self, Ctor, discogs_items):
    return [Ctor(x, self.runner) for x in discogs_items
            if x is not None]

  def _related_artistnodes(self):
    from node.artist_node import ArtistNode
    return self._to_nodes(
      ArtistNode, self._related_artists())

  def _related_labelnodes(self):
    from node.label_node import LabelNode
    return self._to_nodes(
      LabelNode, self._related_labels())

  def _related_releasenodes(self):
    from node.release_node import ReleaseNode
    return self._to_nodes(
      ReleaseNode, self._related_releases())

  def _related_artists(self):
    return []

  def _related_labels(self):
    return []

  def _related_releases(self):
    return []

  def _safeiter(self, lst):
    try:
      iterator = iter(lst)
      while True:
        yield throttling.safenext(iterator)
    except StopIteration:
      return
