import os
import smtplib
import urllib.parse
import uuid

import requests

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from email_generator.models import AIEmail, Business, Employee, EmployeeAction
from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate


# from models import AIEmail

# Load environment variables from .env file
load_dotenv()
from_email = os.getenv("HOST_EMAIL")
app_password = os.getenv("APP_PASSCODE")

to_email = "yl2523@cornell.edu"
# read these parameters from user input
params = {"employer_id": "12345", "employee_id": "33445"}


def index(request):
    return HttpResponse("Welcome to the email generator!")


@csrf_exempt
def sendEmail(request):
    if request.method == "POST" and "email_content" in request.POST:
        # Process other email data here
        email_content = request.POST["email_content"]
        genSendEmail(email_content)
        return HttpResponse("Email sent successfully")
    else:
        raise HttpResponseBadRequest


@csrf_exempt
def scheduleEmail(request):
    if request.method == "POST" and "email_content" in request.POST:
        email_content = request.POST["email_content"]
        genScheduleEmail(genSendEmail, email_content)
        return HttpResponse("Email sent successfully")
    else:
        raise HttpResponseBadRequest


@csrf_exempt
def clickEmail(request):
    if request.method == "POST":
        # Process email click
        employee_id = request.POST["employee_id"]
        email_id = request.POST["email_id"]
        employeeAction = EmployeeAction(action_id=uuid.uuid4())
        # employeeAction.save()
        return HttpResponse("Email sent successfully")
    else:
        raise HttpResponseBadRequest


@csrf_exempt
def storeEmail(request):
    if request.method == "POST" and "email_content" in request.POST:
        email_content = request.POST["email_content"]
        # deprecate this once the DB set up is ready
        saveResponseToFile(email_content)
        email = AIEmail(email_id=uuid.uuid4(), email_content=email_content)
        # email.save()
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
        link = os.getenv("LINK")
        link = generateDeeplink(link, params)
        return HttpResponse(
            getLLMResponse(form_input, email_sender, email_recipient, email_style, link)
        )
    else:
        raise HttpResponseBadRequest


@csrf_exempt
def fetchEmail(request):
    if request.method == "GET":
        email_content = readResponseFromFile("email_response.txt")
        return HttpResponse(email_content)
    else:
        raise HttpResponseBadRequest


def saveResponseToFile(response, filename="email_response.txt"):
    with open(filename, "w") as file:
        file.write(response)


def readResponseFromFile(filename="email_response.txt"):
    try:
        with open(filename, "r") as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print("Error reading the file")


@csrf_exempt
def genSendEmail(message):
    message = f"Subject: Test email\n\n{message}"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_email, app_password)
    server.sendmail(from_email, to_email, message)
    # Close the connection
    server.quit()


@csrf_exempt
def genScheduleEmail(sendEmail, message):
    print("scheduling email...")
    # Create a scheduler instance
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        sendEmail, "cron", args=[message], day_of_week="mon-sun", hour=17, minute=25
    )
    job_id = scheduler.get_jobs()[0].id
    print(f"Job ID: {job_id}")
    # Start the scheduler
    scheduler.start()


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


def generateDeeplink(base_url, params):
    deep_link = base_url + "?" + urllib.parse.urlencode(params)
    return deep_link


@csrf_exempt
def createEmployee(request):
    if request.method == "POST" and "business_id" in request.POST:
        business_id = request.POST["business_id"]
        business = Business.objects.get(business_id=business_id)
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        employee_id = uuid.uuid4()
        employee = Employee(
            employee_id=employee_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            business=business,
        )
        employee.save()
        return HttpResponse("Employee created successfully!")
    else:
        raise HttpResponseBadRequest


@csrf_exempt
def createBusiness(request):
    if request.method == "POST":
        business_id = uuid.uuid4()
        name = request.POST["name"]
        business = Business(
            business_id=business_id,
            name=name,
        )
        business.save()
        return HttpResponse("Business created successfully!")
    else:
        raise HttpResponseBadRequest
