import io
from PIL import Image
import pytesseract
import pandas as pd
import streamlit as st

def extract_text_from_image(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    image = Image.open(io.BytesIO(img_byte_arr))
    text = pytesseract.image_to_string(image)
    
    return text

def create_invoice_dataframe(text):
    lines = text.split("\n")
    invoice_number = "N/A"
    date_issued = "N/A"
    vendor = "N/A"
    description = "N/A"
    amount_due = "N/A"
    currency = "N/A"
    fx = "N/A"
    amount_lc = "N/A"
    tax = "N/A"
    
    for line in lines:
        if "Invoice" in line and "Date" not in line:
            invoice_number = line.split()[-1]
        elif "Invoice Date" in line:
            date_issued = line.split()[-1]
        elif "Vendor" in line:
            vendor = line.split("Vendor")[-1].strip()
        elif "Description" in line:
            description = line.split("Description")[-1].strip()
        elif "Amount Due" in line:
            amount_due = line.split("Amount Due")[-1].strip()
        elif "Tax" in line:
            tax = line.split("Tax")[-1].strip()
        elif "$" in line and "Total" in line:
            amount_lc = line.split("Total")[-1].strip()
    
    invoice_data = {
        "Invoice Number": invoice_number,
        "Date Issued": date_issued,
        "Vendor": vendor,
        "Description": description,
        "Amount Due": amount_due,
        "Tax": tax,
        "Currency": currency,
        "FX": fx,
        "Amount (LC)": amount_lc
    }
    
    df = pd.DataFrame([invoice_data])
    return df

def create_client_dataframe(text):
    lines = text.split("\n")
    client_number = "N/A"
    vendor = "N/A"
    contact_person = "N/A"
    contact_email = "N/A"
    address = "N/A"
    date_due = "N/A"
    
    for line in lines:
        if "Client Number" in line:
            client_number = line.split("Client Number")[-1].strip()
        elif "Vendor" in line:
            vendor = line.split("Vendor")[-1].strip()
        elif "Contact Person" in line:
            contact_person = line.split("Contact Person")[-1].strip()
        elif "Contact E-mail" in line:
            contact_email = line.split("Contact E-mail")[-1].strip()
        elif "Address" in line:
            address = line.split("Address")[-1].strip()
        elif "Date Due" in line:
            date_due = line.split("Date Due")[-1].strip()
    
    client_data = {
        "Client Number": client_number,
        "Vendor": vendor,
        "Contact Person": contact_person,
        "Contact E-mail": contact_email,
        "Address": address,
        "Date Due": date_due
    }
    
    df = pd.DataFrame([client_data])
    return df

def create_tax_dataframe(text):
    lines = text.split("\n")
    invoice_number = "N/A"
    date_issued = "N/A"
    vendor = "N/A"
    description = "N/A"
    tax = "N/A"
    currency = "N/A"
    fx = "N/A"
    amount_lc = "N/A"
    
    for line in lines:
        if "Invoice" in line and "Date" not in line:
            invoice_number = line.split()[-1]
        elif "Invoice Date" in line:
            date_issued = line.split()[-1]
        elif "Vendor" in line:
            vendor = line.split("Vendor")[-1].strip()
        elif "Description" in line:
            description = line.split("Description")[-1].strip()
        elif "Tax" in line:
            tax = line.split("Tax")[-1].strip()
        elif "$" in line and "Total" in line:
            amount_lc = line.split("Total")[-1].strip()
    
    tax_data = {
        "Invoice Number": invoice_number,
        "Date Issued": date_issued,
        "Vendor": vendor,
        "Description": description,
        "Tax": tax,
        "Currency": currency,
        "FX": fx,
        "Amount (LC)": amount_lc
    }
    
    df = pd.DataFrame([tax_data])
    return df

# Streamlit app
st.title('Invoice Data Extractor')

uploaded_file = st.file_uploader("Choose an invoice image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Display the uploaded image
    st.image(image, caption='Uploaded Invoice Image', use_container_width=True)
    
    extracted_text = extract_text_from_image(image)
    invoice_df = create_invoice_dataframe(extracted_text)
    client_df = create_client_dataframe(extracted_text)
    tax_df = create_tax_dataframe(extracted_text)
    
    # Display the extracted data in DataFrames
    st.subheader("Accounts Payable")
    st.write(invoice_df)
    st.subheader("Tax")
    st.write(tax_df)
    st.subheader("Customer List")
    st.write(client_df)

