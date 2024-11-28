import datetime
import json
from random import random

from faker import Faker

from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import re
import string
from array import array
import math
import numpy as np
from numpy import linalg as la
import collections
from collections import defaultdict
from myapp.search.objects import ResultItem, Document


fake = Faker()


# fake.date_between(start_date='today', end_date='+30d')
# fake.date_time_between(start_date='-30d', end_date='now')
#
# # Or if you need a more specific date boundaries, provide the start
# # and end dates explicitly.
# start_date = datetime.date(year=2015, month=1, day=1)
# fake.date_between(start_date=start_date, end_date='+30y')

def get_random_date():
    """Generate a random datetime between `start` and `end`"""
    return fake.date_time_between(start_date='-30d', end_date='now')


def get_random_date_in(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())), )


def load_json_file(path):
    """Load JSON content from file in 'path'

    Parameters:
    path (string): the file path

    Returns:
    JSON: a JSON object
    """

    # Load the file into a unique string
    with open(path) as fp:
        text_data = fp.readlines()[0]
    # Parse the string into a JSON object
    json_data = json.loads(text_data)
    return json_data


def build_terms(line):
    """
    Preprocess the text by removing stop words, stemming,
    transforming to lowercase, removing hashtags, and returning tokens.

    Argument:
    line -- string (text) to be preprocessed

    Returns:
    line - a list of tokens corresponding to the input text after the preprocessing
    """

    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))

    # Start preprocessing
    line = line.lower()  # Convert to lowercase

    #remove hashtags (before tokenization)
    line = re.sub(r'#\w+', '', line)

    line = re.sub(r'[^a-z0-9\s]', '', line)  # Remove every symbol that is not a letter or a number
    line = line.split()  # Tokenize the text to get a list of terms

    # Remove punctuation
    line = [word.translate(str.maketrans('', '', string.punctuation)) for word in line]
    line = [item for item in line if item not in stop_words]  # Remove stopwords
    line = [word for word in line if len(word) > 1]  # Remove single-letter words
    line = [stemmer.stem(word) for word in line]  # Stemming


    return line


def create_index_tfidf(corpus: dict):
    """
    Implement the inverted index and compute tf, df, and idf for a collection of tweets.

    Returns:
    index - the inverted index containing terms as keys and the corresponding
            list of documents these keys appear in (and the positions) as values.
    tf - normalized term frequency for each term in each document
    df - number of documents each term appears in
    idf - inverse document frequency of each term
    """

    index = defaultdict(list)
    tf = defaultdict(list)  # Term frequencies of terms in documents
    df = defaultdict(int)  # Document frequencies of terms in the corpus
    num_documents = len(corpus)  # Total number of documents (tweets)

    for document in corpus:
        doc_id = document.doc_id
        terms = document.tokenized_tweet  # List of terms (already tokenized)
        #print(document)

        ## Build the current tweet index for TF normalization and document frequency
        current_tweet_index = {}

        for position, term in enumerate(terms):  # Terms from the tokenized tweet
            if term not in current_tweet_index:
                current_tweet_index[term] = [doc_id, array('I', [position])] # this is an entry
            else:
                current_tweet_index[term][1].append(position)

        # Normalize term frequencies
        norm = 0
        for entry in current_tweet_index.values():
            norm += len(entry[1]) ** 2
        norm = math.sqrt(norm)

        # Calculate TF and DF weights
        for term, entry in current_tweet_index.items():
            tf[term].append(np.round(len(entry[1]) / norm, 4))  # TF calculation
            df[term] += 1  # Increment DF for current term

            # Merge the current tweet index with the main index
            index[term].append(entry)

    # Compute IDF following the formula
    idf = {}
    for term in df:
        idf[term] = np.round(np.log(float(num_documents) / df[term]), 4)

    return index, tf, df, idf


def rank_documents(terms, doc_ids, index, idf, tf, corpus):
    """
    Perform the ranking of the results of a search based on the tf-idf weights.

    Arguments:
    terms -- list of query terms
    doc_ids -- list of document IDs matching the query
    index -- inverted index data structure
    idf -- inverted document frequencies
    tf -- term frequencies
    corpus -- full list of Document objects

    Returns:
    A list of ranked documents as ResultItem instances.
    """
    # Build a map for quick lookup of Document objects by ID
    doc_map = {doc.doc_id: doc for doc in corpus}

    doc_vectors = defaultdict(lambda: [0] * len(terms))
    query_vector = [0] * len(terms)

    # Compute the norm for the query tf
    query_terms_count = collections.Counter(terms)
    query_norm = la.norm(list(query_terms_count.values()))

    for termIndex, term in enumerate(terms):
        if term not in index or term not in idf:
            continue  # Skip terms not in the index or idf dictionary

        # Compute tf*idf for the query
        query_vector[termIndex] = query_terms_count[term] / query_norm * idf.get(term, 0)

        # Generate document vectors for matching docs
        for doc_index, entry in enumerate(index[term]):
            doc_id, postings = entry

            if doc_id in doc_ids and term in tf:
                doc_vectors[doc_id][termIndex] = tf[term][doc_index] * idf[term]

    # Calculate the score of each document
    doc_scores = [[np.dot(curDocVec, query_vector), doc_id] for doc_id, curDocVec in doc_vectors.items()]
    doc_scores.sort(reverse=True)
    ranked_doc_ids = [x[1] for x in doc_scores]

    # Convert ranked document IDs to ResultItem instances
    result_items = []
    for doc_id in ranked_doc_ids:
        doc = doc_map.get(doc_id)
        if not doc:
            continue  # Skip if no matching Document found
        ranking = next(score[0] for score in doc_scores if score[1] == doc_id)
        result_items.append(ResultItem(
            doc.doc_id, doc.original_tweet, doc.tokenized_tweet, doc.date, doc.username,
            doc.followers_count, doc.hashtags, doc.likes, doc.retweets, doc.reply_count, doc.url, ranking
        ))

    return result_items



def search_tf_idf(query, index, corpus, idf, tf):
    """
    Output the list of documents that contain all of the query terms.

    Arguments:
    query -- search query string
    index -- inverted index data structure
    corpus -- full list of Document objects
    idf -- inverse document frequencies
    tf -- term frequencies

    Returns:
    A ranked list of ResultItem instances.
    """
    query = build_terms(query)
    result_docs = None  # Start with None to allow initialization by the first term
    for term in query:
        if term not in index:
            continue  # Skip terms not in the index
        term_docs = set(posting[0] for posting in index[term])

        if result_docs is None:
            result_docs = term_docs  # Initialize with the first term's docs
        else:
            result_docs = result_docs.intersection(term_docs)  # (AND operation)

    if not result_docs:  # Return an empty list if no documents match
        return []

    # Convert result_docs to a list if it's not empty
    result_docs = list(result_docs)

    # Rank the resulting documents
    ranked_docs = rank_documents(query, result_docs, index, idf, tf, corpus)

    return ranked_docs

