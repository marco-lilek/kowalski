class NetworkNode(object):
  @property
  def text(self):
    return self._text()

  @property
  def color(self):
    return self._color()

  @property
  def title(self):
    return self._title()

  def _text(self):
    raise NotImplementedError()

  def _color(self):
    raise NotImplementedError()

  def _title(self):
    raise NotImplementedError()
