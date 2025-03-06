from flask import Flask, render_template, request, send_file
import os
import cv2
import numpy as np

app = Flask(__name__, template_folder="templates", static_folder="static")
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        return "No file uploaded", 400
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    result_path = os.path.join(RESULT_FOLDER, f"colorized_{file.filename}")
    file.save(filepath)
    
    image = cv2.imread(filepath)
    if image is None:
        return "Invalid image format", 400
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    colorized = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    
    cv2.imwrite(result_path, colorized)
    return send_file(result_path, mimetype='image/jpeg')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)