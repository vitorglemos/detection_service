import json
import uvicorn

from pathlib import Path

from app.config import Config
from app.factory import create_app

with open(str(Path(__file__).parents[0] / ".config.json")) as fb:
    config = Config(json.load(fb))
    app = create_app(config)

if __name__ == '__main__':
    uvicorn.run("run:app", host="127.0.0.1", port=8100, log_level="info")