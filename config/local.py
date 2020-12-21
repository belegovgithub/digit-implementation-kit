from pathlib import Path
import os
from .global_config import config

config.BOUNDARIES_FOLDER = Path(r"D:/eGov/Data/CB data/CB Ahmednagar")

config.TL_FOLDER = Path(r"/content/drive/My Drive/Workspace/CB Ahmednagar")

config.HRMS_CMD_FOLDER=Path(r"D:\egov-repo\Production\57CanttBoard\Verified-CB-Data\SC")

config.MDMS_LOCATION = Path(r"D:\egov-repo\egov-mdms-data\data\pb")

config.TENANT = "pb"
config.CITY_NAME = os.getenv("CITY", None) or "Ahmednagar"

config.CONFIG_ENV = "PROD"

import importlib

importlib.import_module("." + config.CONFIG_ENV, "config")
