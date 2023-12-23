import os

from fastapi import FastAPI
from importlib.util import find_spec
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi_django.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fastapi_django.settings")


app = FastAPI()
application = get_wsgi_application()

app.mount("/", WSGIMiddleware(application))
app.mount("/static",
    StaticFiles(
         directory = os.path.normpath(
              os.path.join(find_spec("django.contrib.admin").origin, "..", "static")
         ),
   ),
   name = "static",
)