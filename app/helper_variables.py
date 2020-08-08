import secrets

# user roles
user_admin = "admin"
user_agronimist  = "agronomist"
user_customer = "customer"


# file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


# gen unique values
unque_value = secrets.token_hex(10) + '.'
