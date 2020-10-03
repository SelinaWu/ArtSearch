import os
from app import app
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import requests
import sys
import pandas as pd
import numpy as np


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def postprocess(filename, image_file):
	"""
	Convert the image to 32x1 vector
	save it into a df to convert to csv file
	"""
	df = pd.DataFrame()
	image_file = cv2.cvtColor(image_file, cv2.COLOR_BGR2GRAY)
    image_file = cv2.resize(image_file, dsize = (32,32))
    pca = PCA(n_components=1)
    img = pca.fit_transform(image_file)
	df = df.append(pd.Series([filename]+img.reshape(1,-1)[0].tolist()), ignore_index = True)
	df = df.set_index([0])
	return df


	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	# user select an image to upload
	# send image to main DB
	# receive cosine similar image
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)

		# TODO: save uploaded image to the database
		# 1. convert it to a csv file
		# 2. upload the csv file to db
		file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

		file.save(file_path)
		image_data = cv2.imread(file_path)
		df = postprocess(filename, image_data) # a pandas df

		csv_name = filename.split('.')[0]
		resp = requests.post(url=db_url,json={'upload':csv_name})
		#return resp.content
		img_url = str(resp.text)
		
		#return filename
		if img_url =='':
			flash('No similar image found')
			return redirect(request.url)

		# delete the image file and the csv file in UPLOAD_FOLDER


		return render_template('upload.html', img_url = img_url)
		#return render_template('upload.html', filename = filename)
	
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<img_url>' )
def display_image(img_url):
	# receive cosine similar image filename and display
	
	return img_url


if __name__=="__main__":
    # determine what the URL for the database should be, port is always 8082 for DB
    if(len(sys.argv) == 2):
        db_url = 'http://' + sys.argv[1] + ':8082'
    else:
        db_url = "http://0.0.0.0:8082/"  
   
    app.run(host='0.0.0.0', port=8081, debug=True)	