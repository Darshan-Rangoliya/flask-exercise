from secrets import token_hex

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:darshan@localhost:5432/blog'
SECRET_KEY = token_hex()
API_TITLE = 'My First Api'
API_VERSION = 'v1'
OPENAPI_VERSION = '3.0.2'