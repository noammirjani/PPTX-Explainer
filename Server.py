import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/file-upload', methods=['POST'])
def create_user():
    """ Create a new user with file upload
    :return: the new user id
    """
    if 'upload_file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400
    file = request.files['upload_file']

    if file.filename == '':
        return jsonify({'message': 'No file selected for uploading'}), 400
    # create the file name and id
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
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = secure_filename(file.filename)
    file_ext = os.path.splitext(filename)[1]
    new_filename = f"{filename}_{timestamp}_{uid}{file_ext}"
    return uid, new_filename


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run()
