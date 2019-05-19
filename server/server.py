from multiprocessing import Pool
from flask import request
from flask import Flask
import logging

from runner import Runner
import util.exception as exception
from node.node_type import NodeType

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _selection_order(search_type):
  logger.info('Search Type {}'.format(search_type))
  if search_type == 'network':
    return [NodeType.ARTIST, NodeType.LABEL, NodeType.RELEASE]
  if search_type == 'releases':
    return [NodeType.RELEASE, NodeType.ARTIST, NodeType.LABEL]
  raise Exception('Unknown search type {}'.format(search_type))


@exception.catchall
def _build_network(search_type, url):
  runner = Runner(_selection_order(search_type))
  runner.build_network(url)

p = Pool(5)

@app.route('/')
def build_network():
  search_type = request.args.get('type')
  url = request.args.get('url')
  p.apply_async(_build_network, (search_type, url, ))
  return 'OK'

