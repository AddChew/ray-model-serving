import logging

from ray import serve
from flask import Flask
from fastapi import FastAPI

from fastapi.middleware.wsgi import WSGIMiddleware
from ray.serve._private.http_util import BufferedASGISender


def setup_app():
    app = FastAPI()
    flask_app = Flask(__name__)
    logger = logging.getLogger("ray.serve")

    @flask_app.route("/")
    def flask_main():
        logger.info("Flask!")
        return "Hello from Flask!"

    @app.get("/fastapi")
    def main():
        logger.info("FastAPI!")
        return "Hello from FastAPI!"

    app.mount("/flask", WSGIMiddleware(flask_app))

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