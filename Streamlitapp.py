#importing necessary libraries
import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import re
import mysql.connector
import base64
import pandas as pd
#creating a streamlit app
def GUI():
    st.title('Business Card Extractor')
    st.write('Upload a business card image to extract information')
    tab1,tab2 = st.tabs(["Extracter", "Database"])

    with tab1:
        # File uploader widget
        uploaded_file = st.file_uploader('Upload Image', type=['png', 'jpg', 'jpeg'])
        
    

        if uploaded_file is not None:
            with open('image.png', 'wb') as f:
                f.write(uploaded_file.getvalue())
            # Display the uploaded image
            image = Image.open(uploaded_file)
            reader = easyocr.Reader(['en'], gpu = False) # this needs to run only once to load the model into memory
            # Extract information from the image using OCR
            extracted_info = extracter(np.array(image), reader)
            
        
            col1, col2 = st.columns(2)
            with col1:
                st.image(image, caption='Uploaded Image', use_column_width=True)
            with col2:
                st.header("Extracted Info")         
                #Displaying the extracted info
                col1, col2 = st.columns(2)
                with col1:
                    Name = st.text_input("Name",extracted_info["Name"], key = 1)
                    Company_Name = st.text_input("Company_name",extracted_info["Company_name"], key = 2)
                    Pincode = st.text_input("Pincode",extracted_info["Pin"], key = 3)
                    Email = st.text_input("Email",extracted_info["Email"], key = 4)
                with col2:
                    Designation = st.text_input("Designation",extracted_info["Designation"], key = 5)
                    Address = st.text_input("Address",extracted_info["Address"], key = 6)
                    Website = st.text_input("Website",extracted_info["Website"], key = 7)
                    Phone_No = st.text_input("Phone no",extracted_info["Phone no"],key = 8)

                with open ('image.png', 'rb') as image_file:
                    encodes_image = base64.b64encode(image_file.read())

                upload = st.button("Edit & Upload")
                #Uploading data to database
                if upload:
                    mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="kishore123",
                    database="businesscard"
                    )
                    mycursor = mydb.cursor()
                    insert_channel_query = """
                                INSERT INTO card_details (Name, Company_name,Pincode,Email,Designation,Address,Website,Phone_no,image)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    """
                    mycursor.execute(insert_channel_query, (Name, Company_Name, Pincode, Email, Designation, Address, Website, Phone_No, encodes_image
                                ))
                    mydb.commit()
                    mydb.close()
    #Database tab
    with tab2:
        database()
        col = st.text_input("Enter the match column")
        row = st.text_input("Enter the value")
        delete = st.button("delete")
        if delete:
            querry(col, row)
    
        
# Creating a extracter as a function
def extracter(file, reader):
    
    result = reader.readtext(file)

    data = []
    for i in result:
        data.append(i[1])
    EMAIL =""
    ph =[]
    WEB = ""
    Name = ""
    Designation = ""
    ids = []
    ADD = ""
    PIN = ""
    Company_name = ""
    # Creating regex to match the data
    for i, string in enumerate(data):
        if i == 0:
            Name = string.lower()
            ids.append(i)
        if i == 1:
            Designation = string.lower()
            ids.append(i)
        if re.search(r'@', string.lower()):
            EMAIL=string.lower()
            ids.append(i)
        if re.search(r'\+*\d{2,3}-\d{3,10}-\d{3,10}', string):
            ph.append(string)
            ids.append(i)
        if re.match(r"(?!.*@)(www|.*com$)", string.lower()):
            WEB= WEB + string.lower()
            ids.append(i)
        if re.match(r'\w[a-zA-z]* \d{6,7}|\d{6,7}', string):
           
            PIN= string
            result = re.findall(r'\d+', PIN)
            new_pin = result[0]
            ids.append(i)
        if re.match(r'^\d+\s.|st$' ,string.lower()):
            ADD = string
            ids.append(i)
    for j, string in enumerate(data):
        if j not in ids:
            if re.match(r'^(?!.*,)' ,string.lower()):
                Company_name = Company_name + " " +string
    # collecting all the data points under one variable
    details = {'Name':Name, "Designation":Designation, "Company_name" :  Company_name,
          "Address": (ADD + PIN) , "Pin": new_pin, "Website": WEB, "Email": EMAIL, "Phone no": ph}

    return details
# creating a function to show table in database tab
def database():
    mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="kishore123",
                    database="businesscard"
                    )
    mycursor = mydb.cursor()
    try:
        mycursor.execute("SELECT * FROM card_details")
        output = mycursor.fetchall()
        df = pd.DataFrame(output)
        title = [i[0] for i in mycursor.description]
        df.columns = title
        st.dataframe(df)
        mydb.commit()
        mydb.close()
    except:
        st.error("No Data Available")
#creating the function to delete the data from the table
def querry(col, row):
    st.write(input)
    mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="kishore123",
                    database="businesscard"
                    )
    mycursor = mydb.cursor()
    mycursor.execute("Delete from card_details where {} = '{}'". format(col,row))
    mydb.commit()
    mydb.close()
  
GUI()