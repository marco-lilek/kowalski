import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class SearchNode(object):
  def related(self):
    raise NotImplementedError()

'''
start_node is a SearchNode
frontier is an OrderedSet
'''
def search(start_node, frontier):
  seen = set()
  top = start_node
  map_to_parent_hash = {hash(top): None}
  while True:
    logger.debug('Top {}'.format(top))
    logger.debug('Seen {}'.format(seen))
    top_hash = hash(top) if top else None

    if not top:
      return
    elif top_hash not in seen:
      seen.add(top_hash)
      logger.debug(seen)
      yield top, map_to_parent_hash[top_hash]

      related = top.related()
      for item in related:
        # Yes there can be collisions
        map_to_parent_hash[hash(item)] = top_hash
      frontier.extend(related)
      logger.debug('Frontier {}'.format(frontier))

    if not frontier:
      return

    top = frontier.pop()

