"""
    Status.py
    -----------
    This file contains the Status class which is used to
    represent the status of a file upload.
"""


class Status:
    """ The status of a file upload """

    def __init__(self, uid, filename, upload_time, finish_time, status, user_id):
        self.uid = uid
        self.filename = filename
        self.upload_time = upload_time
        self.finish_time = finish_time
        self.status = status
        self.user_id = user_id

    @classmethod
    def from_upload(cls, upload):
        return cls(upload.uid, upload.filename, upload.upload_time, upload.finish_time, upload.status,
                   upload.user_id)

    @classmethod
    def from_dict(cls, upload_dict):
        return cls(upload_dict['uid'], upload_dict['filename'], upload_dict['upload_time'],
                   upload_dict['finish_time'], upload_dict['status'], upload_dict['user_id'])

    def __str__(self):
        return f"uid: {self.uid}\nfilename: {self.filename}\nupload_time: {self.upload_time}\n" \
               f"finish_time: {self.finish_time}\nstatus: {self.status}\nuser_id: {self.user_id}"
