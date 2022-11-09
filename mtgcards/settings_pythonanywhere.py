import os
from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_ROOT = BASE_DIR / 'static_hosted'

SECRET_KEY = os.environ['SECRET_KEY']