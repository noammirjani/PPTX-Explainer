"""
                      Service.py
                ------------------
   This file is the service file for the db in the project.

"""

import os
import uuid
from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session

import db.Models as db_models

engine = db_models.get_engine()


def add_upload(upload_uid, email, file):
    """ Add a new upload to the database
    :param upload_uid: the upload uid
    :param email: the user email
    :param file: the file name
    :return: None
    """
    with Session(engine) as session:
        upload = db_models.Upload(uid=upload_uid, filename=file, upload_time=datetime.now(), status='pending')
        if email:
            user = session.query(db_models.User).filter_by(email=email).first()
            if not user:
                user = db_models.User(email=email)
                session.add(user)
                session.commit()
            upload.user_id = user.id

        session.add(upload)
        session.commit()


def find_upload_by_uid(upload_uid):
    """ Get an upload by its uid
    :param upload_uid: the upload uid
    :return: the upload
    """
    with Session(engine) as session:
        uuid_obj = uuid.UUID(upload_uid)
        return session.query(db_models.Upload).filter_by(uid=uuid_obj).first()


def find_upload_by_email_and_file(email, file):
    """ Get an upload by its uid
    :param: email
    :param: file
    :return: the upload
    """
    with Session(engine) as session:
        return session.query(db_models.Upload).join(db_models.User).filter(db_models.User.email == email, db_models.Upload.filename == file)\
            .order_by(desc(db_models.Upload.upload_time)).first()


def find_upload(uid, email, filename):
    if uid:
        upload = find_upload_by_uid(uid)
    elif email and filename:
        upload = find_upload_by_email_and_file(email, filename)
    else:
        raise KeyError('Not enough parameters')

    if not upload:
        raise FileNotFoundError('No such file')

    return upload


def find_pending():
    """ Find all pending uploads
    :return: a list of pending uploads
    """
    with Session(engine) as session:
        return session.query(db_models.Upload).filter_by(status='pending').all()


def update_status(upload_uid, status):
    """ Update the status of an upload
    :param upload_uid: the uid of the upload
    :param status: the new status
    :return: None
    """
    with Session(engine) as session:
        upload = session.query(db_models.Upload).filter_by(uid=upload_uid).first()
        if upload is not None:
            upload.status = status
            session.commit()
