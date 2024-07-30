import streamlit as st
import utils
import argparse
import pyodbc
import dotenv

def main():
    # Embedding the image at the top right corner
    image = 'img/lambton.jpg'  # Replace with the actual path to your image
    st.image(image, use_column_width=False, width=100, clamp=True)

    # Set the title and page layout
    st.title(f'Registration tracker')
    # st.set_page_config(layout="wide")
    term = st.selectbox(
    "What term would you like to see?",
    ('2022W','2022S','2022F',
     '2023W','2023S','2023F',
     '2024W','2024S','2024F'))

    

    def data_retrieval():
        # Creating connection
        cnxn = utils.get_connection()
        
        ################ Extracting ################
        dataframe_rooms = utils.rooms_usage(term= term, 
                                            cnxn = cnxn)
        dataframe_students = utils.xstl_query_term(term= term, 
                                                cnxn = cnxn)
        dataframe_payments = utils.payments_query(term= term, 
                                                cnxn = cnxn)
        return dataframe_rooms, dataframe_students, dataframe_payments
    
    dataframe_rooms, dataframe_students, dataframe_payments = data_retrieval()
     # Adding a refresh button
    if st.button("Refresh"):
        dataframe_rooms, dataframe_students, dataframe_payments = data_retrieval()

    ################ Transforming  ################
    dataframe_courses = utils.data_transformation_courses(dataframe = dataframe_rooms)

    dataframe_courses = dataframe_courses.drop(['subject','course_no','section_no'], axis = 1)
    dataframe_payments = utils.data_transformation_payments(dataframe = dataframe_payments)

    # Merging student data with payments data.  
    dataframe_students = dataframe_students.merge(dataframe_payments, 
                                                  on = ['studentid','program'], 
                                                  how = 'left')
    dataframe_students['pay_filter'] = dataframe_students['pay_filter'].fillna('no_paid')

    dataframe_students = utils.data_transformation_students(dataframe = dataframe_students)
    gen_ed = st.multiselect(
        "General Interest Courses",
        dataframe_courses['gen_ed_flag'].unique(),
        dataframe_courses['gen_ed_flag'].unique()
        )

   

    dataframe_courses = dataframe_courses[dataframe_courses['gen_ed_flag'].isin(gen_ed)]
    # st.dataframe(dataframe_courses)


    # Text input for the user to enter filtering text
    filter_text = st.text_input('Section Name (ex. ACC-2503)', '')

    # Filter the DataFrame based on the input text
    filtered_df = dataframe_courses[dataframe_courses['full_sec_name'].str.contains(filter_text, case=False, na=False)]
    st.dataframe(filtered_df)
if __name__ == "__main__":
    # Embedding the image at the top right corner
    image = 'img/lambton.jpg'  # Replace with the actual path to your image
    st.image(image, use_column_width=False, width=100, clamp=True)
    st.title('this is a test')
    # main()