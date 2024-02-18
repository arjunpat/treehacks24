import os
from datetime import datetime
from io import BytesIO

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from PIL import Image
from io import BytesIO
import requests
from datetime import datetime
import base64


# Google Photos API scope
SCOPES = ["https://www.googleapis.com/auth/photoslibrary.readonly", 'https://www.googleapis.com/auth/gmail.readonly']
API_VERSION = "v1"


def authenticate():
    creds = None
    token_path = "token.json"

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("creds.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as token:
            token.write(creds.to_json())

    return creds


def retrieve_photos():
    creds = authenticate()

    # Use specific version for Google Photos API
    service = build(
        "photoslibrary", API_VERSION, credentials=creds, static_discovery=False
    )

    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    start_year, start_month, start_day = map(int, start_date.split("-"))
    end_year, end_month, end_day = map(int, end_date.split("-"))

    filters = {
        "dateFilter": {
            "ranges": [
                {
                    "startDate": {
                        "year": start_year,
                        "month": start_month,
                        "day": start_day,
                    },
                    "endDate": {"year": end_year, "month": end_month, "day": end_day},
                }
            ]
        }
    }

    # Correctly include pageSize in the request body
    request_body = {
        "filters": filters,
        "pageSize": 100,  # Adjusted pageSize to retrieve more items
    }

    # Retrieve media items based on the date range
    results = service.mediaItems().search(body=request_body).execute()

    items = results.get("mediaItems", [])
    print(items)

    # for item in items:
    #     base_url = item["baseUrl"]
    #     img_data = requests.get(f"{base_url}=d").content

    #     image = Image.open(BytesIO(img_data))
    #     image.show()

def get_most_recent_emails():
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=100).execute()
    messages = results.get('messages', [])

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        headers = msg['payload']['headers']
        subject = [i['value'] for i in headers if i['name'] == 'Subject'][0]
        from_email = [i['value'] for i in headers if i['name'] == 'From'][0]
        print(f"From: {from_email}")
        print(f"Subject: {subject}")

        # This gets the whole email lowkey can j use snippet tho
        # if 'parts' in msg['payload']:
        #     for part in msg['payload']['parts']:
        #         if part['mimeType'] == 'text/plain':
        #             data = part['body']['data']
        #             text = base64.urlsafe_b64decode(data.encode('ASCII')).decode('utf-8')
        #             print("Email Body:")
        #             print(text)
        # else:
        #     print("Email Body Not Available in Plain Text")


        print(f"Snippet: {msg['snippet']}")

        print("\n")



if __name__ == "__main__":
    # retrieve_photos()
    get_most_recent_emails()
