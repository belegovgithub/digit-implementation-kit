from config import config
from common import get_employees_by_phone, superuser_login


def main():
    auth_token = "e70eaa4b-29e7-4f71-a912-35baa6147b64"
    get_employees_by_phone(auth_token,"9480734475", "pb")
    

if __name__ == "__main__":
    main()
