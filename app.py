from flask import Flask, request, render_template, redirect, url_for
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return redirect(request.url)
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        color = get_image_color(filepath)
        return render_template('result.html', color=color)
    return redirect(request.url)

def get_image_color(image_path):
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        colors = img.getcolors(img.size[0] * img.size[1])
        dominant_color = colors[0][1]
        return dominant_color

if __name__ == '__main__':
    app.run(debug=True)
