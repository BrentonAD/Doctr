from flask import Flask

app = Flask(__name__)

from doctr.utils import authenticate_client
from config import endpoint, key

try:
    client = authenticate_client(key,endpoint)
except:
    client = None
