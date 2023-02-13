
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
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bpl.route('/image')
class restApi(MethodView):

	

	def __init__(self):
		if not request.files:
			abort(400)

	

	#@bpl.response(201,Schema)
	def post(self):

		file = request.files['file']
		filecheckname = file.filename
		savefilename = ''

		if file and allowed_file(file.filename):

			savefilename = str(uuid.uuid4()) + '.' + request.files['file'].filename.split('.')[1]

			#filename = secure_filename(file.filename)

			# filepath to save image
			file.save(os.path.join(os.getcwd(), 'static', 'upload', 'image', '', savefilename))

			custom_config = r'-l eng --oem 3 --psm 1'
			_text_ = pytesseract.image_to_string(
			    Image.open(os.path.join(os.getcwd(), 'static', 'upload', 'image', '', savefilename)),
			    output_type=Output.DICT,
			    config=custom_config
			    )

			image_text = list(dict.fromkeys(re.sub("[^A-Z 0-9]", "", _text_['text'],0,re.IGNORECASE).split(" ")))
			#print(image_text)

			os.remove(os.path.join(os.getcwd(), 'static', 'upload', 'image', '', savefilename))

			# response = 'File successfully uploaded'
			if len(image_text) > 1:
				return jsonify({"text": image_text}), 200
			else:
				return jsonify({"text": 'No text found in image'}), 400
		else:
			return jsonify({"message": 'Allowed file types are png, jpg, jpeg'}), 400