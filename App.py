"""
                       App.py
             ------------------------
             The logic of the program.
    Manage the functionality of the other classes.
"""
from PptxScanner import PptxScanner
import asyncio
from ApiAnalyzer import ApiAnalyzer


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


def extract_to_file(responses, prs_path: str):
    """ Extract the responses to a file in JSON format
    :param responses: list of responses
    :param prs_path: the path of the presentation
     """
    import json

    file_name = prs_path.split('/')[-1].split('.pptx')[0] + ".json"
    with open(file_name, "w") as outfile:
        json_responses = {}
        for response in responses:
            slide_id = f"slide {response['slide_id']}"
            analyze = response["analyze"]
            json_responses[slide_id] = analyze
        json.dump(json_responses, outfile, indent=4)


async def run(file_path: str):
    """ Run the program
    :param file_path: the path of the presentation
    """
    try:
        print("-" * 20, " WELCOME ", "-" * 20)
        presentation_content = PptxScanner(file_path).scan_presentation()
        tasks = create_tasks(presentation_content)
        prs_summary = await asyncio.gather(*tasks)
        extract_to_file(prs_summary, file_path)
    except Exception as err:
        print("some error accrued: ", str(err))
    finally:
        print("-" * 22, " END ", "-" * 22)
