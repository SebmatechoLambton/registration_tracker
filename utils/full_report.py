from pathlib import Path
import datetime as dt
import argparse
import utils
import time

def run_report():
	try:
		parser = argparse.ArgumentParser()
		# Add an argument via flag in CLI 
		parser.add_argument('--term', type=str, default = '2024S')
		args = parser.parse_args()
		term = args.term

		# Measuring time of execution
		start_time = time.perf_counter()

		# Creating connection
		cnxn = utils.get_connection()
	
		################ Extracting ################
		dataframe_rooms = utils.rooms_usage(term= term, 
                                        cnxn = cnxn)
		dataframe_students = utils.xstl_query_term(term= term, 
                                               cnxn = cnxn)
		dataframe_payments = utils.payments_query(term= term, 
                                               cnxn = cnxn)
		print(f'[Info] Data retrieved successfully')

		################ Transforming  ################
		dataframe_courses = utils.data_transformation_courses(dataframe = dataframe_rooms)
		dataframe_payments = utils.data_transformation_payments(dataframe = dataframe_payments)
	
		# Merging student data with payments data.  
		dataframe_students = dataframe_students.merge(dataframe_payments, on = ['studentid','program'], how = 'left')
		dataframe_students['pay_filter'] = dataframe_students['pay_filter'].fillna('no_paid')
    
		dataframe_students = utils.data_transformation_students(dataframe = dataframe_students)
    
		print(f'[Info] Data transformed successfully')

		################ Loading  ################

		# utils.exporting_files(dataframe_courses = dataframe_courses,
        #                   dataframe_students = dataframe_students)
		print(f'[Info] Data exported successfully')

		# sharepoint_user, sharepoint_password = utils.load_credentials(sharepoint = True)

		# utils.sharepoint_upload(sharepoint_user = sharepoint_user,
        #                     sharepoint_password = sharepoint_password,
        #                     sharepoint_base_url = 'https://mylambton.sharepoint.com/sites/Registrationreports/',
        #                     root = Path.cwd()/'reports',
        #                     report_name = 'room_occupation')
	
		print(f'[Info] Data update to sharepoint successfully')           
		end_time = time.perf_counter()
		total_time = end_time - start_time
    
		# print('We are done for the run! :) ')
		print(f'[Info] Ran on {dt.datetime.now().strftime(format = "%Y-%m-%d %H:%M:%S")}. Total execution time: {total_time:.2f} secs')
		print('-'*100)
	except: 
		None
		print('Something happened and the process failed')
	return None
