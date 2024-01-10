from flask import Flask, render_template, request
import pandas as pd
from google.oauth2 import service_account
import gspread

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

if __name__ == "__main__":
    app.run(debug=True)
