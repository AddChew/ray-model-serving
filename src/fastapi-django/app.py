import os

from ray import serve
from fastapi import FastAPI
from importlib.util import find_spec
from fastapi.staticfiles import StaticFiles

from fastapi_django.wsgi import application
from fastapi.middleware.wsgi import WSGIMiddleware
from ray.serve._private.http_util import BufferedASGISender


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fastapi_django.settings")


def setup_app():
     app = FastAPI()
     app.mount("/static",
     StaticFiles(
          directory = os.path.normpath(
               os.path.join(find_spec("django.contrib.admin").origin, "..", "static")
          ),
     ),
     name = "static",
     )
     app.mount("/", WSGIMiddleware(application))
     return app
    

@serve.deployment(num_replicas = 2)
class Deployment:
    
    def __init__(self):
        self.app = setup_app()

    async def __call__(self, request):
        sender = BufferedASGISender()
        await self.app(request.scope, receive = request.receive, send = sender)
        return sender.build_asgi_response()
    

deployment = Deployment.bind()