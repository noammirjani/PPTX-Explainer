import os
import uuid

import db.Service as db_service
from flask import Flask, request, jsonify
from api.Status import Status
from constants import UPLOAD_FOLDER, OUTPUT_FOLDER


app = Flask(__name__)

# Set the upload and output folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER


def generate_file_name(uid, filename):
    """ Generate a new file name
    :param uid: the uid of the file
    :param filename: the file to generate a name for
    :return: the new file name with the path of the file
    """
    file_ext = os.path.splitext(filename)[1]
    new_filename = f"{uid}{file_ext}"
    return os.path.join(app.config['UPLOAD_FOLDER'], new_filename)


def check_directories():
    """ Check if the upload and output directories exist, if not create them
    :return: None
    """
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)


def get_param(body, param):
    """ Get a parameter from the request body
    :param body: the request body
    :param param: the parameter to get
    :return: the parameter value
    """
    if param not in body:
        raise KeyError(f'No {param} in the request')
    return body[param]


def get_param_if_exist(body, param):
    """ Get a parameter from the request body
    :param body: the request body
    :param param: the parameter to get
    :return: the parameter value
    """
    if param not in body:
        return None
    return body[param]


def check_file(filename):
    """ Check if the file is valid and exists """
    if filename == '':
        raise FileNotFoundError('No file selected')

    if not os.path.isfile(filename):
        raise FileNotFoundError('Invalid file')


@app.route('/file-upload', methods=['POST'])
def upload_file():
    """ Create a new user with file upload
    :return: the new user id
    """
    try:
        check_directories()
        file = get_param(request.files, 'upload_file')
        email = get_param_if_exist(request.form, 'email')

        check_file(file.filename)
        upload_uid = uuid.uuid4()
        upload_path = generate_file_name(upload_uid, file.filename)
        db_service.add_upload(upload_uid, email, file.filename)
        file.save(upload_path)
        return jsonify({'uid': upload_uid}), 200
    except Exception as e:
        return jsonify({'message': str(e.args[0])}), 400


@app.route('/file-status', methods=['GET'])
def get_file_status():
    check_directories()

    uid = get_param_if_exist(request.args, 'uid')
    email = get_param_if_exist(request.args, 'email')
    filename = get_param_if_exist(request.args, 'filename')

    try:
        upload = db_service.find_upload(uid, email, filename)
        return jsonify(Status.from_upload(upload).__dict__), 200
    except Exception as e:
        return jsonify({'message': str(e.args[0])}), 400


if __name__ == '__main__':
    app.run()
