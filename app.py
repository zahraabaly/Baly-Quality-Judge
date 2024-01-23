from flask import Flask, render_template, request,jsonify  
import pandas as pd
from google.oauth2 import service_account
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials as ServiceAccountCredentials

app = Flask(__name__)

# Load Google Sheets using API credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = service_account.Credentials.from_service_account_file("C:/Users/lenovo/Desktop/New project/baly-quality-judge-07fdacfafbc5.json", scopes=scope)
gc = gspread.authorize(creds)

# Function to get the updated DataFrame from the Google Sheet
def get_updated_worksheet():
    sh = gc.open("All Quality Judge (New process)")
    worksheet = sh.worksheet("CC Cases")
    return worksheet

# Initial DataFrame
worksheet = get_updated_worksheet()

# Function to get the updated DataFrame from the Google Sheet
def get_updated_dataframe():
    sh = gc.open("All Quality Judge (New process)")
    worksheet = sh.worksheet("CC Cases")
    data_list = worksheet.get_all_records()
    df = pd.DataFrame(data_list)
    return df

# Initial DataFrame
df = get_updated_dataframe()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    driver_id = request.args.get("driverId")
    print("Rece.ived Driver ID:", (driver_id))

    # Get the updated DataFrame
    global df
    df = get_updated_dataframe()
    
    # Filter the DataFrame
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

        print("Received Driver ID:", (driver_id))
        print("Received reason:", (reason))
        print("Received city:", (city))
        print("Received service type:", (service_type))

        client = gspread.authorize(creds)

        # Get the updated DataFrame
        global worksheet
        worksheet = get_updated_worksheet()

        # Get the last empty row in column B
        next_row = len(worksheet.col_values(2)) + 1

        # Insert data into the corresponding columns
        worksheet.update_cell(next_row, 1, str(datetime.now().strftime('%Y-%m-%d')))  # Insert current date in column A
        worksheet.update_cell(next_row, 2, driver_id)  # Insert driver ID in column B
        worksheet.update_cell(next_row, 3, reason)  # Insert reason in column C
        worksheet.update_cell(next_row, 7, city)  # Insert city in column G
        worksheet.update_cell(next_row, 8, service_type)  # Insert service type in column H

        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    app.run(debug=True)