from pathlib import Path
import os
from .global_config import config

config.BOUNDARIES_FOLDER = Path(r"D:/eGov/Data/CB data/CB Ahmednagar")

config.MDMS_LOCATION = Path(r"D:/eGov/egov-mdms-data/data/pb")

config.TENANT = "pb"
config.CITY_NAME = os.getenv("CITY", None) or "Ahmednagar"

config.CONFIG_ENV = "PROD"

import importlib

importlib.import_module("." + config.CONFIG_ENV, "config")
