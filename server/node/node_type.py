from enum import Enum, auto

class AutoName(Enum):
  def _generate_next_value(name, start, count, last_values):
    return count - 1

class NodeType(AutoName):
  ARTIST = 0
  LABEL = auto()
  RELEASE = auto()

