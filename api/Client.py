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
    response.raise_for_status()
    Status(response.json())


def main():
    """ Gets a file path from the user and sends it to the server """
    print(" ---- Welcome to the file uploader! ----")

    while True:
        try:
            file_path = input("Enter the file path (or 'quit' to exit): ").strip()

            if file_path == 'quit':
                break

            upload(file_path)
            stt_uid = input("Enter the UID to check the status: ").strip()
            status(stt_uid)
        except Exception as e:
            print("An error occurred: ", str(e))


if __name__ == '__main__':
    main()
