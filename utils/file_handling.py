# from office365.runtime.auth.authentication_context import AuthenticationContext
# from office365.sharepoint.client_context import ClientContext
# from office365.sharepoint.files.file import File

# from shareplum import Office365
# from shareplum import Site
# from shareplum.site import Version

# import pandas as pd
# import datetime as dt
# from pathlib import Path

# def exporting_files(dataframe_courses: pd.DataFrame, 
#                     dataframe_students: pd.DataFrame) -> None:
#     """
#     This function creates two files for the input dataframe. One containing a datetime mark (for tracking purposes)
#     and the other one containing the data that should be updated to Sharepoint. 

#     Args: 
#         dataframe_courses (pd.DataFrame): Dataframe with information about courses 
#         dataframe_students (pd.DataFrame): Dataframe with information about students 

#     Returns: 
#         None
        
#     Example Usage: 
#         exporting_files(dataframe_courses = dataframe_courses,
#                         dataframe_students = dataframe_students)

#     """
#     root_path = Path.cwd()/'reports'
#     # Creating file path if it does not exists
#     if not root_path.exists:
#         root_path.mkdir(parents=True, exists_ok=True)

#     # Creating tracking file (with time mark)
#     file_name_track = 'room_occupation_' + dt.datetime.now().strftime(format='%Y_%m_%d_at_%H_%M_%S')+'.xlsx'
#     file_path_track = root_path/file_name_track

#     # Creating Sharepoint file
#     file_name = 'room_occupation.xlsx'
#     file_path = root_path/file_name

#     # Exporting tracking file to local
#     with pd.ExcelWriter(file_path_track, engine='xlsxwriter') as writer:
#         dataframe_courses.to_excel(excel_writer=writer,
#                                    sheet_name='room_usage',
#                                    index=False)
        
#         dataframe_students.to_excel(excel_writer=writer,
#                                    sheet_name='students_registrations',
#                                    index=False)

#     # Exporting Sharepoint file to local
#     with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
#         dataframe_courses.to_excel(excel_writer=writer,
#                                    sheet_name='room_usage',
#                                    index=False)
        
#         dataframe_students.to_excel(excel_writer=writer,
#                                    sheet_name='students_registrations',
#                                    index=False)
#     return None;

# def sharepoint_upload(sharepoint_user, 
#                       sharepoint_password, 
#                       sharepoint_base_url,
#                       root, 
#                       report_name,
#                       file_name = 'room_occupation.xlsx'):
#     """
#     This function uploads a given file (excel) to a shared folder on Sharepoint

#     Args:
#         sharepoint_user (str): Sharepoint user
#         sharepoint_password (str): Sharepoint password
#         sharepoint_base_url (str): Sharepoing base url 
#         root (str): root path on local machine
#         report_name (str): report name 
#         file_name (str): file name to be given in sharepoing (set as 'room_occupation.xlsx' by default)

#     Returns: 
#         None
    
#     Example Usage: 
#         sharepoint_upload(sharepoint_user = sharepoint_user,
#                             sharepoint_password = sharepoint_password,
#                             sharepoint_base_url = sharepoint_base_url,
#                             root = root,
#                             report_name = report_name)


#     """
    
#     # Folder URL relative to the site URL where the file will beOLE DB or ODBC error: Exception from HRESULT: 0x80040E1D.
#     folder_url = 'Shared Documents/'

#     # Authenticate to SharePoint
#     auth_ctx = AuthenticationContext(sharepoint_base_url)
#     if auth_ctx.acquire_token_for_user(sharepoint_user, sharepoint_password):
#         client_ctx = ClientContext(sharepoint_base_url, auth_ctx)

#         # Get the target folder
#         target_folder = client_ctx.web.get_folder_by_server_relative_url(folder_url)

#         # Read file and upload
#         report_name = report_name+".xlsx"
#         file_path = Path(root / report_name)

#         with open(file_path, 'rb') as content_file:
#             file_content = content_file.read()
#         target_file = target_folder.upload_file(file_name, file_content)
#         client_ctx.execute_query()

#         # print(f"[Info] {file_name} successfully uploaded to SharePoint.")
#     else:
#         print(f"Failed to authenticate to SharePoint for user {sharepoint_user}.")

