from config import config
from common import update_user_password, superuser_login


def main():
    auth_token = superuser_login()["access_token"]
    update_user_password(auth_token, "pb.dalhousie", "DEV_DALHOUSIE_EMP", "Bel@1234")
    print("Password is updated")


if __name__ == "__main__":
    main()
