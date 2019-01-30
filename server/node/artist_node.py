from discogs_client.models import Artist
from node.discogs_node import DiscogsNode
from node.node_type import NodeType

class ArtistNode(DiscogsNode):
  VARIOUS_ARTIST_ID = 194
  model = Artist

  def __init__(self, discogs_artist, runner):
    super().__init__(discogs_artist, runner)

  def isvalid(self):
    if self.item.id == self.VARIOUS_ARTIST_ID:
      return False # "Various" artist doesn't actually exist, returns a 404 when queried
    return True

  def _name(self):
    return self._get('name')

  def _color(self):
    return '#ff0000'

  def _related_releases(self):
    if not self.isvalid():
      return []
    return self._filter_masters(self._getlist('releases'))

  def _related_artists(self):
    if not self.isvalid():
      return []

    return self._getlist('aliases')
