import pandas as pd
import json
from myapp.search.objects import Document, ResultItem
from pandas import json_normalize

_corpus = {}

def load_corpus(path) -> [Document]:
    """
    Load the corpus data from a JSON file and return a list of Document objects.
    """
    # Read all lines from the provided JSON file
    with open(path, encoding='utf-8') as fp:
        lines = fp.readlines()

    # Combine the lines into a single JSON string
    json_string = ''.join(lines)
    
    # Parse the JSON string into a Python object
    json_data = json.loads(json_string)

    # If the data is a list of tweets, normalize it directly
    if isinstance(json_data, list):
        df = json_normalize(json_data)  # Directly normalize the list of tweets
    else:
        # Handle the case where the JSON is not a list (if it's a dictionary, for example)
        print("Unexpected data format")
        return []

    # Ensure 'DocID' is used as a unique identifier for each tweet
    df['DocID'] = df.index.values

    # Apply the row-to-doc conversion function to populate the corpus
    df.apply(_row_to_doc_dict, axis=1)

    # Return the populated corpus
    return _corpus


def _row_to_doc_dict(row: pd.Series):
    """
    Convert a DataFrame row into a Document or ResultItem object and add it to _corpus.
    """
    # Create a Document object for the raw tweet data
    _corpus[row['DocID']] = Document(
        doc_id=row['DocID'],
        original_tweet=row['Original Tweet'], 
        tokenized_tweet=row['Tokenized Tweet'],
        date=row['Date'],  
        username=row['Username'],
        followers_count=row['FollowersCount'],  
        hashtags=row['Hashtags'],  
        likes=row['Likes'], 
        retweets=row['Retweets'],
        reply_count=row['ReplyCount'], 
        url=row['Url'] 
    )

    # If you want to create ResultItem objects, you can add a ranking value here
    ranking = 0  # Placeholder for ranking, could be calculated based on some criteria
    _corpus[row['DocID']] = ResultItem(
        doc_id=row['DocID'],
        original_tweet=row['Original Tweet'],
        tokenized_tweet=row['Tokenized Tweet'],
        date=row['Date'],
        username=row['Username'],
        followers_count=row['FollowersCount'],
        hashtags=row['Hashtags'],
        likes=row['Likes'],
        retweets=row['Retweets'],
        reply_count=row['ReplyCount'],
        url=row['Url'],
        ranking=ranking
    )


