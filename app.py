from flask import Flask, render_template, request,jsonify  
import pandas as pd
from google.oauth2 import service_account
import gspread
from datetime import datetime
import traceback
# from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials as ServiceAccountCredentials

app = Flask(__name__)

# Load Google Sheets using API credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = service_account.Credentials.from_service_account_file("C:/Users/lenovo/Desktop/New project/baly-quality-judge-07fdacfafbc5.json", scopes=scope)
gc = gspread.authorize(creds)

# Open the Google Sheet by title
spreadsheet_title = "All Quality Judge (New process)"
sh = gc.open(spreadsheet_title)

# worksheet name is "CC Cases"
worksheet = sh.worksheet("CC Cases")
data_list = worksheet.get_all_records()
df = pd.DataFrame(data_list)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    driver_id = request.args.get("driverId")
    print("Received Driver ID:", (driver_id))
    filtered_data = df[df["Driver Id"] == int(driver_id)]
    return render_template("result.html", data=filtered_data.to_html(index=False)) 


@app.route("/insert_data", methods=["POST"])
def insert_data():
    try:
        # Extract data from the JSON request body
        data = request.get_json()
        driver_id = data.get("driverId")
        reason = data.get("reason")
        city = data.get("city")
        service_type = data.get("serviceType")

        # Authorize and open the Google Sheet
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/lenovo/Desktop/New project/baly-quality-judge-07fdacfafbc5.json", scope)
        client = gspread.authorize(creds)
        
        # Open the Google Sheet by title
        spreadsheet_title = "All Quality Judge (New process)"
        sh = client.open(spreadsheet_title)

        # worksheet name is "CC Cases"
        sheet = sh.worksheet("CC Cases")
        
        # Get the last empty row in column B
        next_row = len(sheet.col_values(2)) + 1

        # Insert data into the corresponding columns
        sheet.update_cell(next_row, 1, str(datetime.now()))  # Insert current date in column A
        sheet.update_cell(next_row, 2, driver_id)  # Insert driver ID in column B
        sheet.update_cell(next_row, 3, reason)  # Insert reason in column C
        sheet.update_cell(next_row, 7, city)  # Insert city in column G
        sheet.update_cell(next_row, 8, service_type)  # Insert service type in column H

        return jsonify({"status": "success"})
    except Exception as e:
        print("Error during data insertion:", str(e))
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
