import pyodbc
import os
from dotenv import load_dotenv
from datetime import datetime
from utils import credentials 
# load_dotenv()  # take environment variables from .env.

# main_user = os.getenv('user')
# main_password = os.getenv('password')

prod_user, prod_password = credentials.load_credentials(production = True)

def get_connection(user:str = prod_user,
                    password:str = prod_password, 
                    database:str = 'production', 
                    server:str = 'CISSQL-live01',
                    driver:str = '{SQL Server}'):
                    # driver:str = '{SQL Server Native Client 11.0}'):
    """
    This functions provides a secure connection to a database of interest within CISSQL-live01 server
    
    Args:
        user (str): username 
        password (str): password 
        database (str): Database of interest (set in production by default)
        server (str): Server to access (set in CISSQL-live01 by default)
        
    Returns
        Functioning conection to que database of interest with given credentials
    
    Example usage: 
        cnxn = get_connection(user = user,
                                    password = password, 
                                    database = 'production', 
                                    server = 'CISSQL-live01')
    
    """
    # Creating connection string 
    try: 
        cnxn_str = ("Driver="+driver+";"
                "Server="+server+";"
                "Database="+database+";"
                "UID="+str(user)+";"
                "PWD="+str(password)+";"
                "Trusted_connection=yes;")

        # Creating conection
        cnxn = pyodbc.connect(cnxn_str)
        create_at = datetime.today().strftime(format = '%Y-%m-%d at %H:%M:%S')
        print(f'[Info] Connection built successfully. Server: {server}, database: {database}. Created on {create_at}')
    
        return cnxn
    except Exception as e: 
        print(f"""[Info] Error while trying to build connection:
-----------------------------------------------------------------
{e}""")