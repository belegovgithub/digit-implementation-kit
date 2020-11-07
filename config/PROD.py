from pathlib import Path

from config.global_config import config
from attrdict import AttrDict

config.MDMS_LOCATION = Path(r"D:/eGov/egov-mdms-data/data/pb")

## Node
config.HOST = "https://13.71.65.215.nip.io"

SUPERUSER = AttrDict()

SUPERUSER.username = "superuser"
SUPERUSER.password = "UW1Wc1FERXlNelE9"
SUPERUSER.tenant_id = "pb"

config.SUPERUSER = SUPERUSER
