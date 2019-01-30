import time
import logging
import functools

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def catchall(func):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except Exception as e:
      import traceback
      traceback.print_exc()

  return wrapper

def retry(status_codes, func, handler):
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    while True:
      try:
        return func(*args, **kwargs)
      except Exception as e:
        try:
          if e.status_code in status_codes:
            handler(e)
          else:
            raise
        except:
          raise e
  return wrapper

def log_and_sleep(sleep_sec, e):
  logger.debug(e)
  time.sleep(sleep_sec)

def retry_and_sleep(status_codes, sleep_sec, func):
  return retry(
    status_codes,
    func,
    handler=functools.partial(log_and_sleep, sleep_sec))
