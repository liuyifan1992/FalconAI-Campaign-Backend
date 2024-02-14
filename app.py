import os
import smtplib
import urllib.parse

import requests

import streamlit as st
from apscheduler.schedulers.background import BackgroundScheduler
from django.http import HttpResponse
from dotenv import load_dotenv
from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate

# Load environment variables from .env file
load_dotenv()
from_email = os.getenv("HOST_EMAIL")
app_password = os.getenv("APP_PASSCODE")
link = os.getenv("LINK")

# read these parameters from user input
to_email = "yl2523@cornell.edu"
params = {"employer_id": "12345", "employee_id": "33445"}
send_email_api = "http://127.0.0.1:8000/send/email"
generate_email_content = "http://127.0.0.1:8000/generate/email"
store_email = "http://127.0.0.1:8000/store/email"


def sendEmail(message):
    print("sending mail...")
    data = {"email_content": message}
    response = requests.post(url=send_email_api, data=data)
    if response.status_code != 200:
        st.error("Failed to send email.", icon="🚨")
        return
    message = f"Subject: Test email\n\n{message}"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_email, app_password)
    server.sendmail(from_email, to_email, message)
    st.success("Email Sent.", icon="ℹ️")
    # Close the connection
    server.quit()


def scheduleEmail(sendEmail, message):
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


def generateDeeplink(base_url, params):
    deep_link = base_url + "?" + urllib.parse.urlencode(params)
    return deep_link


def readResponseFromFile(filename="email_response.txt"):
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"File {filename} not found.")


st.set_page_config(
    page_title="Generate Emails",
    page_icon="📧",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.header("Generate Emails 📧")

form_input = st.text_area("Enter the email topic", height=275)

link = generateDeeplink(link, params)
# Creating columns for the UI - To receive inputs from user
col1, col2, col3 = st.columns([10, 10, 5])
with col1:
    email_sender = st.text_input("Sender Name")
with col2:
    email_recipient = st.text_input("Recipient Name")
with col3:
    email_style = st.selectbox(
        "Writing Style", ("Formal", "Appreciating", "Not Satisfied", "Neutral"), index=0
    )


submit = st.button("Generate")

# When 'Generate' button is clicked, execute the below code
if submit:
    params = {
        "form_input": form_input,
        "email_sender": email_sender,
        "email_recipient": email_recipient,
        "email_style": email_style,
        "link": link,
    }
    response = requests.get(url=generate_email_content, params=params)
    email_content = response.content.decode("utf-8")
    st.write(email_content)
    data = {"email_content": email_content}
    response = requests.post(url=store_email, data=data)
    if response.status_code != 200:
        st.error("Failed to send email.", icon="🚨")
    filename="email_response.txt"
    st.success(f"Response saved to {filename}", icon="ℹ️")

send_email = st.button("Send Email")

if send_email:
    saved_response = readResponseFromFile()
    if saved_response:
        st.info("Sending Email...", icon="ℹ️")
        # data = {"email_content": saved_response}
        # response = requests.post(url=send_email_api, data=data)
        # if response.status_code != 200:
        #     st.error("Failed to send email.", icon="🚨")
        # st.success("Email Sent.", icon="ℹ️")
        sendEmail(saved_response)
        # scheduleEmail(sendEmail, saved_response)
