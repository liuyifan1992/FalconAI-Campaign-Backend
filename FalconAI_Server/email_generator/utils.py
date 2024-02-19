import urllib.parse

from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate


def generateDeeplink(base_url, params):
    deep_link = base_url + "?" + urllib.parse.urlencode(params)
    return deep_link


# def saveResponseToFile(response, filename="email_response.txt"):
#     with open(filename, "w") as file:
#         file.write(response)


# def readResponseFromFile(filename="email_response.txt"):
#     try:
#         with open(filename, "r") as file:
#             content = file.read()
#             return content
#     except FileNotFoundError:
#         print("Error reading the file")


def getLLMResponse(form_input, email_sender, email_recipient, email_style, link):
    # load the Llama2 model
    llm = CTransformers(
        model="models/ggml-model-q4_0.bin",
        model_type="llama",
        config={"max_new_tokens": 256, "temperature": 0.01},
    )

    # Template for building the PROMPT
    template = """
    Write an email body with {style} style and includes topic :{email_topic}.\n\nSender: {sender}\nRecipient: {recipient}
    Remember to write just the email body not the subject. Also, please include a hyperlink to {link}. The hyperlink should
    be embedded in text.
    \n\nEmail Text:

    """

    # Creating the final PROMPT
    prompt = PromptTemplate(
        input_variables=["style", "email_topic", "sender", "recipient", "link"],
        template=template,
    )

    # Generating the response using LLM
    response = llm(
        prompt.format(
            email_topic=form_input,
            sender=email_sender,
            recipient=email_recipient,
            style=email_style,
            link=link,
        )
    )
    print(response)

    return response
