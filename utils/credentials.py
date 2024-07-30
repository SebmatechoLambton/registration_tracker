from dotenv import load_dotenv
import os 
from pathlib import Path

def load_credentials(production:bool = False,
                     sharepoint:bool = False,
                     chatgpt: bool = False, 
                     snapshot:bool = False):
    """
    This function load credentials from .env file

    Args: 
        production (bool): credentials to access production (set as default False),
        sharepoint (bool): credentials to access sharepoint (set as default False),
        chatgpt (bool): credentials to use ChatGPT API (set as default False)
    
    Returns:
        dictionaries with credentials within. 

    Example usage:
       user, pass = utils.load_credentials()
        
    """
    # load_dotenv('C:/Users/c0846720/AppData/Roaming/Python/Python38/site-packages/python_utils/.env')  # take environment variables from .env.
    #load_dotenv('C:/Users/c0846720/OneDrive - Lambton College/Documents/python_utils/.env')
    load_dotenv()
    if production: 
        user = os.getenv('production_user')
        password = os.getenv('production_password')
        return user, password
    
    if sharepoint: 
        user = os.getenv('sharepoint_user')
        password = os.getenv('sharepoint_password')
        return user, password
    
    if chatgpt: 
        apikey =  os.getenv('chaggpt_key')
        return apikey
    
    if snapshot: 
        user = os.getenv('snapshots_user')
        password = os.getenv('snapshots_password')
        return user, password
    
    print('[Info] Credentials imported successfully')



