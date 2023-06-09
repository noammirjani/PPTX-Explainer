import os
import uuid
import time
import json
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from api.Status import Status

app = Flask(__name__)

# Set the upload and output folder
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(parent_dir, 'uploads')
OUTPUT_FOLDER = os.path.join(parent_dir, 'outputs')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


NAME = 0
TS = 1  # timestamp
UID = 2


def generate_file_name(file):
    """ Generate a new file name
    :param file: the file to generate a name for
    :return: a tuple containing the uid and the new filename
    """
    uid = str(uuid.uuid4())
    timestamp = str(int(time.time()))
    filename = secure_filename(file.filename)
    file_ext = os.path.splitext(filename)[1]
    new_filename = f"{filename}_{timestamp}_{uid}{file_ext}"
    return uid, new_filename


def get_file_content(file):
    with open(os.path.join(OUTPUT_FOLDER, file), 'r') as f:
        return json.load(f)


@app.route('/file-upload', methods=['POST'])
def upload_file():
    """ Create a new user with file upload
    :return: the new user id
    """
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if 'upload_file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    file = request.files['upload_file']
    if file.filename == '':
        return jsonify({'message': 'No file selected for uploading'}), 400

    if not os.path.isfile(file.filename):
        raise FileNotFoundError('Invalid file')

    uid, filename = generate_file_name(file)
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(upload_path)

    return jsonify({'uid': uid}), 200


@app.route('/file-status/<uid>', methods=['GET'])
def get_file_status(uid: str):
    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)

    if not os.path.exists(UPLOAD_FOLDER):
        return jsonify({'message': 'Upload directory is not found'}), 400

    # check if file exists in uploads/output folder, if so return the fit status
    for folder in [OUTPUT_FOLDER, UPLOAD_FOLDER]:
        for file in os.listdir(folder):
            if os.path.isfile(os.path.join(folder, file)):
                file_data = file.split('_')
                if uid == file_data[UID].split('.')[0]:
                    status = 'done' if folder == OUTPUT_FOLDER else 'processing'
                    explanation = get_file_content(file) if folder == OUTPUT_FOLDER else None
                    return jsonify(Status(status, file_data[NAME], file_data[TS], explanation).__dict__), 200

    return jsonify(Status('not found')), 404


if __name__ == '__main__':
    app.run()
