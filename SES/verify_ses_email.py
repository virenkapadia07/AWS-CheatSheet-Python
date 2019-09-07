# Check Ses User Email Verification Status
# Given a list of identities (email addresses and/or domains), 
# returns the verification status and (for domain identities) 
# the verification token for each identity.

import boto3
ses = boto3.client('ses')


def CheckUser(email):
    try:
        response = ses.get_identity_verification_attributes(
            Identities=[
                email,
            ]
        )
    except Exception as e:
        print("[+] ######### Exception while Checking User Status #########")
        print(e)
        return False
    else:
        if response["VerificationAttributes"]:
            status = response["VerificationAttributes"][email]["VerificationStatus"]
            
            return status
        else:
            return "New User"