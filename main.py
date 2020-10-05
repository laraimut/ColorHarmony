import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2
from Solver import Solver
import PIL as PIL
from PIL import Image
from PIL import ImageTk

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	return render_template('home.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		# images=cv2.imread(path)
		# filename,score,time,scoreawal = Solver.Skripsi(images,0)
		# LastScore = score
		im = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		filenames,score,time,scoreawal = Solver.Skripsi(im,0)
		print(filenames)
		print(score)
		if score > 2:
			scorevalue = "Sangat Baik"
		elif score > 1.5 and score < 2:
			scorevalue = "Baik"
		else:
			scorevalue = "Kurang Baik"
		print(scorevalue)
		flash('This is your poster')
		return render_template('home.html', filename=filename,filenames=filenames,score=score,scorevalue=scorevalue)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	CV_LOAD_IMAGE_COLOR = 1 # set flag to 1 to give colour image
	CV_LOAD_IMAGE_COLOR = 0 # set flag to 0 to give a grayscale one
	# im = cv2.imread("C:/test.png")
	# path = url_for('static', filename=filename)
	# print(im)
	# filenames,score,time,scoreawal = Solver.Skripsi(im,0)
	# print(filenames)
	# print(score)
	# if score > 2:
	# 	scorevalue = "Sangat Baik"
	# elif score > 1.5 and score < 2:
	# 	scorevalue = "Baik"
	# else:
	# 	scorevalue = "Kurang Baik"
	# print(scorevalue)
	return redirect(url_for('static', filename=filename), code=301)

@app.route('/display/<filenames>')
def finish_image(filenames):
	return redirect(url_for('static',filenames=filenames), code=301)

if __name__ == "__main__":
	app.run()
