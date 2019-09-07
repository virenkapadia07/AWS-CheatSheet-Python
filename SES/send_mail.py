# Send Email from SES
# Composes an email message and immediately queues it for sending

import boto3

ses = boto3.client('ses')

def SendMail(email):
    #Send Mail for verified user
    SENDER = "SENDER Email"        # Change  Note: Sender mail should be verified on SES before sending Mail
    RECIPIENT = "RECIPIENT Email"   # Change Note: Can send tp more than one user by seperating with ","
    SUBJECT = "Your Subject"        # Change

    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )
            
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Your Content</h1>
    </body>
    </html>"""  # Change

    CHARSET = "UTF-8"

    try:
        #Provide the contents of the email.
        email_response = ses.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except Exception as e:
        print("[+] ######### Exception While Sending Mail #########")
        print(str(e))

        return False
    else:
        print("[+] Email sent!")

        return True