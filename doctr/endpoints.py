from flask import render_template, jsonify, request, redirect

from doctr import app, client
from doctr.models import Document

# Endpoints

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    else:
        url = request.form['url']
        document = Document(url, client)
        # ensure paragraphs are in the right order
        document.paragraphs.sort(key=lambda x: x.id)
        return render_template('document_view.html', document=document)
