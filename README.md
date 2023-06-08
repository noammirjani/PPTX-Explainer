# The GPT-Explainer Project

## Sharing is Caring

So now you have a cool script that can explain presentations with the awesome powers of AI. Naturally, you are filled
with an uncontrollable urge to share your new invention with the world. There is one major problem, however - most
people don't know Python...

It would be great to have an open API, accessible anywhere in the world, using any programming language, or even through
a website or an Android app (for non-programmer muggles).

**Let's write a web application!**

Our goal is to have an HTTP server, which handles user requests. A user can send a file, which the server will process
using the code we already have, and return the outputs.

## Table of Contents

- [Design](#design)
    - A high-level description of the structure and workings of the system.
    - Read this to understand the bigger picture.
- [Requirements](#requirements)
    - The technical requirements for the system.
    - Read this to understand what you actually need to do.
- [Keeping an Organized Workflow](#keeping-an-organized-workflow)
    - Tips for a better work process.
- [Bonus Requirements](#bonus-requirements)

## Design

As you might already sense, we are going to turn our script into a full-fledged software system, running 24/7 and
serving multiple users. This is going to introduce a lot of challenges. It will require us to plan a complex
architecture with several independent parts, delivering high performance and convenient user experience, while allowing
for future scaling, adding features, etc.

Sound intimidating, but fear not! we will proceed in small steps :)

### Architecture Overview

Here is the general architecture of our system. The system will have two components:

- Web API - Handles user requests. This is our interface with the world.
- Explainer - the actual brains of the system. Parses and explain files using GPT.

These two will run simultaneously in separate processes, and communicate using shared folders on the filesystem.

In addition, we will implement a simple Python client. This will be a convenient tool for Python developers to
communicate with the Web API.

To be clear, we are going to have **two completely separate sub-systems** (API & Explainer), which will be **started
separately**, and **run independently**. This gives us more control over scaling, availability and load-balancing. See
also the first [question for though](#questions-for-thought) for extra considerations.

### System Dynamics Overview

Here is a description of how a single user might interact with the system, and what would happen behind the scenes. This
is only intended to give you a picture of how everything should work together. Refer to
the [requirements section](#requirements) for specific instructions.

1. The Web API runs continuously, listening for requests.
2. A user sends an HTTP request to upload a file.
3. The API saves the file in a dedicated `uploads` folder.
4. The API generates a unique identifier (UID) for the file, and returns it to the user.
5. The Explainer runs continuously, checking for new files in the `uploads` folder.
6. The Explainer detects the new file and processes it.
7. The Explainer saves the output JSON in a dedicated `outputs` folder.
8. The user makes another request to check the status of their file.
9. The API checks the `uploads` and `outputs` folders for files matching the given UID.
10. If the file was already processed, the API returns the output JSON.
11. If the file was not yet processed, or doesn't exist, the API responds appropriately.

### Questions for Thought

1. Why did we choose a design where users upload a file and then check its status?
    - It requires users to send two separate requests, one for upload and one for status.
    - It also requires us to run the API and Explainer in separate processes.
    - Isn't this bad UX? Isn't this too complex?
    - What would be the simple, straightforward alternative?
    - What is the biggest problem with that alternative?
    - Remember that GPT is slow.
    - Remember also that we might have multiple users sending requests at the same time.
2. Why do we need to generate a UID for each uploaded file?
    - It requires users to store those UIDs somewhere for later status checks.
    - Why not simply identify uploaded/processed files using their filenames?
    - Think about relevant edge-cases where a filename is not unique enough.
    - Could we solve the problem by adding timestamps to files? Why (not)?
    - Remember we might have multiple users...

## Requirements

Enough stories. Let's talk business!

### Web API

Write a Flask web application. Your app should have the following endpoints:

- Upload:
    1. Receives a POST request with an attached file.
    2. Generates a UID for the uploaded file.
    3. Saves the file in the `uploads` folder. The new filename should contain:
        - the original filename
        - a timestamp of the upload
        - the UID
    4. Returns a JSON object with the UID of the upload (`{uid: ...}`)
- Status:
    1. Receives a GET request with a UID as a URL parameter.
    2. Returns a JSON object, with the following details:
        - `status`: status of the upload. There are 3 options:
            - `'done'` - the upload has been processed
            - `'pending'` - the upload has not yet been processed (still no output file)
            - `'not found'` - no upload exists with the given UID
        - `filename` - the original filename (without the UID and timestamp)
        - `timestamp` - the timestamp of the upload
        - `explanation` - the processed output for the upload, if it is done, or `None` if not

A few extra things about the status endpoint:

- If the status of an upload is `not found` (the user gave a non-existing UID), then the HTTP response should have a
  404 (NOT FOUND) status code.
- If there is an output file (the status is `done`), parse its JSON content and put it into the returned object. Don't
  send the output file itself.

> Tips:
>
> - It is worth taking a look at the builtin `datetime`, `uuid`, `pathlib`, `glob` packages.
> - Receiving files with `flask` is super easy. Don't implement it yourselves.
> - Returning JSONs inside HTTP responses is also super easy with `flask`. In fact, there's a function for that.

### Explainer

Upgrade your GPT explainer script into a GPT explainer system that processes files dropped into a directory.

- The Explainer should run indefinitely after being started.
- The Explainer should sleep for a few seconds between iterations (say, 10 seconds).
- Each iteration, the Explainer should:
    1. Scan the `uploads` folder, and identify the files that still haven't been processed.
    2. For every such file:
        1. Make a debugging print.
        2. Process it using the code you already have (pptx parsing and GPT querying).
        3. Save the explanation JSON in the `outputs` folder.
        4. Make another debugging print.

Some extra considerations:

- The Explainer and Web API should obviously use exactly the same `outputs` and `uploads` folders for the entire system
  to work. This should work regardless of how you run each of them (and from which working directory).
- What information should be printed by the Explainer before and after it processes a file? What is relevant? What is
  redundant? Give it a thought.
- How can you make sure the Explainer only processes new files? How can they be identified? How do you prevent a
  situation where the Explainer processes old uploads again and again? Be creative.

### Python Client

Implement a small Python client for Python developers who want to conveniently send requests to your system. The client
should have these methods:

- Upload:
    1. Receives a path of a file.
    2. Sends the appropriate HTTP request to the web app, with the file attached.
    3. Returns the UID (not the entire JSON, just the UID) from the response, if it was successful.
    4. Raises an exception if the response contains an error code.
- Status:
    1. Receives a UID.
    2. Sends the appropriate HTTP request to the web app, with the UID as a parameter.
    3. If the response is successful, parses the returned JSON into a `Status` object, and returns it.
    4. If the response contains an error (for example if the UID is not found), raises an exception.

The `Status` class should contain:

- Properties:
    - `status` - the status as returned from the Web API
    - `filename` - the original filename as returned from the Web API
    - `timestamp` - a parsed `datetime` object of the upload timestamp
    - `explanation` - the output as returned from the Web API
- Methods:
    - `is_done` - returns `True` if the `status` is `'done'`, or `False` otherwise.
    - Other methods you might find useful.

> Questions for thought:
>
> - Notice that the APIs of the Python client and the web app are not exactly the same. Why is that?
> - Why not have the status method simply return the JSON as is? Why parse it into an object?
> - Why is it convenient to have an `is_done` method? What is the first thing someone will want to do with this object
    after receiving it?

> Tips:
>
> - You might want to install the `requests` package. It's awesome!
> - You might also want to use the builtin `dataclasses` package...
> - Sending files with `requests` is super easy. Don't implement it yourself.

### System Test

Create a system test that performs an end-to-end run-through of the system:

1. Starts the Web API.
2. Starts the Explainer.
3. Uses the Python Client to upload a sample presentation.
4. Uses the Python Client to check the status of that presentation.

This can be useful for easily and consistently checking that everything works.

## Keeping an Organized Workflow

Your project now will essentially become 3 standalone projects, each with its own codebase. At the same time, these
components are going to talk to each other. This introduces quite a lot of complexity. Here are a few tips to avoid
drowning in an uncontrollable mess:

- Write the code for each component in its own folder.
- Don't make imports across components. They should function as totally separate systems.
- Define clear interfaces between components (API URLs, parameter formats, shared folder paths, filename formats, etc.)
  and stick to them. These interfaces are where the components depend on each other, so changing them requires
  modifications in multiple places. Do so carefully, if you must.
- Create a Git branch for each component, and work on them separately. Merge to `main` when you need to test multiple
  components together.
- Make a list of small tasks, and organize them by component. This will help you avoid jumping all over the place.
- Organize your tasks by importance and urgency.
- If something pops up in the middle of developing a feature (you suddenly realize you have a bug in another component),
  take a deep breath, write it down and finish what you're doing first.
- Think while you code. Always remind yourself of the bigger picture of how everything fits together. Keep yourself
  oriented.

## Bonus Requirements

### Logs

Make your system write helpful logs into files. This includes:

- The Explainer logs/prints
- The automatic logs of the Flask server

The logs should be saved according to these specifications:

- The Explainer and the Flask server should write to separate log files.
- All the log files should sit in a dedicated folder, and each component should have its own sub-folder. Keep it
  organized!
- A new log file should be created every day, and you should keep log files from the last 5 days.

> Tips:
>
> - Use [time rotating file handlers](https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler).
> - You can simply access the default Flask logger and add a handler to it.

Think carefully which details are relevant for logging in each component. Remember: logs should be easy to search and
easy to understand.

### Python Package

The Python Client you will implement is essentially intended for use by other developers (just like you are using
the `openai` package to talk to their API). Therefore, we would like to turn it into a package, which can be uploaded
to [PyPI](https://pypi.org/) and installed on other computers. For now, we won't actually upload to PyPI (unless you
want to try it yourself), but it can also be convenient for you to install it locally, so you can import it without
needing to start Python from the directory of the project.

To turn your code into a package, it needs to have a certain directory structure, and a special file
called `pyproject.toml`, which contains specifications like the package name, version and dependencies on other
packages, as well as directions for the build process of the package. You can read
more [here](https://setuptools.pypa.io/en/latest/userguide/quickstart.html#basic-use). Focus on
the [Basic Use](https://setuptools.pypa.io/en/latest/userguide/quickstart.html#basic-use) section. The rest is not very
relevant right now.

After you got that right, try installing your package locally in "editable" mode. This means when you import your
package, the import mechanism looks directly at your project files, so you don't have to reinstall every time you make
changes. To achieve this, simply go to the directory where your `pyproject.toml` sits, and
execute `pip install --editable .` inside it. Then try opening Python and importing your package.

### Better Tests

Separate your system test into smaller tests, using `pytest` with `assert` statements. Use `fixture`s for running the
web API and the Explainer. `assert` stuff like the following:

- The upload method returns a UID.
- The upload creates a file in the `uploads` folder, with the timestamp and UID in the filename.
- The Explainer only processes new files.
- The client raises errors when a UID is not found.
- The status method returns a `pending` status for a file if you try right after uploading it.
- More useful tests you can think of...

![Good Luck](https://i.pinimg.com/originals/33/52/87/33528736e35debe64cffaf15d1696445.jpg)
