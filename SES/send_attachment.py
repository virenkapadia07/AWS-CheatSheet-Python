# Send Attachment in Mail from SES

import boto3
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart



def SendMail():
    message = MIMEMultipart()

    client = boto3.client('ses')

    message['Subject'] = 'Your Subject'     # Change
    message['From'] = 'SENDER EMAIL'    # Change
    message['To'] = ', '.join(["RECIEVER EMAIL1","2"])  # Change
    # message body
    part = MIMEText('email body string', 'html')
    message.attach(part)
    # attachment
    part = MIMEApplication(open('Filename', 'rb').read())   # Change
    part.add_header('Content-Disposition', 'attachment', filename='Filename')       # Change #This file name will appeard in mail
    message.attach(part)
    response = client.send_raw_email(
        Source=message['From'],
        Destinations=message['To'],
        RawMessage={
            'Data': message.as_string()
        }
    )