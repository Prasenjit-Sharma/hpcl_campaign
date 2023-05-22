import streamlit as st
import gspread
import pandas as pd
from google.oauth2 import service_account

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

# Read Dealer Data
df = pd.read_csv('Dealers.csv')

# Read Dealer Data from gsheet
# dsheet = client2.open_by_url(sheet_url).worksheet('Dealer')
# df = pd.DataFrame(dsheet.get_all_records())


# Display Image
st.image(
    "https://i1.wp.com/hrnxt.com/wp-content/uploads/2021/07/Hindustan-Petroleum.jpg?resize=580%2C239&ssl=1",
    # Manually Adjust the width of the image as per requirement
)
# Create a form
st.header("Bharo Aur Jeeto Dhamaka")
st.subheader("Please fill the details of Bill")
district_name = st.selectbox("District", options=df['DISTRICT'].unique())

df = df[df['DISTRICT'] == district_name]
if district_name:
    outlet_name = st.selectbox("Petrol Pump", df['PETROL_PUMP'])
date = st.date_input("Date")


col1, col2 = st.columns(2)
with col1:
    veh_type = st.radio("Type of Vehicle", ('2/3 Wheeler', '4 Wheeler'), horizontal=True)

with col2:
    tank_full = st.checkbox("Tank Full", value=False)

if veh_type == '2/3 Wheeler':
    amount = st.number_input("Bill Amount", min_value=350)
else:
    amount = st.number_input("Bill Amount", min_value=2000)
bill_no = st.number_input("Bill Number", format="%0.0f")
contact_no = st.number_input("Mobile Number", format="%0.0f")

st.info('Please retail the original bill till end of campaign period.', icon="ℹ️")

# Submit the form
with st.spinner('Wait for it...'):
    if st.button("Press To Submit"):
        if outlet_name and date and amount and bill_no and contact_no:
            # Create a new row in the Google Sheet
            row = [district_name, outlet_name, date.isoformat(), veh_type, amount, bill_no, contact_no, tank_full]
            sheet.append_row(row)

            # Display a success message
            st.success("Bill submitted successfully!")
            st.balloons()
        else:
            st.warning('Please Fill all details', icon="⚠️")
