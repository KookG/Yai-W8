# import ส่วนของ flask framework
from flask import Flask, render_template, request, jsonify
import cv2 # OpenCV module
import numpy as np # numpy ใช้เรื่องโครงสร้างข้อมูลขั้นสูงและทางคณิตศาสตร์
import os # ใช้สำหรับจัดการไฟล์และโฟลเดอร์

# module ที่เขียนเอง ไฟล์ imgcvt.py
from imgcvt import base64_cvimage, cvimage_base64

# สร้าง Flask app (Flask framework object)
app = Flask(__name__)

# route /
@app.route('/')
def index():
	return render_template('index.html')

# route /workshop01
@app.route('/workshop01')
def workshop01():
	return render_template('workshop01.html')

# route /workshop02
@app.route('/workshop02')
def workshop02():
	return render_template('workshop02.html')

########## WORKSHOP01 Image Processing (Shape detection) ##########
# route /wp1_backend
@app.route('/wp1_backend_shape', methods=['POST'])
def wp1_backend_shape():
	try:
		# รับข้อมูลจาก frontend request
		data = request.get_json()
		if not data:
			return jsonify({'error': 'No data provided'}), 400

		# parameters json data.parameters
		

		########## รับข้อมูลจาก frontend (request) แล้วแปลงเป็น OpenCV Image ##########
		image_src = base64_cvimage(data['imageBASE64'])

		########## ตัวอย่างการทำงาน Shape detection ##########
		# การทำงาน
		# (1) preprocess image
		# (2) canny edge detect
		# (3) find contours
		# (4) contours filter
		# (5) draw contour and count

		# แปลงเป็นภาพขาวดำ (1)
		

		# เพิ่มความสว่างให้กับภาพ (1)
		

		# ลดความละเอียดของภาพ หรือลด noise (1)
		

		# gray to binary: black and white (1)
		

		# edge detection (2)
		

		# ค้นหา contours (3)
		

		# กรอง contours ที่ไม่ต้องการออก (4)
		coins = 0
		
		# วาด contour ที่ผ่านการกรองแล้ว (5)

		
		# สำเนาไป image_output
		image_output = image_src.copy()

		########## ส่งข้อมูล OpenCV Image กลับไปยัง frontend (response) ##########
		image_base64 = cvimage_base64(image_output)

		# สร้าง python dictionary สำหรับ response กลับไปยัง frontend
		output = {
			'message': '',
			'coins': coins,
			'image': {
				"imageBASE64": image_base64,
				"type": data["type"],
				"width": data["width"],
				"height": data["height"],
			}
		}
		return jsonify(output), 200
	except Exception as e:
		return jsonify({'error': str(e), 'data': data}), 500

########## WORKSHOP01 Image Processing (Hough circle detection) ##########
# route /wp1_backend
@app.route('/wp1_backend_hough', methods=['POST'])
def wp1_backend_hough():
	try:
		# รับข้อมูลจาก frontend request
		data = request.get_json()
		if not data:
			return jsonify({'error': 'No data provided'}), 400
		
		# parameters json data.parameters
		

		########## รับข้อมูลจาก frontend (request) แล้วแปลงเป็น OpenCV Image ##########
		image_src = base64_cvimage(data['imageBASE64'])

		########## ตัวอย่างการทำงาน hough circles detection ##########
		# การทำงาน
		# (1) preprocess image
		# (2) hough circles
		# (3) draw circles and count

		# แปลงเป็นภาพขาวดำ (1)
		

		# ลดความละเอียดของภาพ หรือลด noise (1)
		

		# Hough Circles (2)
		

		# วาดวงกลมรอบๆ วงกลมที่ตรวจพบ (3)
		coins = 0
		
		
		# สำเนาไป image_output
		image_output = image_src.copy()

		########## ส่งข้อมูล OpenCV Image กลับไปยัง frontend (response) ##########
		image_base64 = cvimage_base64(image_output)

		# สร้าง python dictionary สำหรับ response กลับไปยัง frontend
		output = {
			'message': '',
			'coins': coins,
			'image': {
				"imageBASE64": image_base64,
				"type": data["type"],
				"width": data["width"],
				"height": data["height"],
			}
		}
		return jsonify(output), 200
	except Exception as e:
		return jsonify({'error': str(e)}), 500

########## WORKSHOP02 HAAR Cascade Object Detection ##########
# route /wp2_backend
@app.route('/wp2_backend', methods=['POST'])
def wp2_backend():
	try:
		# รับข้อมูลจาก frontend request
		data = request.get_json()
		if not data:
			return jsonify({'error': 'No data provided'}), 400

		########## รับข้อมูลจาก frontend (request) แล้วแปลงเป็น OpenCV Image ##########
		image_src = base64_cvimage(data['imageBASE64'])

		########## HAAR Cascade Object Detection ##########
		# การทำงาน
		# (1) preprocess image
		# (2) prepair cascade with pre-trained cascade (xml)
		# (3) detect objects
		# (4) draw bounding boxes

		# แปลงเป็นภาพขาวดำ (1)

		# โหลด pre-trained เพื่อเตรียม cascade (2)
		# ใช้ pre-trained cascade ที่ OpenCV มีมาให้

		# ตัวอย่าง custom cascade
		
		

		# ตรวจจับวัตถุ (3)
		

		# วาดกรอบรอบๆ วัตถุที่ตรวจพบ (4)
		

		# สำเนาไป image_output
		image_output = image_src.copy()

		########## ส่งข้อมูล OpenCV Image กลับไปยัง frontend (response) ##########
		image_base64 = cvimage_base64(image_output)

		# สร้าง python dictionary สำหรับ response กลับไปยัง frontend
		output = {
			'message': '',
			'image': {
				"imageBASE64": image_base64,
				"type": 'image/png',
				"width": data["width"],
				"height": data["height"],
			}
		}
		return jsonify(output), 200
	except Exception as e:
		return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True)