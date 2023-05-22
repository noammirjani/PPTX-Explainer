"""


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


async def main():
    print("-" * 20, "Presentation Analysis by AI", "-" * 20)
    file_path = input("Enter the path to the presentation file: ")

    try:
        prs_scanner = PptxScanner(file_path)
        presentation_content = prs_scanner.scan_presentation()

        # Create tasks for each slide, execute and wait for all tasks to complete
        tasks = create_tasks(presentation_content)
        prs_summary = await asyncio.gather(*tasks)

        for x in prs_summary:
            print(x)
    except Exception as e:
        print(e)
    finally:
        print("-" * 70)


if __name__ == "__main__":
    asyncio.run(main())
