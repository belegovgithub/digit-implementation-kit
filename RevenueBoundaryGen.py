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
    auth_token = superuser_login()["access_token"]
    create_boundary(auth_token,load_revenue_boundary_config, "REVENUE",write_localization=False)
 

if __name__ == "__main__":
    main()
