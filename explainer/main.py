"""
              main.py
     ------------------------
    The main file of the project.

     TO RUN THE PROGRAM:
   1. pip install python-pptx
   2. pip install openai
   3. pip install backoff

   python main.py <path_to_presentation>

--> notice that the program includes API_KEY,
    you have to set it to your correct key(in apiAnalyzer.py),
    without it the program will fail.
--> The program includes the bonus requirements.

    Enjoy!
"""

import argparse
import asyncio
from App import run


def configure_cli() -> str:
    """ Configure the CLI
    :return: the path of the presentation
    """
    parser = argparse.ArgumentParser(description="Presentation Summarization CLI")
    parser.add_argument("presentation_path", type=str, help="Path to the presentation file")
    args = parser.parse_args()
    return args.presentation_path


async def main():
    presentation_path = configure_cli()
    await run(presentation_path)

if __name__ == "__main__":
    asyncio.run(main())
