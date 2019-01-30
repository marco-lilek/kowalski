import functools
import logging
from datetime import datetime

from discogs_client_wrapper import DiscogsClientWrapper
from node.label_node import LabelNode
from util.search import search
from discogs_frontier import DiscogsFrontier
from util.network.network_wrapper import NetworkWrapper
import util.exception as exception
import tempfile
import os

class Runner(object):
  def __init__(self, selection_order):
    self.selection_order = selection_order
    self.max_items = 100

  def build_network(self, url):
    discogs_client = DiscogsClientWrapper(self)
    root_node = discogs_client.get_discogs_node(url)

    network = NetworkWrapper()

    network.populate(
      discogs_client.search(root_node, self.max_items))
    handle, fname = tempfile.mkstemp(
      'discogs_scraper-{}-{}'.format(
        str(root_node),
        datetime.now().strftime('%y-%m-%d-%H-%M-%S')))

    network.render(fname)
    os.close(handle)

