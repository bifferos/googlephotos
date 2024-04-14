#!/usr/bin/env python3

import json
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scopes your application needs
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']


def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json',  # Path to your client secret JSON file
        scopes=SCOPES
    )
    credentials = flow.run_local_server(port=0)
    # After the user has completed the authorization flow, store the refresh token
    with open('credentials.json', 'w') as json_file:
        json.dump(credentials_to_dict(credentials), json_file)


if __name__ == "__main__":
    main()

