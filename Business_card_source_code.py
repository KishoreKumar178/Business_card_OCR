import streamlit as st
import easyocr
import pymysql
from PIL import Image

#Connect to the SQLite database
conn = pymysql.connect(
        host='localhost',
        user='root', 
        password = "kishore123",
        db='businesscard'
        )
      
cur = conn.cursor()

# Create a table to store business card information
"""cur.execute('''CREATE TABLE business_cards
             id INT PRIMARY KEY AUTOINCREMENT,
              image BLOB,
              company_name TEXT,
              card_holder_name TEXT,
              designation TEXT,
              mobile_number TEXT,
              email_address TEXT,
              website_url TEXT,
              area TEXT,
              city TEXT,
              state TEXT,
              pin_code TEXT''')"""
conn.commit()

# Initialize the easyOCR reader
reader = easyocr.Reader(['en'])



# Function to extract information from the uploaded image using OCR
def extract_information(image):
    result = reader.readtext(image)
    extracted_info = {}

    # Extract relevant fields from the OCR result
    for line in result:
        text = line[1]
        if 'company' in text.lower():
            extracted_info['company_name'] = text
        elif 'name' in text.lower():
            extracted_info['card_holder_name'] = text
        elif 'designation' in text.lower():
            extracted_info['designation'] = text
        elif 'mobile' in text.lower():
            extracted_info['mobile_number'] = text
        elif 'email' in text.lower():
            extracted_info['email_address'] = text
        elif 'website' in text.lower():
            extracted_info['website_url'] = text
        elif 'area' in text.lower():
            extracted_info['area'] = text
        elif 'city' in text.lower():
            extracted_info['city'] = text
        elif 'state' in text.lower():
            extracted_info['state'] = text
        elif 'pin' in text.lower():
            extracted_info['pin_code'] = text

    return extracted_info

# Function to display the extracted information
def display_extracted_info(extracted_info):
    st.subheader('Extracted Information')
    for key, value in extracted_info.items():
        st.write(f'{key}: {value}')

# Function to save the extracted information and image to the database
def save_to_database(image, extracted_info):
    # Convert the image to bytes
    image_bytes = image.read()

    # Insert data into the database
    cur.execute('''INSERT INTO business_cards
                 (image, company_name, card_holder_name, designation, mobile_number, email_address,
                  website_url, area, city, state, pin_code)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (image_bytes, extracted_info.get('company_name'), extracted_info.get('card_holder_name'),
               extracted_info.get('designation'), extracted_info.get('mobile_number'), extracted_info.get('email_address'),
               extracted_info.get('website_url'), extracted_info.get('area'), extracted_info.get('city'),
               extracted_info.get('state'), extracted_info.get('pin_code')))
    conn.commit()
    st.success('Data saved successfully!')

# Streamlit application UI
st.title('Business Card Extractor')
st.write('Upload a business card image to extract information')

    # File uploader widget
uploaded_file = st.file_uploader('Upload Image', type=['png', 'jpg', 'jpeg'])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Extract information from the image using OCR
    extracted_info = extract_information(image)
    display_extracted_info(extracted_info)

    # Save the extracted information and image to the database
    save_to_database(uploaded_file, extracted_info)
