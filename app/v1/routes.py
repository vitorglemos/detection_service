from ..__version__ import __version__

import os

from app.v1 import schema
from app.v1 import helper
from app.v1 import manager

from fastapi import APIRouter, Request, Form
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates


def locate_model():
    path_dir = os.path.dirname(os.path.realpath(__file__))
    file_name_face_model = os.path.basename("./model/haarcascade_frontalface_default.xml")
    path_model_face = os.path.join(path_dir, file_name_face_model)
    return path_model_face


router_v1 = APIRouter(prefix="/v1")

loaded_model = manager.ModelManagement(1024, 1024, 0.4)
loaded_model.load_model(locate_model())

templates = Jinja2Templates("html")


@router_v1.get('/home', tags=["html_page"])
async def write_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router_v1.post('/submitform', tags=["html_page"])
async def submit_handle_form(request: Request, assignment: str = Form(...)):
    ret_value = await helper.detections(assignment, loaded_model)
    context = {"request": request,
               "age_prediction": ret_value["age_prediction"],
               "histogram": ret_value["histogram"],
               "face_detection": ret_value["face_detection"]}
    return templates.TemplateResponse("index.html", context=context)


@router_v1.post('/predict', response_model=schema.GetModelResult, tags=["prediction"])
async def predict(url: schema.GetDetection):
    ret_value = await helper.detections(url.image_url, loaded_model)
    return JSONResponse(content=jsonable_encoder(ret_value))


@router_v1.post('/predict', response_model=schema.GetModelResult, tags=["prediction"])
async def predict(url: schema.GetDetection):
    ret_value = await helper.detections(url.image_url, loaded_model)
    return JSONResponse(content=jsonable_encoder(ret_value))


@router_v1.get('/version', tags=["version"])
async def version() -> JSONResponse:
    return JSONResponse({"version": __version__})
