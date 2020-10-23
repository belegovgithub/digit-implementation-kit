from common import create_boundary
from config import load_revenue_boundary_config
#import processing.process_boundary_localization

def main():
    create_boundary(load_revenue_boundary_config, "REVENUE")
    exec(open('./processing/process_boundary_localization.py').read())


if __name__ == "__main__":
    main()
