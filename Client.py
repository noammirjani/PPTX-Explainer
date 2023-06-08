import requests


def main():
    """ Gets a file path from the user and sends it to the server """
    print(" ---- Welcome to the file uploader! ----")

    while True:
        file_path = input("Enter the file path (or 'quit' to exit): ")

        if file_path == 'quit':
            break

        try:
            with open(file_path, 'rb') as file:
                response = requests.post('http://127.0.0.1:5000/file-upload', files={'upload_file': file})
                if response.status_code == 200:
                    print(response.json())
                else:
                    print("File upload failed. Status code:", response.status_code)
        except FileNotFoundError:
            print("File not found. Please enter a valid file path.")
        except IOError as e:
            print("Error occurred while reading the file:", str(e))


if __name__ == '__main__':
    main()
