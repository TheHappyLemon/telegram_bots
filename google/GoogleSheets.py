import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheets:
    def __init__(self, credentials_file: str, sheet_name: str):
        """
        Initializes the Google Sheets client.
        :param credentials_file: Path to the Google service account JSON credentials file.
        :param sheet_name: Name of the Google Sheet to interact with.
        """
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, self.scope)
        self.client = gspread.authorize(self.credentials)
        self.sheet = self.client.open(sheet_name).sheet1  # Access the first sheet
    
    def append_row(self, data: list):
        """
        Appends a new row to the Google Sheet.
        :param data: List of values to append as a row.
        """
        self.sheet.append_row(data)
    
    def get_all_records(self):
        """
        Retrieves all rows from the Google Sheet as a list of dictionaries.
        """
        return self.sheet.get_all_records()
    
    def clear_sheet(self):
        """
        Clears all data in the sheet.
        """
        self.sheet.clear()
    
    def update_cell(self, row: int, col: int, value):
        """
        Updates a specific cell in the Google Sheet.
        :param row: Row number (1-based index)
        :param col: Column number (1-based index)
        :param value: New value to set
        """
        self.sheet.update_cell(row, col, value)
