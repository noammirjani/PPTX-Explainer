import requests

from api.Status import Status
from constants import URL, UPLOAD, STATUS


def upload(file_path: str, email: str):
    """ Uploads a file to the server
    :param email: the user email
    :param file_path: the file path
    :return: the file id
    """
    with open(file_path, 'rb') as file:
        file = {'upload_file': file}
        email = {'email': email}
        response = requests.post(URL + UPLOAD, files=file, data=email)
        response.raise_for_status()
        return response.json()['uid']


def status(uid: str):
    """ Gets the status of a file upload
    :param uid: the file id
    :return: the file status
    """
    response = requests.get(URL + STATUS + uid)
    response.raise_for_status()
    return Status(**response.json())


def main():
    while True:
        try:
            c = input("Enter command: ").strip()
            if c == "exit":
                break
            elif c == "u":
                file = input("Enter file path: ")
                email = input("Enter email: (optional - press enter to skip) )")
                print(upload(file, email))
            elif c == "s":
                uid = input("Enter uid: ")
                print(status(uid))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
