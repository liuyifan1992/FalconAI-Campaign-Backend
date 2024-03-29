import os
import smtplib
import uuid

import requests

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from email_generator.models import AIEmail, Business, Employee, EmployeeAction
from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate

from .utils import (
    generateDeeplink,
    getLLMResponse,
    # readResponseFromFile,
    # saveResponseToFile,
)

# from models import AIEmail

# Load environment variables from .env file
load_dotenv()
from_email = os.getenv("HOST_EMAIL")
app_password = os.getenv("APP_PASSCODE")

to_email = "yl2523@cornell.edu"
# read these parameters from user input
params = {"email_id": "11111", "employee_id": "33445"}


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
    if request.method == "GET":
        # Process email click
        employee_id = request.GET.get("employee_id")
        email_id = request.GET.get("email_id")
        employeeAction = EmployeeAction(action_id=uuid.uuid4())
        employeeAction.save()
        return HttpResponse("YOU are fucking stupid!")
    else:
        raise HttpResponseBadRequest


@csrf_exempt
def storeEmail(request):
    if request.method == "POST" and "email_content" in request.POST:
        email_content = request.POST["email_content"]
        email_id = request.POST["email_id"]
        # deprecate this once the DB set up is ready
        # saveResponseToFile(email_content)
        email = AIEmail(email_id=email_id, email_content=email_content)
        email.save()
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
        email_id = request.GET.get("email_id")
        print(email_id)
        try:
            email = AIEmail.objects.get(email_id=email_id)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest
        email_content = email.email_content
        print(email_content)
        # email_content = readResponseFromFile("email_response.txt")
        return HttpResponse(email_content)
    else:
        raise HttpResponseBadRequest


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


@csrf_exempt
def createAdmin(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        is_admin = true
        admin = FlaconAIUser(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_admin=is_admin,
        )
        admin.save()
        return HttpResponse("Admin created successfully!")
    else:
        raise HttpResponseBadRequest
