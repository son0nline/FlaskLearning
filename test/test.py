import os
import secrets
import uuid

from dotenv import load_dotenv

load_dotenv()
print(os.getenv("DBCONNECT", "sqlServerConnectString"))
print(os.environ.get('DBCONNECT'))

print(uuid.uuid4())

print(str(secrets.SystemRandom().getrandbits(k=256)))