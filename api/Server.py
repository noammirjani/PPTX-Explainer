import os
import uuid
import time
import json
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


@app.route('/file-upload', methods=['POST'])
def create_user():
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

    uid, filename = generate_file_name(file)
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(upload_path)

    return jsonify({'message': 'File saved', 'uid': uid}), 200


def generate_file_name(file) -> (str, str):
    """ Generate a new file name
    :param file: the file to upload
    :return: the new file name and id
    """
    uid = str(uuid.uuid4())
    timestamp = str(int(time.time()))
    filename = secure_filename(file.filename)
    file_ext = os.path.splitext(filename)[1]
    new_filename = f"{filename}_{timestamp}_{uid}{file_ext}"
    return uid, new_filename


def content(file) -> str:
    """ Get the content of a file
    :param file: the file to read
    :return: the content of the file
    """
    with open(os.path.join(OUTPUT_FOLDER, file), 'r') as f_name:
        return json.load(f_name)


@app.route('/file-status/<uid>', methods=['GET'])
def get_file_status(uid):
    """ Get the status of a file upload
    :param uid: the file id
    :return: the file status
    """
    if not os.path.exists(OUTPUT_FOLDER):
        return jsonify({'message': 'Output directory is not found'}), 400

    for folder in [OUTPUT_FOLDER, UPLOAD_FOLDER]:
        for file in os.listdir(folder):
            file_data = file.split('_')
            if uid == file_data[2].split('.')[0]:
                # File is found in the folder
                if folder == OUTPUT_FOLDER:
                    return jsonify({'status': 'done',
                                    'filename': file_data[0],
                                    'timestamp': file_data[1],
                                    'explanation': content(file)}), 200
                else:  # file is in the upload folder
                    return jsonify({'status': 'processing',
                                    'filename': file_data[0],
                                    'timestamp': file_data[1],
                                    'explanation': None}), 200

    return jsonify({'status': 'uid not found', 'filename': None, 'timestamp': None, 'explanation': None}), 400


if __name__ == '__main__':
    app.run()
