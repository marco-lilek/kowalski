import re

from discogs_client import Client
from node.discogs_node import DiscogsNode
from discogs_frontier import DiscogsFrontier
import util.search as search

class NotDiscogsUrlException(Exception):
  pass

class DiscogsClientWrapper(object):
  DISCOGS_DOMAIN = 'www.discogs.com'

  def __init__(self, runner):
    self.client = Client('DiscogsVisualizer', user_token='uSlXGFkaTQowGbHJrHibZhkymIyCwARLgFvuuvyS')
    self.runner = runner

  @classmethod
  def is_discogs_url(cls, url):
    return re.search(cls.DISCOGS_DOMAIN, url)

  def _get_discogs_item(self, url):
    match = re.search('/([a-z]+)/(\d+)'.format(
      self.DISCOGS_DOMAIN), url)
    itype, iid = match.group(1), int(match.group(2))
    return getattr(self.client, itype.lower())(iid)

  def get_discogs_item(self, url):
    if not self.is_discogs_url(url):
      raise NotDiscogsUrlException()
    return self._get_discogs_item(url)

  def get_discogs_node(self, url):
    discogs_item = self.get_discogs_item(url)
    return DiscogsNode.from_item(discogs_item, self.runner)

  def search(self, start_node, max_items=10):
    frontier = DiscogsFrontier(artists=[], labels=[], releases=[], pop_order=self.runner.selection_order)

    num_items = 0
    for node, parent_hash in search.search(start_node, frontier):
      if num_items > max_items:
        break

      if not node.isvalid():
        continue

      yield node, parent_hash
      num_items += 1

    return

