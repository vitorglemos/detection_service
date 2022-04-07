FROM python:3.7
RUN apt-get install python3-distutils
RUN mkdir /app


RUN pip install --upgrade pip==21.3.1
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install setuptools==57.0.0
COPY . /app
COPY ./requirements.txt /app

WORKDIR /app


RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "run:app", "--host=0.0.0.0", "--port=8100", "--reload"]
