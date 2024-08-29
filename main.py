from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
from googleapiclient.discovery import build
import openai
import config

# Initialize OpenAI
openai.api_key = config.OPENAI_API_KEY

# Gmail API Setup
def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', config.GMAIL_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                config.GMAIL_CLIENT_SECRET_FILE, config.GMAIL_SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def list_emails(service):
    results = service.users().messages().list(userId='me', q='').execute()
    messages = results.get('messages', [])
    if not messages:
        print('No messages found.')
    else:
        print('Messages:')
        for message in messages[:10]:  # Limit to first 10 messages
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            print(f"From: {msg['payload']['headers'][0]['value']}")
            print(f"Subject: {msg['payload']['headers'][1]['value']}")
            print(f"Snippet: {msg['snippet']}")
            print()

def get_openai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=50
    )
    return response.choices[0].message['content']

if __name__ == '__main__':
    service = authenticate_gmail()
    list_emails(service)
    prompt = "Tell me a joke."
    response = get_openai_response(prompt)
    print(f"OpenAI Response: {response}")
