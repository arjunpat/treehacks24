import os
from datetime import datetime
from io import BytesIO

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from PIL import Image

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


if __name__ == "__main__":
    retrieve_photos()
