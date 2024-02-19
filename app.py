import os
import smtplib
import urllib.parse
import uuid

import requests

import streamlit as st
from django.http import HttpResponse


send_email_api = "http://127.0.0.1:8000/send/email"
generate_email_content = "http://127.0.0.1:8000/generate/email"
store_email = "http://127.0.0.1:8000/store/email"
fetch_email = "http://127.0.0.1:8000/fetch/email"
# don't use this email id
email_id = "abcd_edfe888_ryan_rocks"


st.set_page_config(
    page_title="Generate Emails",
    page_icon="📧",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.header("Generate Emails 📧")

form_input = st.text_area("Enter the email topic", height=275)

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
# email_id = uuid.uuid4()

# When 'Generate' button is clicked, execute the below code
if submit:
    params = {
        "form_input": form_input,
        "email_sender": email_sender,
        "email_recipient": email_recipient,
        "email_style": email_style,
    }
    response = requests.get(url=generate_email_content, params=params)
    email_content = response.content.decode("utf-8")
    st.write(email_content)
    data = {"email_content": email_content, "email_id": email_id}
    response = requests.post(url=store_email, data=data)
    if response.status_code != 200:
        st.error("Failed to send email.", icon="🚨")
    filename = "email_response.txt"
    st.success(f"Response saved to {filename}", icon="ℹ️")

send_email = st.button("Send Email")

if send_email:
    params = {
        "email_id": email_id,
    }
    response = requests.get(url=fetch_email, params=params)
    saved_response = response.content.decode("utf-8")
    st.write(saved_response)
    if saved_response:
        st.info("Sending Email...", icon="ℹ️")
        data = {"email_content": saved_response}
        response = requests.post(url=send_email_api, data=data)
        if response.status_code != 200:
            st.error("Failed to send email.", icon="🚨")
        st.success("Email Sent.", icon="ℹ️")
        # sendEmail(saved_response)
        # scheduleEmail(sendEmail, saved_response)
