from flask import Flask, render_template , request , jsonify
import tensorflow as tf
from PIL import Image
import os , io , sys
import numpy as np 
import cv2
import base64

cur_dirname = os.path.split(os.path.realpath(__file__))[0]
proj_root = os.path.split(cur_dirname)[0]
sys.path.append(proj_root)
from utils.DocumentSegmentation import DocSegModel

app = Flask(__name__)

docSegM = DocSegModel(size=512, dataset='pretrained')
@app.route('/docseg' , methods=['POST'])
def mask_image():
    file = request.files['image'].read() ## byte file
    npimg = np.fromstring(file, np.uint8)
    img = cv2.cvtColor(cv2.imdecode(npimg,cv2.IMREAD_COLOR),cv2.COLOR_BGR2RGB)
    if img.shape[0] > 1000:
        img = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 

    _, img = docSegM.predict(img, is_path=False)

    img = Image.fromarray(img.astype("uint8"))
    
    rawBytes = io.BytesIO()
    img.save(rawBytes, "PNG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())
    return jsonify({'status':str(img_base64)})

@app.route('/')
def home():
	return render_template('index.jinja2')
	
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
	app.run(debug = True, port=8080, host='0.0.0.0')
