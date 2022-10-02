import databases

from starlette.applications import Starlette
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret


# Config will be read from environment variables and/or ".env" files.
config = Config("api.env")

PROJECT_NAME = "cbh_api"
VERSION = "1.0.0"
API_PREFIX = "/api"

SECRET_KEY = config("SECRET_KEY", cast=Secret, default="CHANGEME")

DEBUG = config('DEBUG', cast=bool, default=False)
POSTGRES_USER = config('POSTGRES_USER', cast=str, default=False)
POSTGRES_PASSWORD = config('POSTGRES_PASSWORD', cast=Secret)
POSTGRES_SERVER= config('POSTGRES_SERVER', cast=str, default="db")
POSTGRES_HOST = config('POSTGRES_HOST', cast=str, default=False)
POSTGRES_PORT = config('POSTGRES_PORT', cast=int, default="5435")
POSTGRES_DB= config('POSTGRES_DB', cast=str, default=False)
DATABASE_URL = config(
    'DATABASE_URL', 
    cast=databases.DatabaseURL,
    default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )