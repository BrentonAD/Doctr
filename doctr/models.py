import json
from boilerpy3 import extractors
from doctr.utils import document_extractive_summarisation, paragraph_extractive_summarisation, generate_audio_stream

class Document:
    
    extractor = extractors.DefaultExtractor()

    def __init__(self, url: str, client=None, speech_config=None):
        
        document = self.extractor.get_doc_from_url(url)

        self.title = document.title
        self.content_raw = document.content
        self.summary = document_extractive_summarisation(client, [self.content_raw])
        self.paragraphs = self.generate_paragraphs(client, document)
        self.audio_stream = generate_audio_stream(speech_config, self.content_raw)

    def generate_paragraphs(self, client, document):
        text_blocks = [ block.text for block in document.text_blocks if block.is_content == True ]
        paragraphs_raw = [ {'id': idx, 'text_raw': paragraph_raw} for idx, paragraph_raw in enumerate(text_blocks) ]
        paragraphs_sorted = sorted(paragraphs_raw, key=lambda x: len(x['text_raw']), reverse=True)

        if client:
            paragraphs = paragraph_extractive_summarisation(paragraphs_sorted, client)
        else:
            paragraphs = paragraphs_sorted

        return [ Paragraph(paragraph_dict) for paragraph_dict in paragraphs ]
    
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Paragraph:
    def __init__(self, paragraph_object):
        self.id = paragraph_object['id']
        self.text_raw = paragraph_object['text_raw']
        self.summary = paragraph_object.get('summary')
        self.key_phrases = paragraph_object.get('key_phrases')