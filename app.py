import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
import smtplib

from_email = "liuyifan19926@gmail.com"
to_email = "Ryantobin77@gmail.com"
app_password= "ttfq xmwo tsfh admx"

def sendEmail(message):
    print("sending mail...")
    message = f"Subject: Test email\n\n{message}"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, app_password)
    server.sendmail(from_email, to_email, message)
    st.success('Email Sent.', icon="ℹ️")
    # Close the connection
    server.quit()

def saveResponseToFile(response, filename="email_response.txt"):
    with open(filename, 'w') as file:
        file.write(response)
    st.success(f'Response saved to {filename}', icon="ℹ️")

def readResponseFromFile(filename="email_response.txt"):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        st.error(f'File {filename} not found.')

def getLLMResponse(form_input,email_sender,email_recipient,email_style):
    #load the Llama2 model
    llm = CTransformers(model='models/ggml-model-q4_0.bin',
                    model_type='llama',
                    config={'max_new_tokens': 256,
                            'temperature': 0.01})


    #Template for building the PROMPT
    template = """
    Write an email body with {style} style and includes topic :{email_topic}.\n\nSender: {sender}\nRecipient: {recipient}
    Remember to write just the email body not the subject.
    \n\nEmail Text:

    """

    #Creating the final PROMPT
    prompt = PromptTemplate(
    input_variables=["style","email_topic","sender","recipient"],
    template=template,)


    #Generating the response using LLM
    response=llm(prompt.format(email_topic=form_input,sender=email_sender,recipient=email_recipient,style=email_style))
    print(response)

    return response


st.set_page_config(page_title="Generate Emails",
                    page_icon='📧',
                    layout='centered',
                    initial_sidebar_state='collapsed')
st.header("Generate Emails 📧")

form_input = st.text_area('Enter the email topic', height=275)

#Creating columns for the UI - To receive inputs from user
col1, col2, col3 = st.columns([10, 10, 5])
with col1:
    email_sender = st.text_input('Sender Name')
with col2:
    email_recipient = st.text_input('Recipient Name')
with col3:
    email_style = st.selectbox('Writing Style',
                                    ('Formal', 'Appreciating', 'Not Satisfied', 'Neutral'),
                                       index=0)


submit = st.button("Generate")

#When 'Generate' button is clicked, execute the below code
if submit:
    response = getLLMResponse(form_input,email_sender,email_recipient,email_style)
    st.write(response)
    saveResponseToFile(response)

send_email = st.button("Send Email")

if send_email:
    saved_response = readResponseFromFile()
    if saved_response:
        st.info('Sending Email...', icon="ℹ️")
        sendEmail(saved_response)