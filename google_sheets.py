import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import GOOGLE_SHEETS_CREDENTIALS_PATH, GOOGLE_SHEET_ID

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_sheets_service():
    """
    Authenticates and returns a Google Sheets service instance.
    """
    creds = service_account.Credentials.from_service_account_file(
        GOOGLE_SHEETS_CREDENTIALS_PATH, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service

def update_or_add_row(data: dict):
    """
    Updates an existing row if the job listing (by URL) exists, or appends a new row.
    
    The Google Sheet must have a header row with keys matching the data keys.
    """
    service = get_sheets_service()
    sheet = service.spreadsheets()
    
    # Read existing data
    result = sheet.values().get(spreadsheetId=GOOGLE_SHEET_ID, range="A1:Z1000").execute()
    values = result.get("values", [])
    if not values:
        logger.error("Google Sheet appears to be empty. Ensure headers are set.")
        raise Exception("Empty Google Sheet")
    
    headers = values[0]
    try:
        url_index = headers.index("original_listing_url")
    except ValueError:
        logger.error("Header 'original_listing_url' not found in sheet.")
        raise

    row_to_update = None
    for idx, row in enumerate(values[1:], start=2):
        if len(row) > url_index and row[url_index] == data.get("original_listing_url"):
            row_to_update = idx
            break

    # Prepare row data based on headers
    row_data = [data.get(header, "") for header in headers]
    if row_to_update:
        # Update existing row
        body = {
            "values": [row_data]
        }
        sheet.values().update(
            spreadsheetId=GOOGLE_SHEET_ID,
            range=f"A{row_to_update}:Z{row_to_update}",
            valueInputOption="RAW",
            body=body
        ).execute()
        logger.info(f"Updated row {row_to_update} in Google Sheet.")
    else:
        # Append new row
        body = {
            "values": [row_data]
        }
        sheet.values().append(
            spreadsheetId=GOOGLE_SHEET_ID,
            range="A1",
            valueInputOption="RAW",
            body=body
        ).execute()
        logger.info("Appended new row to Google Sheet.")
