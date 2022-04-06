

async def detections(image_url, loaded_model):
    return loaded_model.face_detection(image_url)
