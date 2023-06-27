"""
                    Status.py
                    -----------
    This file contains the Status class which is used to
        represent the status of a file upload.
"""


class Status:
    """ The status of a file upload """

    def __init__(self, upload):
        self.uid = upload.uid
        self.filename = upload.filename
        self.upload_time = upload.upload_time
        self.finish_time = upload.finish_time
        self.status = upload.status
        self.user_id = upload.user_id

    def __str__(self):
        return f"uid: {self.uid}\nfilename: {self.filename}\nupload_time: {self.upload_time}\n" \
               f"finish_time: {self.finish_time}\nstatus: {self.status}\nuser_id: {self.user_id}"
