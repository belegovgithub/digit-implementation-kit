from common import superuser_login, update_property_status

properties = (
    ('PT-101-1222', 'pb.testing'),
)

if __name__ == "__main__":
    login = superuser_login()
    auth_token = login["access_token"]

    update_property_status(auth_token, properties, "ACTIVE")