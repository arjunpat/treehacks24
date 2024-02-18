import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from PIL import Image
from io import BytesIO
import requests

# Google Photos API scope
SCOPES = ["https://www.googleapis.com/auth/photoslibrary.readonly"]
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
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as token:
            token.write(creds.to_json())

    return creds

def retrieve_photos():
    creds = authenticate()
    
    # Use specific version for Google Photos API
    service = build("photoslibrary", API_VERSION, credentials=creds, static_discovery=False)
    
    results = (
        service.mediaItems()
        .list(pageSize=10)  # You can change the page size
        .execute()
    )
    print(results)

    items = results.get("mediaItems", [])

    for item in items:
        base_url = item["baseUrl"]
        img_data = requests.get(base_url).content

        image = Image.open(BytesIO(img_data))
        image.show()

if __name__ == "__main__":
    retrieve_photos()