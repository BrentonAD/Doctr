from flask import render_template, send_file, request, after_this_request

from doctr import app, client, speech_config
from doctr.models import Document

import os

# Endpoints

@app.route("/", methods=["GET", "POST"])
def home():
    
    if request.method == "GET":
        return render_template("index.html")
    else:
        url = request.form['url']
        document = Document(url, client, speech_config)
        path = os.path.join("doctr","static","audio","tts_audio.wav")
        document.audio_stream.save_to_wav_file(path)

        # ensure paragraphs are in the right order
        document.paragraphs.sort(key=lambda x: x.id)
        return render_template('document_view.html', document=document)
