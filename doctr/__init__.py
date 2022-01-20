from flask import Flask

app = Flask(__name__)

from doctr.utils import authenticate_client
from config import endpoint, key

client = authenticate_client(key,endpoint)

from doctr import endpoints

