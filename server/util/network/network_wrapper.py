import logging
from pyvis.network import Network

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class NetworkWrapper(object):
  def __init__(self):
    self.network = Network(height="100%", width="100%", bgcolor="#222222", font_color="white")
    self.network.barnes_hut()
    self.network.inherit_edge_colors_from(False)

  '''
  entries from node_generator:
  node (NetworkNode)
  parent_hash (can be None)
  '''
  def populate(self, node_generator):
    for entry in node_generator:
      node, parent_hash = entry
      logger.debug(str(hash(node)))
      self.network.add_node(
        hash(node), node.text,
        color=node.color,
        title=node.title)

      if parent_hash:
        self.network.add_edge(hash(node), parent_hash)

  def render(self, filename):
    full_fname = '{}.html'.format(filename)
    logger.info('saving to {}'.format(full_fname))
    self.network.show(full_fname)

