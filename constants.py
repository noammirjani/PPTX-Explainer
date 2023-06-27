"""
                    constants.py
                ------------------
This file contains all the constants used in the project.
"""
import os

URL = "http://127.0.0.1:5000"
UPLOAD = "/file-upload"
STATUS = "/file-status"


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(parent_dir, 'uploads')
OUTPUT_FOLDER = os.path.join(parent_dir, 'outputs')