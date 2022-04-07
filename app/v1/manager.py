import io
import os
import re
import cv2
import base64
import logging
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt

import urllib.request
from urllib.error import HTTPError

import pandas as pd
from PIL import Image

from age_classification.manager.manager import ModelManager as age_model


class ModelManagement:
    def __init__(self, height, width, threshold):
        self.age_model = age_model()
        self.age_model.load_model(self.locate_model("./model/weights.h5"))
        self.image_height = height
        self.image_width = width
        self.threshold = threshold
        self.colors = None
        self.models = None
        self.models_eye = None
        self.labels = None

    @staticmethod
    def locate_model(path_name: str):
        path_dir = os.path.dirname(os.path.realpath(__file__))
        file_name_age_model = os.path.basename(path_name)
        path_model_age = os.path.join(path_dir, file_name_age_model)
        return path_model_age

    @staticmethod
    def get_hist_age(df: dict, fields: list):
        for field in fields:
            figure, (ax1) = plt.subplots(1, 1, figsize=(9, 4))
            v_dist_1 = df[field].values
            sns.histplot(v_dist_1, ax=ax1, color="blue", kde=True)

            mean = df[field].mean()
            median = df[field].median()
            mode = df[field].mode().values[0]

            ax1.axvline(mean, color='r', linestyle='--', label="Mean")
            ax1.axvline(median, color='g', linestyle='-', label="Mean")
            ax1.axvline(mode, color='b', linestyle='-', label="Mode")
            ax1.legend()
            plt.grid()
            plt.title(f"Histograma - Idade")
            return figure

    @staticmethod
    def fig_to_base64(fig):
        img = io.BytesIO()
        fig.savefig(img, format='png',
                    bbox_inches='tight')
        return base64.b64encode(img.getvalue()).decode('utf-8')

    @staticmethod
    def url_to_image(url: str):
        """ convert url to an image in cv2 """
        try:
            response = urllib.request.urlopen(url)
            image = np.asarray(bytearray(response.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            return image
        except HTTPError as error:
            logging.info(error)
            return None

    @staticmethod
    def normalize_url(url: str) -> str:
        if not re.search("^http", url):
            url = f"http://{url}"
        return url

    @staticmethod
    def show_image(image: object, title: str, colorspace: object):
        dpi = 96
        fig_size = (image.shape[1] / dpi, image.shape[0] / dpi)
        fig, ax = plt.subplots(figsize=fig_size, dpi=dpi)
        if colorspace == 'RGB':
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), interpolation='spline16')
        if colorspace == 'gray':
            plt.imshow(image, cmap='gray')
        plt.title(title, fontsize=12)
        ax.axis('off')
        return fig

    def load_model(self, model_path: str):
        self.models = cv2.CascadeClassifier(model_path)

    def load_model_eye(self, model_path: str):
        self.models_eye = cv2.CascadeClassifier(model_path)

    def face_detection(self, url: str, verbose=True):
        html_plot = ""
        model_result = {"total_faces": 0, "boxes": {}}
        image = self.url_to_image(self.normalize_url(url))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = self.models.detectMultiScale(gray, 1.1, 4)

        crop_faces = list()
        for index, (xi, yi, width, height) in enumerate(faces):
            crop_faces.append(gray[yi:yi + height, xi:xi + width])
            cv2.rectangle(image, (xi, yi), (xi + width, yi + height), (255, 0, 0), 2)

        original_image = self.show_image(image, "Face Detection", "RGB")
        original_image_encoded = self.fig_to_base64(original_image)
        original_image_html = f'data:image/png;base64,{original_image_encoded}'
        if verbose:
            fig = plt.figure(figsize=(12, 8))
            axes = []
            columns = 5
            total = len(crop_faces)
            rows = total // columns
            rows += total % columns
            dataframe = {"age": []}
            for index, crop in enumerate(crop_faces):
                image_crop = np.array(Image.fromarray(crop.astype(np.uint8)).resize((48, 48))).astype('float32')
                image_crop = cv2.cvtColor(image_crop, cv2.COLOR_GRAY2RGB)
                image_crop = image_crop.reshape(1, 48, 48, 3)
                predict_age = self.age_model.predict_image(image_crop, False)
                dataframe["age"].append(predict_age)

                axes.append(fig.add_subplot(rows, columns, index + 1))
                axes[-1].set_title(f"Predict: {predict_age} anos")
                plt.imshow(crop, cmap='gray')
                fig.tight_layout()
            encoded = self.fig_to_base64(fig)
            html_plot = f'data:image/png;base64,{encoded}'

        dataframe = pd.DataFrame(dataframe)
        fig_histogram = self.get_hist_age(dataframe, ["age"])
        encoded_histogram = self.fig_to_base64(fig_histogram)
        html_plot_histogram = f'data:image/png;base64,{encoded_histogram}'
        model_result["total_faces"] = len(faces)
        return {"face_detection": original_image_html, "age_prediction": html_plot, "histogram": html_plot_histogram}
