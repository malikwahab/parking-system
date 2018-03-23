import os

if os.getenv('HEROKU') is not None:
    from .production import *
else:
    from .development import *
