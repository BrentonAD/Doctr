from azure.ai.textanalytics import TextAnalyticsClient, ExtractSummaryAction, ExtractKeyPhrasesAction
import azure.cognitiveservices.speech as speechsdk

from azure.core.credentials import AzureKeyCredential

# Authenticate the client using your key and endpoint 
def authenticate_client(key, endpoint):
    try:
        ta_credential = AzureKeyCredential(key)
        text_analytics_client = TextAnalyticsClient(
                endpoint=endpoint, 
                credential=ta_credential)
        return text_analytics_client
    except:
        return None

def initialise_speech_config(key, endpoint):
    try:
        speech_config = speechsdk.SpeechConfig(subscription=key, endpoint=endpoint)
        return speech_config
    except:
        return None

def document_extractive_summarisation(client, document_list):

    poller = client.begin_analyze_actions(
        document_list,
        actions=[
            ExtractSummaryAction(MaxSentenceCount=1, order_by='Rank')
        ],
    )

    document_results = poller.result()
    for result in document_results:
        # Extract first summary sentence
        extract_summary_result = result[0]  # first document, first result
        if extract_summary_result.is_error:
            # print("...Is an error with code '{}' and message '{}'".format(
            #     extract_summary_result.code, extract_summary_result.message
            # ))
            print(extract_summary_result)
            document_summary = "Could not generate summary"
        else:
            document_summary = extract_summary_result.sentences[0].text

    return document_summary

# Example method for summarizing text
def paragraph_extractive_summarisation(paragraphs_list, client):

    paragraph_text_list = [ paragraph['text_raw'] for paragraph in paragraphs_list ]

    poller = client.begin_analyze_actions(
        paragraph_text_list[:25],
        actions=[
            ExtractKeyPhrasesAction(),
            ExtractSummaryAction(MaxSentenceCount=1, order_by='Rank')
        ],
    )

    document_results = poller.result()
    for idx, result in enumerate(document_results):
        # Extract key phrases
        extract_keyphrase_result = result[0]
        if extract_keyphrase_result.is_error:
            # print("...Is an error with code '{}' and message '{}'".format(
            #     extract_keyphrase_result.code, extract_keyphrase_result.message
            # ))
            print(extract_keyphrase_result)
        else:
            paragraphs_list[idx]['key_phrases'] = extract_keyphrase_result.key_phrases
        
        # Extract first summary sentence
        extract_summary_result = result[1]  # first document, first result
        if extract_summary_result.is_error:
            # print("...Is an error with code '{}' and message '{}'".format(
            #     extract_summary_result.code, extract_summary_result.message
            # ))
            print(extract_summary_result)
        else:
            paragraphs_list[idx]['summary'] = extract_summary_result.sentences[0].text

    return paragraphs_list

def generate_audio_stream(speech_config, content):
    speech_config.speech_synthesis_language = "en-AU" # e.g. "de-DE"
    # The voice setting will overwrite language setting.
    # The voice setting will not overwrite the voice element in input SSML.
    speech_config.speech_synthesis_voice_name ="en-IE-EmilyNeural"

    #audio_config = speechsdk.audio.AudioOutputConfig(filename='./TestAudio.wav')
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = synthesizer.speak_text(content)
    stream = speechsdk.AudioDataStream(result)

    return stream
