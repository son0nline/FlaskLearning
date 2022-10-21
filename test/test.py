import os
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("DBCONNECT", "sqlServerConnectString"))
print(os.environ.get('DBCONNECT'))