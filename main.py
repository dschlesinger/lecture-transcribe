import os, sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import whisper

from dotenv import load_dotenv

load_dotenv()

# Check if file provided is valid
def check_path(file_path) -> str:

  path = os.getenv('AUDIO_PATH') + '/' + file_path

  print(path)

  if not os.path.exists(path):

    raise ValueError(f'File {file_path} not found')
  
  return path

# Load Model
model = whisper.load_model("tiny")

SCOPES = ['https://www.googleapis.com/auth/docs', 'https://www.googleapis.com/auth/drive']

def main(file_name: str):

  path = check_path(file_name)

  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.

  sk = "key.apps.googleusercontent.com.json"

  if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          sk, SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  drive_service = build('drive', 'v3', credentials=creds)
  doc_service = build('docs', 'v1', credentials=creds)

  folder_id = os.getenv('FOLDER_ID')

  # Metadata for the new document
  file_metadata = {
      'name': file_name,
      'mimeType': 'application/vnd.google-apps.document',
      'parents': [folder_id]
  }

  # Create the document
  file = drive_service.files().create(
      body=file_metadata,
      fields='id, name'
  ).execute()

  doc_id = file.get('id')

  text_to_insert = model.transcribe(path)

  # Create a request to insert text at the beginning of the document
  requests = [
      {
          'insertText': {
              'location': {
                  'index': 1,  # Index 1 places the text at the beginning
              },
              'text': '[THIS IS AN AUDIO TRANSCRIPT REFER TO DOCUMENTS IF CONFLICTING INFORMATION OR TYPOS]' + text_to_insert['text']
          }
      }
  ]

  # Execute the batchUpdate request
  doc_service.documents().batchUpdate(
      documentId=doc_id,
      body={'requests': requests}
  ).execute()

if __name__ == "__main__":

  for file in os.listdir('audio'):

    if file.split('.')[-1] == 'mp3':

      main(file)