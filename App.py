from PptxScanner import PptxScanner


def ai_text_analyzer(presentation):
    import openai

    OPENAI_API_KEY = "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"

    openai.api_key = OPENAI_API_KEY
    system_prompt = "You're an AI text analyzer assisting with presentation summarization.For each slide's content you"\
                    " receive, generate a concise summary of the text.\n User:'Slide content'\nAI:'Summary explanation'"
    messages = [{"role": "system", "content": system_prompt}]  # the behavior of the system
    responses = []

    for index, slide_content in enumerate(presentation):
        # set instructions to the chat as a user message (the slide content)
        messages.append({"role": "user", "content": slide_content})
        # sends the request
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        # get response
        chat_response = completion.choices[0].message.content
        # keeping the history of the chat
        messages.append({"role": "assistant", "content": chat_response})
        responses.append(chat_response + "\n")

    return responses


def main():
    print("-" * 20, "Hello ChatBot", "-" * 20)
    file_path = input("Enter the path to the presentation file: ")

    try:
        prs_scanner = PptxScanner(file_path)
        presentation_content = prs_scanner.scan_presentation()
        print(ai_text_analyzer(presentation_content))
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
