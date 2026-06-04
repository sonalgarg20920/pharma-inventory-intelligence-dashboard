import os
import glob
import base64

import streamlit as st

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


def running_in_cloud():

    return (
        os.environ.get(
            "STREAMLIT_SERVER_HEADLESS"
        )
        is not None
    )

def get_credentials():

    st.write("SECRETS KEYS:", list(st.secrets.keys()))

    try:

        if (
            "gmail" in st.secrets
            and
            "refresh_token" in st.secrets["gmail"]
        ):

            st.write("Using Cloud Credentials")

            return get_cloud_credentials()

    except Exception as e:

        st.write("Secrets Error:", str(e))

    st.write("Using Local Credentials")

    return get_local_credentials()

def get_local_credentials():

    creds = None

    if os.path.exists("token.json"):

        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        if (
            creds
            and creds.expired
            and creds.refresh_token
        ):

            creds.refresh(
                Request()
            )

        else:

            client_secret_file = glob.glob(
                "client_secret*.json"
            )[0]

            flow = (
                InstalledAppFlow
                .from_client_secrets_file(
                    client_secret_file,
                    SCOPES
                )
            )

            creds = flow.run_local_server(
                port=8081
            )

        with open(
            "token.json",
            "w"
        ) as token:

            token.write(
                creds.to_json()
            )

    return creds


def get_credentials():

    if running_in_cloud():
        return get_cloud_credentials()

    return get_local_credentials()


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
