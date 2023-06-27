"""
                       App.py
             ------------------------
    The logic of the program - explainer of presentations.

    REQUIREMENTS:
   1. pip install python-pptx
   2. pip install openai
   3. pip install backoff

--> change to your API_KEY in apiAnalyzer.py.
"""

from PptxScanner import PptxScanner
from ApiAnalyzer import ApiAnalyzer
from constants import OUTPUT_FOLDER, UPLOAD_FOLDER
import db.Service as db_service
import asyncio
import os


# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# UPLOADS_DIR = os.path.join(CURRENT_DIR, '..', 'uploads')
# OUTPUTS_DIR = os.path.join(CURRENT_DIR, '..', 'outputs')


def create_tasks(presentation: list) -> list:
    """ Create tasks for each slide
    :param presentation: list of slide content
    :return: list of tasks
    """
    tasks = []
    api_analyzer = ApiAnalyzer()
    for index, slide_content in enumerate(presentation):
        task = asyncio.create_task(api_analyzer.analyze(slide_content, index))
        tasks.append(task)
    return tasks


def extract_to_file(responses, file_uid: str):
    """ Extract the responses to a file in JSON format
    :param file_uid:
    :param responses: list of responses
     """
    import json

    file_name = OUTPUT_FOLDER + '/' + file_uid + ".json"
    with open(file_name, "w") as outfile:
        json_responses = {}
        for response in responses:
            slide_id = f"slide {response['slide_id']}"
            analyze = response["analyze"]
            json_responses[slide_id] = analyze
        json.dump(json_responses, outfile, indent=4)


async def explain_presentation(file):
    """ Run the program
    :param file:
    """
    file_path = UPLOAD_FOLDER + '/' + str(file.uid) + '.pptx'
    presentation_content = PptxScanner(file_path).scan_presentation()
    tasks = create_tasks(presentation_content)
    prs_summary = await asyncio.gather(*tasks)
    extract_to_file(prs_summary, str(file.uid))
    db_service.update_status(file.uid, 'done')
    print(f"presentation {file_path} was processed successfully")


def main():
    try:
        if not os.path.exists(OUTPUT_FOLDER):
            os.mkdir(OUTPUT_FOLDER)
        if not os.path.exists(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)

        print("explainer is running...")
        while True:
            pending = db_service.find_pending()
            for file in pending:
                print(f"processing presentation: {file}")
                asyncio.run(explain_presentation(file))

    except Exception as err:
        print("Some error accrued: ", str(err))

    finally:
        print("explainer stopped!")


if __name__ == "__main__":
    main()
