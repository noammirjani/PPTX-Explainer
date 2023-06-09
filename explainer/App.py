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
import asyncio
import os
import time

UPLOADS_DIR = '../uploads'
OUTPUTS_DIR = '../outputs'


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


def extract_to_file(responses, file_name: str):
    """ Extract the responses to a file in JSON format
    :param responses: list of responses
    :param file_name: the path of the presentation
     """
    import json

    name = file_name.split('/')[-1].rsplit('.pptx', 1)[0]
    file_name = OUTPUTS_DIR + '/' + name + ".json"
    with open(file_name, "w") as outfile:
        json_responses = {}
        for response in responses:
            slide_id = f"slide {response['slide_id']}"
            analyze = response["analyze"]
            json_responses[slide_id] = analyze
        json.dump(json_responses, outfile, indent=4)


async def explain_presentation(file_path: str):
    """ Run the program
    :param file_path: the path of the presentation
    """
    print(f"processing presentation: {file_path}")
    presentation_content = PptxScanner(file_path).scan_presentation()
    tasks = create_tasks(presentation_content)
    prs_summary = await asyncio.gather(*tasks)
    extract_to_file(prs_summary, file_path)
    print(f"presentation {file_path} was processed successfully")


def main():
    try:
        if not os.path.exists(UPLOADS_DIR):
            raise Exception("Explainer has no access to the uploads directory")
        if not os.path.exists(OUTPUTS_DIR):
            os.mkdir(OUTPUTS_DIR)
        last_check_timestamp = int(time.time())

        print("explainer is running...")
        while True:
            for file in os.listdir(UPLOADS_DIR):
                file_timestamp = int(file.split('_')[1])
                if file_timestamp > last_check_timestamp:
                    asyncio.run(explain_presentation(f"{UPLOADS_DIR}/{file}"))
                    last_check_timestamp = file_timestamp

    except Exception as err:
        print("Some error accrued: ", str(err))


if __name__ == "__main__":
    main()
