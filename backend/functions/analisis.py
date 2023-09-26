from supabase import create_client
from dotenv import load_dotenv
import os
import requests
from functions.querys_db import getCompanyConversation
load_dotenv()

url =os.environ.get("SUPABASE_URL")
key =os.environ.get("SUPABASE_KEY")
supabase=create_client(url,key)

def resumen_sencillo(company_name):
    conversaciones_json = getCompanyConversation(company_name)


# company_name="Branimax"
# resumen_sencillo(company_name)

