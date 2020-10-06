from pathlib import Path

from config.global_config import config
from attrdict import AttrDict

config.MDMS_LOCATION = Path(r"/content/egov-mdms-data/data/pb")

## Node
config.HOST = "https://13.71.65.215.nip.io"

SUPERUSER = AttrDict()

SUPERUSER.username = ""
SUPERUSER.password = ""
SUPERUSER.tenant_id = "pb"

config.SUPERUSER = SUPERUSER
