# SendMail.py
# By Murat Erenturk

import os
import pickle
import base64
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request




def GetCredentials(CredentialFilePrefix):
    creds=None
    CFP=CredentialFilePrefix+'.pkl'
    if os.path.exists(CFP):
        print("found file "+CFP+",loading...")
        with open(CFP, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Opening web UI for refreshing token...")
            creds.refresh(Request())
        else:
            CFJ=CredentialFilePrefix+'.json'
            print("Opening web UI for creating token from "+CFJ+"...")
            flow = InstalledAppFlow.from_client_secrets_file(
                CFJ, Scopes)
            creds = flow.run_local_server(port=0)
            print('Created token')
        # Save the credentials for the next run
        print('Saving...')
        with open(CFP, 'wb') as token:
            pickle.dump(creds, token)
        print('Saved token')
    else:
        print("loaded successfully")
    return creds

def CreateTxtMessage(sender,to,subject,message_text):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(message_text, 'plain'))
    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}
    return body

def CreateHtmlMessage(sender,to,subject,message_text,attached=""):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(message_text, 'html'))
    if len(attached)>0:
        my_mimetype, encoding = mimetypes.guess_type(attached)
        if my_mimetype is None or encoding is not None:
            my_mimetype = 'application/octet-stream' 
        print("Attachment mimetype:"+my_mimetype)
        main_type, sub_type = my_mimetype.split('/', 1)

        if main_type == 'text':
            temp = open(attached, 'r')  # 'rb' will send this error: 'bytes' object has no attribute 'encode'
            attachment = MIMEText(temp.read(), _subtype=sub_type)
            temp.close()

        elif main_type == 'image':
            temp = open(attached, 'rb')
            attachment = MIMEImage(temp.read(), _subtype=sub_type)
            temp.close()

        elif main_type == 'audio':
            temp = open(attached, 'rb')
            attachment = MIMEAudio(temp.read(), _subtype=sub_type)
            temp.close()            

        elif main_type == 'application' and sub_type == 'pdf':   
            temp = open(attached, 'rb')
            attachment = MIMEApplication(temp.read(), _subtype=sub_type)
            temp.close()
        elif main_type == 'application' and sub_type == 'vnd.openxmlformats-officedocument.wordprocessingml.document':   
            temp = open(attached, 'rb')
            attachment = MIMEApplication(temp.read(), _subtype=sub_type)
            temp.close()
        else:                              
            attachment = MIMEBase(main_type, sub_type)
            temp = open(attached, 'rb')
            attachment.set_payload(temp.read())
            temp.close()
        filename = os.path.basename(attached)
        attachment.add_header('Content-Disposition', 'attachment', filename=filename) # name preview in email
        msg.attach(attachment) 

    raw = base64.urlsafe_b64encode(msg.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}
    return body

def SendMessage(encoded,creds):
    service = build('gmail', 'v1', credentials=creds)
    user_id="me"
    try:    
        message = (service.users().messages().send(userId=user_id, body=encoded).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
    return ""

#Global Variables
Toolname='SendMail'
ToolVersion='0.5.20201223.1'
Scopes = 'https://www.googleapis.com/auth/gmail.send'
Client_Secret_File = 'credentials'
App_Name = 'MailSender'
to = "erenturk@goradata.com"
sender = "erenturkm@gmail.com"
subject = "Test Mail with attachment"
msgHtml = "Hi<br/><b>Html Email</b>"
msgPlain = "Hi\nPlain Email"
attachment="doc.pdf"
#Global Variables

def main():
    credentials = None
    credentials = GetCredentials(Client_Secret_File)
    print("Got credentials")
    msgEncoded=CreateHtmlMessage(sender, to, subject,msgHtml,attachment)
    SendMessage(msgEncoded,credentials)

if __name__ == '__main__':
    main()