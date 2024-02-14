import os
import smtplib
import urllib.parse

import requests

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate


# from models import AIEmail


def index(request):
    return HttpResponse("Welcome to the email generator!")


@csrf_exempt
def sendEmail(request):
    if request.method == "POST" and "email_content" in request.POST:
        # Process other email data here
        email_content = request.POST["email_content"]
        # sendEmail(email_content)
        return JsonResponse({"email_content": email_content}, status=200)
    else:
        raise HttpResponseBadRequest


@csrf_exempt
def storeEmail(request):
    if request.method == "POST" and "email_content" in request.POST:
        # Process other email data here
        email_content = request.POST["email_content"]
        saveResponseToFile(email_content)
        return JsonResponse({"email_content": email_content}, status=200)
    else:
        raise HttpResponseBadRequest


@csrf_exempt
def generateEmail(request):
    if request.method == "GET":
        form_input = request.GET.get("form_input")
        email_sender = request.GET.get("email_sender")
        email_recipient = request.GET.get("email_recipient")
        email_style = request.GET.get("email_style")
        link = request.GET.get("link")
        return HttpResponse(
            getLLMResponse(form_input, email_sender, email_recipient, email_style, link)
        )
        # return JsonResponse({"email_content": email_content}, status=200)
    else:
        raise HttpResponseBadRequest


def saveResponseToFile(response, filename="email_response.txt"):
    with open(filename, "w") as file:
        file.write(response)


# def sendEmail(message):
#     print("sending mail...")
#     message = f"Subject: Test email\n\n{message}"
#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#     server.login(from_email, app_password)
#     server.sendmail(from_email, to_email, message)
#     # Close the connection
#     server.quit()


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
