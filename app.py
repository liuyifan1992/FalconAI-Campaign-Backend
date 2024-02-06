import smtplib
import urllib.parse

import streamlit as st
from apscheduler.schedulers.background import BackgroundScheduler
from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate

from_email = "liuyifan19926@gmail.com"
to_email = "yl2523@cornell.edu"
app_password = "ttfq xmwo tsfh admx"
link = "https://www.falcon-ai.tech/"


def sendEmail(message):
    print("sending mail...")
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


def saveResponseToFile(response, filename="email_response.txt"):
    with open(filename, "w") as file:
        file.write(response)
    st.success(f"Response saved to {filename}", icon="ℹ️")


def readResponseFromFile(filename="email_response.txt"):
    try:
        with open(filename, "r") as file:
            return file.read()
    except FileNotFoundError:
        st.error(f"File {filename} not found.")


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
    be under the email text.
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


st.set_page_config(
    page_title="Generate Emails",
    page_icon="📧",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.header("Generate Emails 📧")

form_input = st.text_area("Enter the email topic", height=275)

params = {"employer_id": "12345", "employee_id": "33445"}

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
    response = getLLMResponse(
        form_input, email_sender, email_recipient, email_style, link
    )
    st.write(response)
    saveResponseToFile(response)

send_email = st.button("Send Email")

if send_email:
    saved_response = readResponseFromFile()
    if saved_response:
        st.info("Sending Email...", icon="ℹ️")
        sendEmail(saved_response)
        # scheduleEmail(sendEmail, saved_response)
