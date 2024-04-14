#!/usr/bin/env python3

import json
from typing import List
from pathlib import Path
from pprint import pprint
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


DUMMY_ACCESS_TOKEN = 'dummy_access_token'
SCOPES: List[str] = ['https://www.googleapis.com/auth/photoslibrary.readonly']
API_SERVICE_NAME = 'photoslibrary'
API_VERSION = 'v1'


def make_credentials(creds_path) -> Credentials:
    creds = json.load(creds_path.open("r"))
    client_id = creds["client_id"]
    client_secret = creds["client_secret"]
    refresh_token = creds["refresh_token"]

    return Credentials(
        token=DUMMY_ACCESS_TOKEN,
        refresh_token=refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES
    )


def enum_image_metadata(service):
    # Search for media items by filename
    response = service.mediaItems().search(body={
        "pageSize": 10,
        "filters": {
            "mediaTypeFilter": {
                "mediaTypes": ["PHOTO"]
            },
            "includeArchivedMedia": False
        }
    }).execute()

    pprint(response)


def get_image_metadata(service, item_id):
    # Search for media items by filename
    response = service.mediaItems().get(mediaItemId=item_id).execute()
    pprint(response)


def main():
    creds_path = Path("credentials.json")
    credentials = make_credentials(creds_path)
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials, static_discovery=False)
    # enum_image_metadata(service)
    get_image_metadata(service, "<ID>")


if __name__ == "__main__":
    main()
