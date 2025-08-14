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
		brightness = int(data['parameters'].get('brightness', 0))
		blur = int(data['parameters'].get('blur', 0))
		area = int(data['parameters'].get('area', 0))

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
		image_output = cv2.cvtColor(image_src, cv2.COLOR_BGR2GRAY)

		# เพิ่มความสว่างให้กับภาพ (1)
		mask = np.full_like(image_output, brightness)
		image_output = cv2.add(image_output, mask)

		# ลดความละเอียดของภาพ หรือลด noise (1)
		image_output = cv2.blur(image_output, (blur, blur))

		# gray to binary: black and white (1)
		_, image_output = cv2.threshold(image_output, 0, 255, cv2.THRESH_BINARY, cv2.THRESH_OTSU)

		# edge detection (2)
		image_output = cv2.Canny(image_output, 0, 255)

		# ค้นหา contours (3)
		contours, _ = cv2.findContours(image_output, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


		# กรอง contours ที่ไม่ต้องการออก (4)
		coins = 0
		for c in contours:
			c_area = cv2.contourArea(c)
			if c_area > area:
				continue


			c_length =cv2.arcLength(c, True)
			if c_length == 0:
				continue

			# หาความกลมของ contour
			circularity = 4 * np.pi * (c_area / (c_length ** 2))
			if circularity < 0.5:   # กำหนด threshold ความกลม
				continue

            coins += 1
	        # วาด contour ที่ผ่านการกรองแล้ว (5)
	        image_src = cv2.drawContours(image_src, [c], -1, (255, 0, 0), 2)

		
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
		blur = int(data['parameters'].get('blur', 0))
		minDist = int(data['parameters'].get('minDist', 0))
		param1 = int(data['parameters'].get('param1', 0))
		param2 = int(data['parameters'].get('param2', 0))
		minRadius = int(data['parameters'].get('minRadius', 0))
		maxRadius = int(data['parameters'].get('maxRadius', 0))

		########## รับข้อมูลจาก frontend (request) แล้วแปลงเป็น OpenCV Image ##########
		image_src = base64_cvimage(data['imageBASE64'])

		########## ตัวอย่างการทำงาน hough circles detection ##########
		# การทำงาน
		# (1) preprocess image
		# (2) hough circles
		# (3) draw circles and count

		# แปลงเป็นภาพขาวดำ (1)
		image_output = cv2.cvtColor(image_src, cv2.COLOR_BGR2GRAY)

		# ลดความละเอียดของภาพ หรือลด noise (1)
		image_output = cv2.GaussianBlur(image_output, (blur, blur), 0)

		# Hough Circles (2)
		circles = cv2.HoughCircles(
			image_output, # input image
			cv2.HOUGH_GRADIENT, # detection method
			dp=1, # อัตราส่วนของความละเอียด
			minDist=minDist, # ระยะห่างขั้นต่ำระหว่างวงกลมที่ตรวจพบ
			param1=param1, # แก้ไขค่าขอบเขตสูงสุดของ Canny edge detector
			param2=param2, # แก้ไขค่าขอบเขตต่ำสุดของ Canny edge detector
			minRadius=minRadius, # รัศมีขั้นต่ำของวงกลมที่ตรวจพบ
			maxRadius=maxRadius # รัศมีสูงสุดของวงกลมที่ตรวจพบ
		)
		#circles ได้เป็น numpy array ที่เก็บข้อมูลของวงกลมที่ตรวจพบ
		#[1, N, (x, y, r)] โดย N คือจำนวนวงกลมที่ตรวจพบ

		# วาดวงกลมรอบๆ วงกลมที่ตรวจพบ (3)
		coins = 0
		if circles is not None:
			# ต้องแปลงค่าพิกัดและรัศมีของวงกลมให้เป็นจำนวนเต็ม
			circles = np.uint16(np.around(circles))
		    for (x, y, r) in circles[0, :]: #[0, :] = [N, (x, y, r)]
			   image_src = cv2.circle(image_src, (x, y), r, (0, 255, 0), 2) # วาดวงกลม
			   coins += 1 # นับจำนวนวงกลมที่ตรวจพบ

		
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
		image_output = cv2.cvtColor(image_src, cv2.COLOR_BGR2GRAY)

		# โหลด pre-trained เพื่อเตรียม cascade (2)
		# ใช้ pre-trained cascade ที่ OpenCV มีมาให้
		cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
		# ตัวอย่าง custom cascade
		
		# ตรวจจับใบหน้า (3)
		faces = cascade.detectMultiScale(
			image_output, # input image
			scaleFactor=1.1, # อัตราส่วนการปรับขนาดภาพ ต้องมีค่ามากกว่า 1
			minNeighbors=5 
		)
		# faces ได้เป็น numpy array ที่เก็บข้อมูลของวัตถุที่ตรวจพบ
		#[x, y, w, h] เรียกว่า bounding box

		# วาดกรอบรอบๆ วัตถุที่ตรวจพบ (4)
		for (x, y, w, h) in faces:
			image_src = cv2.rectangle(image_src, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
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