
from flask import Flask, request, jsonify
from flask.views import MethodView
from flask_smorest import abort, Blueprint
import uuid
import os
from PIL import Image
import pytesseract
from pytesseract import Output
import re


bpl = Blueprint("getss",__name__,description="OCR REST API")

@bpl.route('/image')
class restApi(MethodView):

	def __init__(self):
		if not request.files:
			abort(400)

	#@bpl.response(201,Schema)
	def post(self):

		file = request.files['file']
		filename = ''

		filename = str(uuid.uuid4()) + '.' + request.files['file'].filename.split('.')[1]

		#filename = secure_filename(file.filename)

		# filepath to save image
		file.save(os.path.join(os.getcwd(), 'static', 'upload', 'image', '', filename))

		custom_config = r'-l eng --oem 3 --psm 1'
		_text_ = pytesseract.image_to_string(
		    Image.open(os.path.join(os.getcwd(), 'static', 'upload', 'image', '', filename)),
		    output_type=Output.DICT,
		    config=custom_config
		    )

		image_text = list(dict.fromkeys(re.sub("[^A-Z 0-9]", "", _text_['text'],0,re.IGNORECASE).split(" ")))
		#print(image_text)

		# response = 'File successfully uploaded'
		return jsonify({"text": image_text}), 201