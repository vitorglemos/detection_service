import json
from .__version__ import __version__
from cached_property import cached_property

from app.v1.manager import ModelManagement


class Config:
    def __init__(self, config_json):
        self.app_name = config_json["app"].get("name")
        self.description = config_json["app"].get("description")
        self.version = __version__

        self.author = config_json["author"]
        self.license = config_json["license"]

        self.host = config_json["fastapi"].get("host")
        self.port = config_json["fastapi"].get("port")

        self.model_face = config_json["model"].get("face_model")
        self.model_age = config_json["model"].get("age_model")

        self.img_height = config_json["image"].get("height")
        self.img_width = config_json["image"].get("width")

    @cached_property
    def manager(self) -> ModelManagement:
        return ModelManagement(height=self.img_height, width=self.img_width, threshold=self.model_threshold)
