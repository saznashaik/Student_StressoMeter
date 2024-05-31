import streamlit as st
import numpy as np
import pickle
import sqlite3
import sklearn
import pandas as pd
from PIL import Image

# Connect to SQLite database
conn = sqlite3.connect('stress_predictions_college.db')
cursor = conn.cursor()

# Create a sidebar with navigation options
menu = ["Home", "User input", "View Predictions", "For Queries"]
choice = st.sidebar.selectbox("Select a page", menu)

# Show the appropriate page based on the user's choice
if choice == "Home":
    st.markdown("<h2 style='color: BLACK;'>Welcome to Student Stress-O-Meter</h3>", unsafe_allow_html=True)
   
    # Set the background image
    def set_bg_hack_url():
        st.markdown(
            """
            <style>
            .stApp {
                background: rgba(255, 255, 255, 0.7) url("https://miro.medium.com/v2/resize:fit:1000/0*TcwJLbWDd-lNTcNq.jpg");
                background-size: 90% 90%;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    set_bg_hack_url()

if choice == "User input":
    def set_bg_hack_url():
        st.markdown(
            """
            <style>
            .stApp {
                background: rgba(255, 255, 255, 0.7) url("https://media.istockphoto.com/id/821760914/vector/pastel-multi-color-gradient-vector-background-simple-form-and-blend-with-copy-space.jpg?s=612x612&w=0&k=20&c=adwrMs3MkPLXMb69AYSoMpnCfLSAb_D3PCQRGGXiM5g=");
                background-size: COVER;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    set_bg_hack_url()
    st.markdown("<h1 style='color: red;'>Please enter input data for Stress Level Prediction</h1>", unsafe_allow_html=True)

    # Load the stress level prediction model
    with open("STUDENT_MENTAL_HEALTH (3).sav", "rb") as file:
      stress_model = pickle.load(file)
    course_mapping = {
        'ALA': 0, 'Accounting': 1, 'BCS': 2, 'BENL': 3, 'BIT': 4, 'Banking Studies': 5,
        'Biomedical Science': 6, 'Biotechnology': 7, 'Business Administration': 8, 'CTS': 9,
        'Communication': 10, 'Diploma Nursing': 11, 'Diploma TESL': 12, 'ENM': 13, 'Economics': 14,
        'Engineering': 15, 'Fiqh': 16, 'Fiqh Fatwa': 17, 'Human Resources': 18, 'Human Sciences': 19,
        'IRKHS': 20, 'IT': 21, 'Islamic Education': 22, 'KENMS': 23, 'KIRKHS': 24, 'KOE': 25,
        'KOP': 26, 'Law': 27, 'MALCOM': 28, 'MHSC': 29, 'Marine Science': 30, 'Mathematics': 31,
        'Nursing': 32, 'Psychology': 33, 'Radiography': 34, 'TAASL': 35, 'Usuluddin': 36
    }

    # Reverse mapping for displaying course names
    reverse_course_mapping = {v: k for k, v in course_mapping.items()}

    def stress_level_prediction(name, Register_Number, input_data):
        input_data_as_numpy_array = np.asarray(input_data)
        input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
        stress_prediction = stress_model.predict(input_data_reshaped)

        # Store the prediction in the database
        try:
            cursor.execute('''
                INSERT INTO stress_predictions_college
                VALUES (NULL, ?,?,?,?,?,?,?,?,?,?)
            ''', [name] + [Register_Number] + input_data + [stress_prediction[0]])
            conn.commit()  # Commit changes to the database
            st.write("Data successfully inserted into the database.")
        except Exception as e:
            st.error(f"Error inserting data into the database: {e}")

        st.write(f"Predicted Stress Level: {stress_prediction[0]}")

    def main():
        # Get input data from the user
        name = st.text_input("Enter name")
        Register_Number = st.text_input("Enter Register_number")
        course = st.selectbox("Course", list(course_mapping.keys()))
        year_of_study = st.number_input("Year of Study", min_value=0, max_value=4, value=1)
        cgpa = st.number_input("CGPA", min_value=0.0, max_value=4.0, value=3.245)
        marital_status = st.selectbox('marital_status', ['married', 'not married'])
        marital_status = 0 if marital_status == 'not married' else 1
        anxiety = st.selectbox('anxiety', ['more anxious', 'not more anxious'])
        anxiety = 0 if anxiety == 'not more anxious' else 1
        panic_attack = st.selectbox('panic attack', ['yes before', 'not before'])
        panic_attack = 0 if panic_attack == 'not before' else 1
        treatment = st.selectbox('treatment', ['taken before', 'not taken before'])
        treatment = 0 if treatment == 'not taken before' else 1

        user_data = {
            'Course': course_mapping[course],
            'Year of Study': year_of_study,
            'CGPA': cgpa,
            'Marital Status': marital_status,
            'Anxiety': anxiety,
            'Panic Attack': panic_attack,
            'Treatment': treatment
        }

        # Code for stress level prediction
        if st.button('Predict Stress Level'):
            stress_level_prediction(name, Register_Number, list(user_data.values()))

    if __name__ == '__main__':
        main()

if choice == "View Predictions":
    def set_bg_hack_url():
        st.markdown(
            """
            <style>
            .stApp {
                background: rgba(255, 255, 255, 0.7) url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQGMAaSD84amZhZtu76T0zjpeKVwAEioP7t_A&usqp=CAU");
                background-size: COVER;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    set_bg_hack_url()
    st.title("Predictions History")

    # Retrieve and display data from the database
    cursor.execute('SELECT * FROM stress_predictions_college ORDER BY "Predicted Stress Level" DESC')
    data = cursor.fetchall()

    # Display the stored data in a Streamlit table
    if data:
        columns = [
            'ID','name','Register_number','Course','Year of Study','CGPA','Marital Status','Anxiety','Panic Attack',
            'Treatment', 'Predicted Stress Level'
        ]
        df = pd.DataFrame(data, columns=columns)
        st.write('Predictions History:')
        st.write(df)
    else:
        st.write('No prediction records found.')

if choice == "For Queries":
    def set_bg_hack_url():
        st.markdown(
            """
            <style>
            .stApp {
                background: rgba(255, 255, 255, 0.7) url("https://png.pngitem.com/pimgs/s/367-3677729_thank-you-png-transparent-png.png");
                background-size: COVER;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    set_bg_hack_url()
    st.title("Contributors")
    st.write('Contact us at :')
    st.write('  saznashaik@gmail.com', type='mail')
    st.write('  harinirayala@gmail.com', type='mail')
    st.write('  maanasak@gmail.com', type='mail')
    st.write('  kavyavemuri@gmail.com', type='mail')
    st.write('  manjula143@gmail.com', type='mail')
    # image = Image.open('stress.jpeg')

# Close the database connection
conn.close()
