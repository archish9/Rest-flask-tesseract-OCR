import os
from flask import Flask, request
from flask_smorest import Api
from resources.ocr_core import bpl as ImgApi
from flask import Flask, jsonify
from  dotenv import load_dotenv

def create_app(db_url=None):

	app = Flask(__name__)

	load_dotenv()

	app.config["PROPAGATE_EXCEPTIONS"] = True
	app.config["API_TITLE"] = "OCR flask REST API"
	app.config["API_VERSION"] = "v1"
	app.config["OPENAPI_VERSION"] = "3.0.3"
	app.config["OPENAPI_URI_PREFIX"] = "/"
	app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
	app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
	
	api = Api(app)
 	 	

	# @app.before_first_request
	# def create_tables():
	# 	db.create_all()

		
	api.register_blueprint(ImgApi)
	return app