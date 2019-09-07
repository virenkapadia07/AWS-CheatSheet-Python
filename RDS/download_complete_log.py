# AWS Version 4 signing example for RDS DownloadComplete Log file
# For temporary credentials uncomment lines 36 and 87 
# Tested with Python 3.7.3

import sys, os, base64, datetime, hashlib, hmac, urllib
import requests # pip install requests

from boto3 import session

method = 'GET'
service = 'rds'
region = input('Enter region (Example: us-east-1): ')
host = 'rds.' + region + '.amazonaws.com'
instance_name = input('Enter DB Instance Identifier: ')
logfile = input('Enter log file name (with full path): ')
rds_endpoint = 'https://' + host
uri = '/v13/downloadCompleteLogFile/' + instance_name + '/' + logfile
endpoint =  rds_endpoint + uri

# Key derivation functions. Taken from https://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

# Get session credentials 
session = session.Session()
cred = session.get_credentials()
access_key = cred.access_key
secret_key = cred.secret_key
# session_token = cred.token

if access_key is None or secret_key is None:
    print ("Credentials are not available.")
    sys.exit()

# Create a date for headers and the credential string
t = datetime.datetime.utcnow()
amzdate = t.strftime('%Y%m%dT%H%M%SZ') # Format date as YYYYMMDD'T'HHMMSS'Z'
datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope

# Overview:
# Create a canonical request - https://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html
# Sign the request.
# Attach headers.
# Send request

# Create canonical URI--the part of the URI from domain to query
canonical_uri = uri

# Create the canonical headers
canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'
# signed_headers is the list of headers that are being included as part of the signing process.
signed_headers = 'host;x-amz-date'

# Using recommended hashing algorithm SHA-256
algorithm = 'AWS4-HMAC-SHA256'
credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'

# Canonical query string. All parameters are sent in http header instead in this example so leave this empty.
canonical_querystring = ''

# Create payload hash. For GET requests, the payload is an empty string ("").
payload_hash = hashlib.sha256(''.encode('utf-8')).hexdigest()

# Create create canonical request
canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

# String to sign
string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()

# Create the signing key
signing_key = getSignatureKey(secret_key, datestamp, region, service)

# Sign the string_to_sign using the signing_key
signature = hmac.new(signing_key, (string_to_sign).encode("utf-8"), hashlib.sha256).hexdigest()

# Add signed info to the header
authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
headers = {'Accept-Encoding':'gzip', 'x-amz-date':amzdate, 'Authorization':authorization_header}
#headers = {'Accept-Encoding':'gzip', 'x-amz-date':amzdate, 'x-amz-security-token':session_token, 'Authorization':authorization_header}

# Send the request
r = requests.get(endpoint, headers=headers, stream=True)

print ("Logs Downloaded!")
print ("Response Code: " + str(r.status_code))
print ("Content-Encoding: " + r.headers['content-encoding'])

oname = input('Enter output file name (fullpath): ')
with open(oname, 'w') as f:
    for part in r.iter_content(chunk_size=8192):
        f.write(str(part).replace(r'\n', '\n'))

print ("Log file saved to " + oname)