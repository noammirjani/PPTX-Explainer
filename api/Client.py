import requests

url = "http://127.0.0.1:5000/"


class Status:
    """ The status of a file upload """

    def __init__(self, data):
        self.status = data['status']
        self.filename = data['filename']
        self.timestamp = data['timestamp']
        self.explanation = data['explanation']


def upload(file_path):
    """ Uploads a file to the server
    :param file_path: the file path
    :return: the file id
    """
    try:
        with open(file_path, 'rb') as file:
            response = requests.post(url + 'file-upload', files={'upload_file': file})
            if response.status_code == 200:
                print(response.json())
                return response.json()['uid']
            else:
                raise Exception(f"File upload failed. Status code: {response.status_code}")
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except IOError:
        raise IOError(f"Error occurred while reading the file: {file_path}")


def status(uid):
    """ Gets the status of a file upload
    :param uid: the file id
    :return: the file status
    """
    response = requests.get(url + 'file-status/' + uid)
    if response.status_code == 404:
        raise Exception(f"uid not found: {uid}")
    else:
        response.raise_for_status()
    return Status(response.json())


def main():
    while True:
        file = input("Enter file path: ")
        uid = upload(file)
        status(uid)
        print(status(uid).status)


if __name__ == '__main__':
    pass
