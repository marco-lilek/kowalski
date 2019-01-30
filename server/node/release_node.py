import math
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from discogs_client.models import Release
from node.discogs_node import DiscogsNode

class ReleaseNode(DiscogsNode):
  model = Release
  def __init__(self, discogs_release, runner):
    super().__init__(discogs_release, runner)

  def _name(self):
    return self._get('title')

  def _color(self):
    return '#00{0:0>2x}00'.format(
      max(30, int(self._score() * 255)))

  def _score(self):
    community = self._fetch('community')
    rating = community['rating']['average']
    want = community['want']
    have = community['have']
    score = ( 1.0 / (1.0 + math.exp( - want / (have + 1))))
    if rating != 0:
        score = 0.5 * (rating / 5.0) + 0.5 * score

    logger.debug('rating {} want {} have {} score {}'.format(rating, want, have, score))
    return score

  def _related_artists(self):
    return self._getlist('artists')
