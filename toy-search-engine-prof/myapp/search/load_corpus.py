import pandas as pd
import json
from myapp.search.objects import Document, ResultItem
from pandas import json_normalize

_corpus = {}

def load_corpus(json_file):
    """
    Load a JSON file containing tweets and convert them into a list of Document objects.
    
    Args:
        json_file (str): Path to the JSON file.
    
    Returns:
        list[Document]: A list of Document objects.
    """
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)  # Load JSON content

    documents = []
    for item in data:
        # Create Document object from each JSON item
        doc = Document(
            doc_id=item['DocID'],
            original_tweet=item['Original Tweet'],
            tokenized_tweet=item['Tokenized Tweet'],
            date=item['Date'],
            username=item['Username'],
            followers_count=item['FollowersCount'],
            hashtags=item['Hashtags'],
            likes=item['Likes'],
            retweets=item['Retweets'],
            reply_count=item['ReplyCount'],
            url=item['Url']
        )
        documents.append(doc)

    return documents

