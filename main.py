import streamlit as st
import pandas as pd
import gspread
from gspread_pandas import Spread, Client
from google.oauth2 import service_account
from gsheetsdb import connect

# Disable certificate verification (Not necessary always)
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Create a Google Authentication connection object
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"], scopes=scope)

sheet_url = st.secrets["private_gsheets_url"]

# Check the connection
# client = Client(scope=scope, creds=credentials)
# spread = Spread(sheet_url, client=client)
# st.write(spread.url)


# Create a connection to the Google Sheet
client2 = gspread.authorize(credentials=credentials)
sheet = client2.open_by_url(sheet_url).sheet1

# Display Image
st.image(
        "https://i1.wp.com/hrnxt.com/wp-content/uploads/2021/07/Hindustan-Petroleum.jpg?resize=580%2C239&ssl=1",
        # Manually Adjust the width of the image as per requirement
    )
# Create a form
st.title("Bills")
outlet_name = st.selectbox("Outlet Name", ["McDonald's", "Starbucks", "KFC"])
date = st.date_input("Date")
amount = st.number_input("Amount")
bill_no = st.number_input("Bill No")

# Submit the form
if st.button("Submit"):
    # Create a new row in the Google Sheet
    row = [outlet_name, date.isoformat(), amount, bill_no]
    sheet.append_row(row)

    # Display a success message
    st.success("Bill submitted successfully!")
