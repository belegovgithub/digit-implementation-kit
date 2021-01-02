from common import create_boundary
from config import load_revenue_boundary_config
import json
import io
import os
from pathlib import Path
import os, sys
  
from common import superuser_login, upsert_localization
from processing.generate_localization_data import process_boundary_file
from config import config

def main():
    create_boundary(load_revenue_boundary_config, "REVENUE")

    boundary_path = config.MDMS_LOCATION / config.CITY_NAME.lower() / "egov-location" / "boundary-data.json"
    auth_token = superuser_login()["access_token"]
    process_boundary_file(auth_token, boundary_path, write_localization=True, generate_file=False)


if __name__ == "__main__":
    main()
