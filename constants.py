"""
                    constants.py
                ------------------
This file contains all the constants used in the project.
"""
import os

URL = "http://127.0.0.1:5000"
UPLOAD = "/file-upload"
STATUS = "/file-status"


parent_dir = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(parent_dir, 'uploads')
OUTPUT_FOLDER = os.path.join(parent_dir, 'outputs')
DB_FOLDER = os.path.join(parent_dir, 'db')
DB_PATH = os.path.join(DB_FOLDER, 'db.sqlite3.db')


API_KEY = "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"
