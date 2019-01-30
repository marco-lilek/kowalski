import re
import logging
from discogs_client.exceptions import HTTPError
import util.exception as exception

RATE_LIMIT_ERROR_CODES = [429]
SLEEP_SEC = 65

def wrap(f):
  return exception.retry_and_sleep(
    RATE_LIMIT_ERROR_CODES, SLEEP_SEC, f)

safeget = wrap(getattr)
safenext = wrap(next)
