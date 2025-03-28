from GoogleSheets import GoogleSheets

# Define credentials file and sheet name
CREDENTIALS_FILE = "credentials.json"
SHEET_NAME = "test_sheet"

# Initialize GoogleSheets instance
gs = GoogleSheets(CREDENTIALS_FILE, SHEET_NAME)

# Sample data to append
data = ["Test User", "test@example.com", "Hello from Python!"]

# Append the data to the sheet
gs.append_row(data)

print("✅ Row added successfully!")
