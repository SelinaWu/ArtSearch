import os
from app import app
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import requests
import sys


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
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
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		resp = requests.post(url=db_url,json={'upload':filename})
		#return resp.content
		img_url = str(resp.text)

		print(img_url)
		
		#return filename
		if img_url =='':
			flash('No similar image found')
			return redirect(request.url)

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