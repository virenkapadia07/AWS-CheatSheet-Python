# Send Custom Verification Email to User
# Adds an email address to the list of identities for your Amazon SES account 
# in the current AWS Region and attempts to verify it. 
# As a result of executing this operation, 
# a customized verification email is sent to the specified address.

import boto3
ses = boto3.client('ses')

def SesUserStatus(email):
    try:
        response = ses.send_custom_verification_email(
            EmailAddress=email,
            TemplateName='Your Template Name'   # Change
        )
    except Exception as e:
        print("[+] ######### Exception while Sending Mail #########")
        print(e)

        return False
    else:
        print("Email Sent Successfully !!")
        return True