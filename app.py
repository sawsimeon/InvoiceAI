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
        elif "$" in line and "Total" in line:
            amount_lc = line.split("Total")[-1].strip()
    
    invoice_data = {
        "Invoice Number": invoice_number,
        "Date Issued": date_issued,
        "Vendor": vendor,
        "Description": description,
        "Amount Due": amount_due,
        "Currency": currency,
        "FX": fx,
        "Amount (LC)": amount_lc
    }
    
    df = pd.DataFrame([invoice_data])
    return df

# Streamlit app
st.title('Invoice Data Extractor')

uploaded_file = st.file_uploader("Choose an invoice image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Display the uploaded image
    st.image(image, caption='Uploaded Invoice Image', use_container_width=True)
    
    extracted_text = extract_text_from_image(image)
    df = create_invoice_dataframe(extracted_text)
    
    # Display the extracted data in a DataFrame
    st.write(df)
