from flask.blueprints import Blueprint
from flask import render_template, request
import time
import pickle
import numpy as np
import os

from tensorflow.keras.preprocessing.sequence import pad_sequences

from model import model, tokenizer, model_predict


class MainpageBlueprint:
 
    def __init__(self):
        self.__bp = Blueprint("mainpage","mainpage",url_prefix="/")
        self.__bp.route("/")(self.route)


    def route(self):
        return render_template("index.html")

    def get_blueprint(self):
        return self.__bp



class ResponseBlueprint:

    

    def __init__(self):
        self.__bp = Blueprint("request","request",url_prefix="/request")
        self.__bp.route("/",methods=["POST"])(self.route_post)
        self.__bp.route("/",methods=["GET"])(self.route_get)


    def route_post(self) -> str:

        message1 = str(request.form.get("message1"))
        
        model_ = model
        tok_ = tokenizer

        result = model_predict(model_, tok_, message1)

        return f"{result[0][0]}|{result[0][1]}\n{result[1][0]}|{result[1][1]}\n{result[2][0]}|{result[2][1]}";

    def route_get(self) -> str:
        return "<h1><font color=red>Forbidden!</font> You can not access to /request/ by get_method.</h1>"

    def get_blueprint(self):
        return self.__bp
