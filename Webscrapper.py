import logging
import requests
import lxml.html
import azure.functions as func
from datetime import date, datetime, tzinfo

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import pickle


def main(mytimer: func.TimerRequest)-> None:
    utc_timestamp =datetime.datetime,utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    
    if mytimer.past_due:
        logging.info('The timer is past due!')
    link = "https://covidindia.org/"
    requesting = requests.get(link)
    content = lxml.html.fromstring(requesting.content)
    table = content.xpath('//tr')

data = []


data.append(str(utc_timestamp))
client_credentials={
'type': 'service_account',
'project_id': 'covid-288609',
'pricate_key_id': '5c034308e3edea7830d3257069fd1f8cf20ff619',
'private_key' : '-----BEGIN PRIVATE KEY-----\nMIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoBAQCqRmpL4ZSxptIw\ndrs17js1BQC1AdrjNgbH/P/q9pP1EpB6WGpOu0FgJ',
'client_email' : 'adithya@covid-288609.iam.gserviceaccount.com',
'client_id': '115010989583143165655',
'auth_uri' : 'https://accounts.google.com/o/oauth2/auth',
'token_uri': 'https://oauth.googleapis.com/token',
'auth_provider_x509_cert_url' : 'https://www.googleapis.com/robot/v1/metadata/x509/adithya%40covid-288609.iam.gserviceaccount.com'
}


i=0
for j in table[31]:
    i+=1
    name=j.text_content()
    data.append(name)
print(data)

scope = ['https://www.googleapis.com/auth/drive']


credentials = ServiceAccountCredentials._from_parsed_json_keyfile(client_credentials, scope,token_uri=None,revoke_uri=None)
client = gspread.authorize(credentials)
sheet=client.open('trail 1').sheet1
sheet.append_row(data)
logging.info('Python time trigger function ran at %s' str(data))