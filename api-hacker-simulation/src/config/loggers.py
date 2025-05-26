import logging
import sys

def setup_logging(level: int = logging.INFO) -> None:
    fmt = "%(asctime)s %(levelname)-8s [%(name)s:%(lineno)d] %(message)s"
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt))
    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)