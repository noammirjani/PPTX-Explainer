# The GPT-Explainer Project

## Going Pro

As our system grows, we will begin to handle a lot more data...

So far we have used filenames and folders to track our data. This requires disgusting code to play with the filesystem.
It is also less performant on large scales, and requires manual implementation to perform advanced queries, like finding
the latest pending upload.

It's time to start managing our data like pros. It's time to use a database!

## Requirements

### DB

Add an [SQLite](https://www.sqlitetutorial.net/what-is-sqlite/) database to your system. The physical DB file should sit
inside a dedicated `db` folder.

The DB will have 2 tables:

- Users - people who upload files for explanation.
- Uploads - files uploaded by people, with metadata related to their processing.

> Important: Make sure your code always accesses the same DB file, no matter how or from where you run the code.

### ORM

Define an ORM for your DB, using the `SQLAlchemy` package. You should have the following classes:

**User**:

- Mapped Columns:
    - id: `int` (primary key)
    - email: `str` - the email address of the user
- Relationships:
    - uploads: `List[Upload]` - list of uploads this user made

**Upload**:

- Mapped Columns:
    - id: `int` (primary key)
    - uid: `UUID` - the UID that was generated for the upload
    - filename: `str` - original uploaded filename
    - upload_time: `datetime` - when the Web API received the upload
    - finish_time: `datetime` - when the Explainer finished processing the upload
    - status: `str` - the current status of the upload
    - user_id: `int` - foreign key (primary key of the user who uploaded this upload)
- Relationships:
    - user: `User` - the user who uploaded this upload

You may define additional columns if you wish (but before you do, ask yourself why you want to).

> Tips:
> - Here's a useful [quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html) for how to work with SQLAlchemy.
    It covers all the basics.
> - SQLAlchemy is very complex, and its documentation is full of advanced and confusing terminology. It is very easy to
    lose yourself in there. Focus on the code examples, and try to understand the main points.

**Additional requirements**:

- Use the new SQLAlchemy syntax for defining columns, using the `mapped_column` function. Also add Python type
  annotations, using the `Mapped` class.
- Columns should use [data types](https://docs.sqlalchemy.org/en/20/core/type_basics.html) that work for every DB, even
  if the DB doesn't support types that exist in Python. Notice there are two categories of column types in SQLAlchemy.
  Which one should you use?
- Make sure you add proper [data constraints](https://www.w3schools.com/sql/sql_constraints.asp) for the different
  columns in the ORM. It is very easy [in SQLAlchemy](https://docs.sqlalchemy.org/en/20/core/constraints.html). For
  example, a user's `email` should be unique, and also not nullable. What about other columns?
- If a user is deleted, all their uploads should also be deleted. You can make this happen automatically by defining
  [cascades](https://docs.sqlalchemy.org/en/20/orm/cascades.html).
- Previously we could only distinguish two upload statuses: `pending` and `done`. Now add a few more options, so we can
  have a better sense of what exactly happens to each upload at any moment. What do you think should be useful?
- Add some additional methods to the `Upload` class. For example, an `upload_path` method could compute the path of the
  uploaded file based on the metadata in the DB. Can you think of other useful ideas?
- Add a way to see error messages for failed uploads easily and without searching the logs for hours. What is the
  easiest way to do that?
- Make sure uploads receive a `finish_time` under the right circumstances. What are those?
- Don't put your own values into the primary key columns. Let them automatically increment.

### Changing the Web API

Modify the Web API component so that it uses the data in the DB.

**Upload**:

The upload endpoint should now:

- Allow an optional `email` POST parameter.
- Create an `Upload` object and commit it to the DB.
- If an email was given:
    - Fetch that user from the DB, or create a new one if it doesn't exist.
    - Associate the user with the new upload.
- If no email was given, simply leave the upload without a user. It will be an anonymous upload.
- Save files with only the UID in the filename (without the other details).

Questions for thought:

- Why do we want to allow people to upload files without sending their email?
- How is the user experience different when uploading files associated with an email vs. when uploading anonymously?
- What does an anonymous upload look like in the DB?

**Status**:

The status endpoint should now:

- Receive either a UID or a filename and an email.
- If a UID was given, fetch that upload from the DB.
- If a filename and an email were given, fetch the **latest** upload with that filename of the user with that email.
- Add the UID, status and finish time (and maybe other data?) to the response JSON.

Please note that now all the details should be read from the DB. Only the actual GPT explanation should be read from
the filesystem.

### Changing the Explainer

The Explainer should now:

- Find pending uploads in the DB instead of scanning directories.
- Get all metadata about uploads and outputs from the DB.
- Save output files with only the UID in the filename (+ ".json" of course).
- Update upload statuses in the DB every time something noteworthy happens.
- Update upload finish times.

### Changing the Python Client

The Python Client should now:

- Allow uploading files with an optional email attached.
- Allow checking status by email and filename.
- Anything else? You can figure it out!

### General Tips

- Don't forget to `commit` your changes to the DB.
- Don't forget to close every [session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html) you create.
- Don't forget to `add` changes to the session before you `commit`.
- It is very convenient to create a module that automatically connects to the DB when you `import` it, and creates
  an [engine](https://docs.sqlalchemy.org/en/20/core/engines.html) that you can `import` and use to execute queries.
- It is very convenient to write a small DB initialization script, that creates the DB and the tables. You will
  probably (mess up and) want to create a new clean DB several times during development.
- It is very convenient to look at the data in your DB with your own eyes to check if everything's right. If you're
  using PyCharm Professional you can use the Database Tool Window (notice if it says you need to download a driver). If
  you're using VSCode you can install an SQLite extensions (there are a few). You can also download third-party software
  like [SQLite Browser](https://sqlitebrowser.org/). All options allow you to open a DB file and execute SQL queries.

And also: when refactoring code, delete everything you don't use anymore! Clean code == clean soul.

## Bonus Requirements

### Properties

Make the extra methods you added to the `Upload` class look and behave like regular properties.
Read about the `@property` decorator.

### Email Validation

You don't just trust people who give you string and claim they are emails. What if it's not? Or maybe the format is
right, but the email doesn't really exist. Or it's a temporary disposable email...

Make the Upload endpoint of the Web API validate the user emails it receives.

You might want to use [this](https://pypi.org/project/email-validate/) package. If you don't like it, there are others.
Search [PyPI](https://pypi.org/).

### Upload Summary

Add a new `history` endpoint to the Web API. It should:

- Receive a GET request with an email as a URL parameter.
- Return a JSON summary of past uploads for that user.

The returned JSON should be a list, where every element is an object with brief metadata about an upload. The metadata
for each upload should contain the UID, filename, upload time, status and other things you find relevant.

Needless to say, you should handle bad inputs...

And of course, add a method to the Python Client to access this API endpoint.

![Good Luck](https://i.imgflip.com/1pz4wb.jpg)