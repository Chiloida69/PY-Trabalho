from dotenv import load_dotenv
import os
from supabase import create_client, Client

# Carrega as variáveis do arquivo .env
load_dotenv()

# Obtém a URL e a chave do Supabase das variáveis de ambiente
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Cria o cliente do Supabase  
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) 
    