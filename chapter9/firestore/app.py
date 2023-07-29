import tempfile

from flask import Flask, request, render_template, redirect, url_for, send_file
from google.cloud import storage, firestore

BUCKET_NAME = "04092023-target"

storage_client = storage.Client()
firestore_client = firestore.Client()
app = Flask(__name__)


@app.route('/')
def index():
    """Display the single page app"""
    images = []
    uploads_ref = firestore_client.collection(u'uploads')
    uploads = uploads_ref.stream()
    for upload in uploads:
        images.append(upload.to_dict())
    return render_template('index.html', images=images)


@app.route('/upload', methods=['POST'])
def upload():
    """Process a file upload"""
    if request.files["image"].filename != '':
        image = request.files["image"]
        # Write image to GCS
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(image.filename)
        blob.upload_from_file(image)
        # Create entry in Firestore
        new_upload_ref = firestore_client.collection(u'uploads').document()
        new_upload_ref.set({
            'filename': image.filename,
            'description': request.form['description']
        })
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
