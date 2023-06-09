import requests

from api.Status import Status

url = "http://127.0.0.1:5000/"


def upload(file_path: str):
    """ Uploads a file to the server
    :param file_path: the file path
    :return: the file id
    """
    try:
        with open(file_path, 'rb') as file:
            response = requests.post(url + 'file-upload', files={'upload_file': file})
            if response.status_code == 200:
                return response.json()['uid']
            else:
                raise Exception(f"File upload failed. Status code: {response.status_code}")
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except IOError:
        raise IOError(f"Error occurred while reading the file: {file_path}")


def status(uid: str):
    """ Gets the status of a file upload
    :param uid: the file id
    :return: the file status
    """
    response = requests.get(url + 'file-status/' + uid)
    if response.status_code == 404:
        raise Exception(f"uid not found: {uid}")
    else:
        response.raise_for_status()
    stt = Status(**response.json())
    return stt


def main():
    while True:
        try:
            c = input("Enter command: ").strip()
            if c == "exit":
                break
            elif c == "u":
                file = input("Enter file path: ")
                print(upload(file))
            elif c == "s":
                uid = input("Enter uid: ")
                print(status(uid))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
