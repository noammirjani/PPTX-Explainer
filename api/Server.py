
import os
import uuid
import json
from flask import Flask, request, jsonify
from api.Status import Status
from constants import UPLOAD_FOLDER, OUTPUT_FOLDER, UPLOAD

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


def get_file_content(file):
    with open(os.path.join(OUTPUT_FOLDER, file), 'r') as f:
        return json.load(f)


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


def check_file(filename):
    """ Check if the file is valid and exists """
    if filename == '':
        raise FileNotFoundError('No file selected')

    if not os.path.isfile(filename):
        raise FileNotFoundError('Invalid file')


@app.route(UPLOAD, methods=['POST'])
def upload_file():
    """ Create a new user with file upload
    :return: the new user id
    """
    try:
        check_directories()
        file = get_param(request.files, 'upload_file').filename
        email = get_param(request.form, 'email')

        check_file(file)
        upload_uid = uuid.uuid4()
        upload_path = generate_file_name(upload_uid, file)
        # db_service.add_update_user(upload_uid, email, file)
        file.save(upload_path)
        return jsonify({'uid': upload_uid}), 200
    except Exception as e:
        return jsonify({'message': str(e.args[0])}), 400


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
                if uid == file_data["uid"].split('.')[0]:
                    status = 'done' if folder == OUTPUT_FOLDER else 'processing'
                    explanation = get_file_content(file) if folder == OUTPUT_FOLDER else None
                    return jsonify(Status(status, file_data["name"], file_data["ts"], explanation).__dict__), 200

    return jsonify(Status("not found").__dict__), 404


if __name__ == '__main__':
    app.run()
