# For debugging, should be avoided
def main():
  import functools
  import logging
  from datetime import datetime

  from discogs_client_wrapper import DiscogsClientWrapper
  from node.label_node import LabelNode
  from util.search import search
  from discogs_frontier import DiscogsFrontier
  from util.network.network_wrapper import NetworkWrapper

  logging.basicConfig(level=logging.INFO)

  url = 'https://www.discogs.com/Various-Bosconi-Stallions-Apacz/release/4673161'
  discogs_client = DiscogsClientWrapper()
  root_node = discogs_client.get_discogs_node(url)

  network = NetworkWrapper()

  network.populate(discogs_client.search(root_node, 100))
  filename = '{}-{}'.format(
    str(root_node), datetime.now().strftime('%y-%m-%d-%H-%M-%S'))

  network.render(filename)

if __name__ == '__main__':
  main()
