
import datetime as dt
import pandas as pd
from utils.project_utils import custom_agg, extract_unique_and_count1, extract_unique_and_count2


def data_transformation_courses(dataframe: pd.DataFrame):
    """
    This function performs the data transformation required to the input data

    Args: 
        dataframe (pd.DataFrame): DataFrame containing data of interest to be transformed

    Returns: 
        dataframe (pd.DataFrame): Transformed data

    Example Usage:
        data_transformation_courses(dataframe = dataframe)
    """    

    # setting times and dates
    dataframe['start_time'] = dataframe['start_time'].dt.time
    dataframe['end_time'] = dataframe['end_time'].dt.time
    dataframe['start_date'] = dataframe['start_date'].dt.date
    dataframe['end_date'] = dataframe['end_date'].dt.date

    # copy the original dataframe
    dataframe_copy = dataframe.copy()

    # isolate the days portion
    dataframe_days = dataframe_copy[['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']]

    # reshape the dataframe
    dataframe_days = dataframe_days.reset_index().melt(id_vars='index', var_name='day', value_name='flag')

    # keep only the rows with 'Y'
    dataframe_days = dataframe_days[dataframe_days['flag'] == 'Y']

    # drop the 'flag' column as it's no longer needed
    dataframe_days = dataframe_days.drop(columns='flag')

    # merge the 'day' column back into the original dataframe
    dataframe = pd.merge(dataframe_copy, dataframe_days, left_index=True, right_on='index')

    # drop the original days columns
    dataframe = dataframe.drop(columns=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'index'])

    # column names and treatment to be given 
    dict_processes = {col: custom_agg if col in ['building', 'room'] else 'first' for col in dataframe.columns}

    # Group by 'course' and aggregate other columns using 'custom_agg' for 'room' column
    dataframe = dataframe.groupby('full_sec_name', as_index=False).agg(dict_processes)

    # Apply the function to each row
    dataframe[['building', 'section_deliveries']] = dataframe ['building'].apply(extract_unique_and_count1)
    dataframe[['room', 'section_deliveries']] = dataframe['room'].apply(extract_unique_and_count2)

    # cleaning course names 
    dataframe['title'] = dataframe['title'].str.replace('ý', ' ')
    
    # Compute occupation rate
    dataframe['occupation_rate'] = dataframe['student_count']/dataframe['capacity']

    # availability
    dataframe['available'] = dataframe['capacity'] - dataframe['student_count']
    
    # columns as integer
    int_columns = ['capacity','student_count','waitlisted','section_deliveries','available']
    dataframe[int_columns] = dataframe[int_columns].fillna(0).astype(int)

    # cleaning room 
    dataframe['room'] = dataframe['room'].str.replace(r'^,+$', '--').fillna('--')
    dataframe['room'] = dataframe['room'].str.replace(',', ', ')

    dataframe['gen_ed_flag'] = dataframe['section_no'].apply(lambda section: 'gen_ed' if section[0]=='G' else 'non_gen_ed')

    return dataframe;

def data_transformation_students(dataframe = pd.DataFrame):
    """
    This function performs the data transformation required to the input student data
    
    Args: 
        dataframe (pd.DataFrame): DataFrame containing data of interest to be transformed

    Returns: 
        dataframe (pd.DataFrame): Transformed data

    Example Usage:
        data_transformation_students(dataframe = dataframe)
    """
    
    dataframe['AAL'] = dataframe['AAL'].astype(str)
    dataframe.loc[dataframe['current_load']=='T','current_load'] = 'T_'+dataframe.loc[dataframe['current_load']=='T','pay_filter']
    dataframe = dataframe.groupby(['program','AAL','current_load', 'acad_level']).count()['studentid'].to_frame().reset_index()
    
    return dataframe


def data_transformation_payments(dataframe: pd.DataFrame):
    """
    This function turns raw data pulled out of payments_query and arranges it flag students who have paid
    
    Args: 
        dataframe (pd.DataFrame): Dataframe with raw data of interest
    
    Retuns: 
        dataframe of students, program and payment flag
        
    Example usage: 
        data_transformation_payments(dataframe = dataframe)
    """
    # Setting aal to string and starting with0
    dataframe['aal'] = dataframe['aal'].astype(str).str.zfill(2)

    # Creating today's date
    date = dt.datetime.now().strftime("%Y/%m/%d")

    # flagging students with sponsorship
    cond = (pd.notnull(dataframe['sponsorship'])) 
    dataframe.loc[cond,'pay_filter']=dataframe.loc[cond,'sponsorship_applied'].apply(lambda x : 'paid' if x.strftime("%Y/%m/%d") < date else 0)

    # flagging students with RO flag (OSAP)
    dataframe.loc[dataframe['stnt'].str.contains("RO",na=False),'stnt_date'] = dataframe.loc[dataframe['stnt'].str.contains("RO",na=False),'stnt_date'].apply(lambda x:dt.datetime.strptime(x[0:19], "%Y-%m-%dT%H:%M:%S"))
    cond3 = (dataframe['stnt'].str.contains("RO",na=False)) 
    dataframe.loc[cond3,'pay_filter']=dataframe.loc[cond3,'stnt_date'].apply(lambda x : 'paid' if x.strftime("%Y/%m/%d")<= date else 0)

    # Flagging students who have paid at least 10 dollars
    dataframe.loc[dataframe['payment_amount']>=10,'pay_filter'] = 'paid'

    # flagging student who haven't paid, no waiver, no OSAP
    dataframe['pay_filter'] = dataframe['pay_filter'].fillna('no_paid')

    # keeping student_id and payment flag
    dataframe = dataframe.loc[dataframe['pay_filter']=='paid',['studentid','program','pay_filter']]
    dataframe = dataframe.drop_duplicates()
    
    return dataframe;