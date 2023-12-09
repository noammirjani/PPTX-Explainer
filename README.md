# GPT-Explainer Project

## Table of Contents

- [GPT-Explainer Project](#gpt-explainer-project)
  - [Overview](#overview)
  - [Features](#features)
    - [Web Application Interface](#web-application-interface)
    - [Database Integration](#database-integration)
  - [Usage](#usage)
    - [Web Application Interface](#web-application-interface-1)
    - [Database Integration](#database-integration-1)
  - [Installation](#installation)
  - [Running the Project](#running-the-project)
  - [Contributions](#contributions)
  - [Project Origin](#Project-Origin)
  - [License](#license)

## Overview

The GPT-Explainer project is a powerful tool built to enhance the understanding of PowerPoint presentations using AI. This Python-based solution leverages the GPT-3.5 model from OpenAI to explain presentations by analyzing the text content in each slide and generating detailed explanations. The project is divided into three main components:

1. **Web Application Interface**: Provides an HTTP server that handles user requests, processes uploaded files using the explanation script, and returns outputs.
2. **Database Integration**: Implements SQLite database for efficient data management, storing user information, upload history, and processing statuses.

## Features

### Web Application Interface

- **Endpoints**:
  - `Upload`: Accepts file uploads, assigns a UID, and initiates processing.
  - `Status`: Checks the processing status of uploaded files.

### Database Integration

- **Tables**:
  - `Users`: Stores user information (email).
  - `Uploads`: Tracks file uploads, their status, and timestamps.

## Usage

### Web Application Interface

1. Start the HTTP server.
2. Interact with endpoints:
   - `/upload`: POST files for processing.
   - `/status`: GET status of uploads.

### Database Integration

1. Ensure SQLite and SQLAlchemy setup.
2. Utilize ORM classes (`User`, `Upload`) for managing user data and uploads.

## Installation

1. Clone the repository.
2. Install required Python packages (`requirements.txt`).
```bash
pip install -r requirements.txt
```
3. Set up SQLite database (`db` folder).
4. Configure the OpenAI API key:
    - Update the variable `API_KEY = os.getenv("OPENAI_API_KEY")` in `./explainer/ApiAnalyzer.py` with the relevant API key.
    - Alternatively, update the environment variable `OPENAI_API_KEY` with the relevant key.
5. Run the application components individually or together.

## Running the Project

To run the project, execute the following commands:
- Start the server: `python api/Server.py`
- Run the client: `python api/Client.py`

## Contributions

Contributions, issues, and feature requests are welcome! Please follow the guidelines in `CONTRIBUTING.md`.


## Project Origin

This project was developed as the final project for the Advanced Python course at HAC. It represents the culmination of skills and knowledge gained during the course, showcasing an application that leverages Python's capabilities in various domains, including AI, web development, and database management.
- [Noam Mirjani](noamirjani@gmail.com)


## License

This project is licensed under the [License Name](LICENSE).
