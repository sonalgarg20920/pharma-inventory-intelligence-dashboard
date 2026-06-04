import base64

import streamlit as st

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


def get_credentials():

    creds = Credentials(
        token=None,
        refresh_token=st.secrets["gmail"]["refresh_token"],
        token_uri=st.secrets["gmail"]["token_uri"],
        client_id=st.secrets["gmail"]["client_id"],
        client_secret=st.secrets["gmail"]["client_secret"],
        scopes=SCOPES
    )

    creds.refresh(Request())

    return creds


def download_latest_stock():

    creds = get_credentials()

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    results = (
        service.users()
        .messages()
        .list(
            userId="me",
            q='subject:"Stock Detail"',
            maxResults=1
        )
        .execute()
    )

    messages = results.get(
        "messages",
        []
    )

    if not messages:
        raise Exception(
            "No Stock Detail email found."
        )

    msg_id = messages[0]["id"]

    msg = (
        service.users()
        .messages()
        .get(
            userId="me",
            id=msg_id
        )
        .execute()
    )

    subject = "Unknown"
    email_date = "Unknown"

    for header in msg["payload"]["headers"]:

        if header["name"] == "Subject":
            subject = header["value"]

        if header["name"] == "Date":
            email_date = header["value"]

    for part in msg["payload"].get(
        "parts",
        []
    ):

        filename = part.get(
            "filename"
        )

        if filename:

            attachment_id = (
                part["body"]
                ["attachmentId"]
            )

            attachment = (
                service.users()
                .messages()
                .attachments()
                .get(
                    userId="me",
                    messageId=msg_id,
                    id=attachment_id
                )
                .execute()
            )

            file_data = (
                base64.urlsafe_b64decode(
                    attachment["data"]
                )
            )

            output_file = (
                "latest_stock.xls"
            )

            with open(
                output_file,
                "wb"
            ) as f:

                f.write(file_data)

            return {
                "file_path": output_file,
                "subject": subject,
                "email_date": email_date,
                "attachment_name": filename
            }

    raise Exception(
        "No attachment found."
    )
