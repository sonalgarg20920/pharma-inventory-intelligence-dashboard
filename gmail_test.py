import base64

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

CLIENT_SECRET_FILE = (
    'client_secret_540864342242-'
    'mj3504e19uq6997icitjp63o92o3v73v.'
    'apps.googleusercontent.com.json'
)

flow = InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRET_FILE,
    SCOPES
)

creds = flow.run_local_server(port=8080)

service = build(
    'gmail',
    'v1',
    credentials=creds
)

query = 'subject:"Stock Detail"'

results = service.users().messages().list(
    userId='me',
    q=query,
    maxResults=1
).execute()

messages = results.get('messages', [])

if not messages:
    print("No email found")
    exit()

msg_id = messages[0]['id']

msg = service.users().messages().get(
    userId='me',
    id=msg_id
).execute()

for part in msg['payload'].get('parts', []):

    filename = part.get('filename')

    if filename:

        attachment_id = (
            part['body']['attachmentId']
        )

        attachment = (
            service.users()
            .messages()
            .attachments()
            .get(
                userId='me',
                messageId=msg_id,
                id=attachment_id
            )
            .execute()
        )

        file_data = base64.urlsafe_b64decode(
            attachment['data']
        )

        with open(
            "latest_stock.xls",
            "wb"
        ) as f:
            f.write(file_data)

        print(
            f"Downloaded: {filename}"
        )
