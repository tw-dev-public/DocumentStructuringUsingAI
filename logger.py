import logging
import os

LOG_LEVEL = os.getenv("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s [%(levelname)s] %(message)s")