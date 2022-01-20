from azure.ai.textanalytics import TextAnalyticsClient, ExtractSummaryAction, ExtractKeyPhrasesAction
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