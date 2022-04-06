import logging

from fastapi import FastAPI

from .config import Config

from fastapi.encoders import jsonable_encoder
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from .v1.routes import router_v1


def error_handling(request: Request, exec):
    return JSONResponse(status_code=500, content=jsonable_encoder({"detail": str(exec)}))


def create_app(config: Config):
    app = FastAPI(title=config.app_name,
                  description=config.description,
                  version=config.version,
                  contact=config.author,
                  license_info=config.license
                  )
    app.include_router(router_v1)
    app.add_exception_handler(500, error_handling)

    @app.get("/health")
    async def health_return(request: Request) -> JSONResponse:
        return JSONResponse(True, status_code=200)

    return app
