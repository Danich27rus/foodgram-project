import environ
import os

from pathlib import Path

env = environ.Env()
environ.Env.read_env()

PROD = os.environ.get("PROD")

if PROD:
    from .settings_prod import *
else:
    from .settings_dev import *
