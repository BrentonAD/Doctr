from flask import Flask

app = Flask(__name__)

from doctr.utils import authenticate_client, initialise_speech_config
from config import endpoint, key, speech_endpoint, speech_key

client = authenticate_client(key,endpoint)
speech_config = initialise_speech_config(speech_key, speech_endpoint)

from doctr import endpoints

