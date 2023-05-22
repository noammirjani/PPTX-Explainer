"""
            App.py
    ------------------------
   The main file of the project,
   manage the flow of the program.

   TO RUN THE PROGRAM:
   1. pip install python-pptx
   2. pip install openai
   3. pip install backoff

--> notice that the program includes  API_KEY, which is a (my) private key,
    you can change it in apiAnalyzer.
    The program includes 2 out 3 of the bonus requirements.
"""
from PptxScanner import PptxScanner
import asyncio
from ApiAnalyzer import ApiAnalyzer


def create_tasks(presentation):
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


def extract_to_file(responses, prs_path):
    """ Extract the responses to a file in JSON format """
    import json

    file_name = prs_path.split('/')[-1].split('.pptx')[0] + ".json"
    with open(file_name, "w") as outfile:
        json_responses = {}
        for response in responses:
            slide_id = f"slide {response['slide_id']}"
            analyze = response["analyze"]
            json_responses[slide_id] = analyze

        json.dump(json_responses, outfile, indent=4)


async def main():
    print("-" * 20, " WELCOME ", "-" * 20)
    file_path = input("Enter the path of the presentation: ")  # validation found in PptxScanner.py
    try:
        prs_scanner = PptxScanner(file_path)
        presentation_content = prs_scanner.scan_presentation()
        # Create tasks for each slide, execute and wait for all tasks to complete
        tasks = create_tasks(presentation_content)
        prs_summary = await asyncio.gather(*tasks)
        extract_to_file(prs_summary, file_path)

    except Exception as err:
        print("some error accrued: ", err)

    finally:
        print("-" * 51)


if __name__ == "__main__":
    asyncio.run(main())
