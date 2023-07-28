import os

from flask import Flask, request, render_template, redirect, url_for

ROOT_DIR = os.path.dirname(__file__)
UPLOAD_DIR = os.path.join(ROOT_DIR, 'static/uploads')
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app = Flask(__name__)


@app.route('/')
def index():
    """Display the single page app"""
    images = [f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(
        os.path.join(UPLOAD_DIR, f))]
    return render_template('index.html', images=images)


@app.route('/upload', methods=['POST'])
def upload():
    """Process a file upload"""
    if request.files["image"].filename != '':
        image = request.files["image"]
        image.save(os.path.join(UPLOAD_DIR, image.filename))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
