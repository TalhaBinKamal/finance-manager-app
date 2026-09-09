import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

# Set up the page
st.set_page_config(page_title="Talha's Finance Manager", layout="wide")
st.title("💸 Finance Dashboard")

# Authenticate with Google Sheets
# We use Streamlit Secrets to safely store the JSON credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["gcp_service_account"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open the Google Sheet (Use the exact name of your live sheet)
sheet = client.open("Copy of Talha's Finance Manager").worksheet("Transactions")

# Fetch data and convert to Pandas DataFrame
data = sheet.get_all_records()
df = pd.DataFrame(data)

# Display the Data on the Web App
st.subheader("Recent Transactions")
st.dataframe(df)

# Add a form to input new transactions
st.subheader("Add a New Transaction")
with st.form("new_transaction"):
    col1, col2, col3 = st.columns(3)
    date = col1.date_input("Date")
    category = col2.text_input("Category (e.g., Salary, Electricity Bill)")
    amount = col3.number_input("Amount", min_value=0)
    
    col4, col5 = st.columns(2)
    reg_account = col4.selectbox("Type", ["Credit", "Debit"])
    notes = col5.text_input("Notes")
    
    submitted = st.form_submit_button("Add Transaction")
    
    if submitted:
        # Append the new row to the Google Sheet
        year = date.year
        month = date.strftime("%B")
        new_row = [category, amount, str(date), year, month, reg_account, notes]
        sheet.append_row(new_row)
        st.success("Transaction added successfully! Refresh the page to see updates.")
