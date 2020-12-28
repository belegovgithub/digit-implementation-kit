from config import config
from common import unlock_user, superuser_login


def main():
    auth_token = superuser_login()["access_token"]
    unlock_user(auth_token, "pb.dalhousie", "DEV_DALHOUSIE_EMP")
    print("User is unlocked")


if __name__ == "__main__":
    main()
