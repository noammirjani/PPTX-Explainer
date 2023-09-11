## PPTX Explainer

A Client-Server system, incorporating SQLAlchemy for upload and user data management, 
leverages the OpenAI API to process uploaded PowerPoint presentations and generate display-ready explanations.

It consists of three main components:

Server (web_api_manager.py): This component is a Flask-based web application that serves as an interface for users to upload their PPTX files. Upon file submission, the application generates a unique identifier (UID) for the file and stores it in the 'uploads' directory. Additionally, it records the upload in a database, associating it with the respective user.
Analyzer (pptx_explainer.py): Operating in the background, this service continuously monitors the database for pending uploads. Once an unprocessed upload is detected, it triggers the analysis procedure. This procedure involves tasks such as extracting textual content from the slides, formulating prompts, and dispatching these prompts to the GPT API for analysis. Subsequently, the responses received from the GPT API are consolidated and archived in the 'outputs' folder.
Client (client.py): To facilitate user interaction with the API, a Python script is provided. This script enables users to easily upload files and inquire about their analysis status.

These three components work together to automate the analysis of PowerPoint presentations and derive insights from them.
