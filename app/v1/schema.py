from typing import List, Any, Dict
from pydantic import BaseModel


class BasicReturn(BaseModel):
    message: dict


class GetDetection(BaseModel):
    image_url: str


class GetModelResult(BaseModel):
    total_faces: int