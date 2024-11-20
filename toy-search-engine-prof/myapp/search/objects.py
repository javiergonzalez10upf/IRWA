import json

import json

class Document:
    """
    Represents a document (tweet) in the corpus.
    """

    def __init__(self, doc_id, original_tweet, tokenized_tweet, date, username, followers_count, hashtags, likes, retweets, reply_count, url):
        self.doc_id = doc_id 
        self.original_tweet = original_tweet 
        self.tokenized_tweet = tokenized_tweet 
        self.date = date  
        self.username = username  
        self.followers_count = followers_count 
        self.hashtags = hashtags  
        self.likes = likes
        self.retweets = retweets 
        self.reply_count = reply_count 
        self.url = url  

    def to_json(self):
        """
        Convert the Document object into a JSON-compatible dictionary.
        """
        return self.__dict__

    def __str__(self):
        """
        Return a JSON string representation of the Document object.
        """
        return json.dumps(self.__dict__)


class ResultItem:
    """
    Represents a ranked item (processed tweet) in the search results.
    """

    def __init__(self, doc_id, original_tweet, tokenized_tweet, date, username, followers_count, hashtags, likes, retweets, reply_count, url, ranking):
        self.doc_id = doc_id  
        self.original_tweet = original_tweet 
        self.tokenized_tweet = tokenized_tweet  
        self.date = date 
        self.username = username  
        self.followers_count = followers_count  
        self.hashtags = hashtags  
        self.likes = likes  
        self.retweets = retweets  
        self.reply_count = reply_count 
        self.url = url  
        self.ranking = ranking 

