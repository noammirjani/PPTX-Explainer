"""
                    Status.py
                    -----------
    This file contains the Status class which is used to
        represent the status of a file upload.
"""


class Status:
    """ The status of a file upload """

    def __init__(self, status: str, filename=None, timestamp=None, explanation=None):
        self.status = status
        self.filename = filename
        self.timestamp = timestamp
        self.explanation = explanation

    def __str__(self):
        return f"Status: {self.status}\n" \
               f"Filename: {self.filename}\n" \
               f"Timestamp: {self.timestamp}\n" \
               f"Explanation: {self.explanation}\n"
