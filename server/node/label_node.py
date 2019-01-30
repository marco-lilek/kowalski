from discogs_client.models import Label
from node.discogs_node import DiscogsNode

class LabelNode(DiscogsNode):
  model = Label
  def __init__(self, discogs_label, runner):
    super().__init__(discogs_label, runner)

  def _name(self):
    return self._get('name')

  def _color(self):
    return '#0000ff'

  def _related_releases(self):
    return self._filter_masters(self._getlist('releases'))

  def _related_labels(self):
    rl =  self._getlist('sublabels') + [self._get('parent_label')]
    return rl

