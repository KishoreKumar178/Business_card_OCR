# Business Card Extractor - Streamlit App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/streamlit/streamlit)

## Introduction
The "Business Card Extractor" is a Streamlit web application that allows users to upload an image of a business card and extract information from it using Optical Character Recognition (OCR). The extracted information is displayed to the user, and they have the option to edit and upload the extracted data to a MySQL database. The app also provides a database tab where users can view the data stored in the database and delete records based on specified conditions.

## How to Run the App
1. Make sure you have the necessary Python packages installed by running the following command:

   pip install -r requirements.txt

3. Ensure you have a MySQL database set up to store the extracted business card information. Modify the database connection details in the `streamlitapp.py` file to match your MySQL database credentials.

4. Run the Streamlit app by executing the following command in the terminal:

   streamlit run streamlitapp.py

5. The app will start running locally, and you can access it in your web browser at `http://localhost:8501`.

## How to Use the App
1. When you open the app in your web browser, you will see the "Business Card Extractor" title and a description asking you to upload a business card image to extract information.

2. Click on the "Extracter" tab to access the business card extraction section.

3. Upload an image of a business card using the "Upload Image" file uploader widget. Supported image formats are PNG, JPG, and JPEG.

4. The app will display the uploaded image and extract the information using OCR. Extracted information fields (Name, Company Name, Pincode, Email, Designation, Address, Website, and Phone Number) will be displayed as text inputs.

5. If the OCR doesn't correctly identify some information, you can manually edit the fields before proceeding.

6. Click on the "Edit & Upload" button to upload the extracted and edited data to the MySQL database. The data will be stored in the "card_details" table.

7. Switch to the "Database" tab to view the data stored in the database. The table will be displayed showing all the extracted business card information stored so far.

8. To delete a record from the database, enter the column name (`col`) and the value (`row`) you want to delete, then click the "Delete" button. The app will execute the delete query and remove the specified record from the database.

## Note
- Make sure you have proper OCR trained data if you encounter any issues with text extraction.
- Ensure your MySQL database is running and accessible with the provided credentials.
- The app currently only supports English text extraction. You can extend it to support other languages by modifying the `easyocr.Reader()` function parameters.
