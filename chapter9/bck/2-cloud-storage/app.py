import tempfile

from flask import Flask, request, render_template, redirect, url_for, send_file
from google.cloud import storage

BUCKET_NAME = "<YOUR-BUCKET-NAME>"

storage_client = storage.Client()
app = Flask(__name__)


@app.route('/')
def index():
    """Display the single page app"""
    images = [f.name for f in storage_client.list_blobs(BUCKET_NAME)]
    return render_template('index.html', images=images)


@app.route('/upload', methods=['POST'])
def upload():
    """Process a file upload"""
    if request.files["image"].filename != '':
        image = request.files["image"]
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(image.filename)
        blob.upload_from_file(image)
    return redirect(url_for('index'))


@app.route('/display/<imagename>')
def display(imagename):
    """Display an image from the bucket"""
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(imagename)
    with tempfile.NamedTemporaryFile() as temp:
        blob.download_to_filename(temp.name)
        return send_file(temp.name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
