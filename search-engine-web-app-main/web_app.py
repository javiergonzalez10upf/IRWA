import os
from json import JSONEncoder
### WWUUU iria
# pip install httpagentparser
import httpagentparser  # for getting the user agent as json
import nltk
from flask import Flask, render_template, session, redirect, url_for
from flask import request

from myapp.analytics.analytics_data import AnalyticsData, ClickedDoc
from myapp.search.load_corpus import load_corpus
from myapp.search.objects import Document, StatsDocument
from myapp.search.search_engine import SearchEngine


# *** for using method to_json in objects ***
def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default

# end lines ***for using method to_json in objects ***

# instantiate the Flask application
app = Flask(__name__)

# random 'secret_key' is used for persisting data in secure cookie
app.secret_key = 'afgsreg86sr897b6st8b76va8er76fcs6g8d7'
# open browser dev tool to see the cookies
app.session_cookie_name = 'IRWA_SEARCH_ENGINE'



full_path = os.path.realpath(__file__) #get current path
path, filename = os.path.split(full_path)
file_path = path + "/processed_tweets.json"
corpus = load_corpus(file_path)
# instantiate our search engine
search_engine = SearchEngine(corpus=corpus)

# instantiate our in memory persistence
analytics_data = AnalyticsData()

'''# print("current dir", os.getcwd() + "\n")
# print("__file__", __file__ + "\n")
full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)
# print(path + ' --> ' + filename + "\n")
# load documents corpus into memory.
file_path = path + "/processed_tweets.json"'''

# Get the absolute path of the current script
full_path = os.path.realpath(__file__)
# Extract the directory and filename from the full path
path, filename = os.path.split(full_path)
# Construct the path to the 'processed_tweets.json' file in the same directory as 'my_app.py'
file_path = os.path.join(path, "processed_tweets.json")

# file_path = "../../tweets-data-who.json"
corpus = load_corpus(file_path)
#print("loaded corpus. first elem:", list(corpus.values())[0])


# Home URL "/"
@app.route('/')
def index():
    print("starting home url /...")

    # flask server creates a session by persisting a cookie in the user's browser.
    # the 'session' object keeps data between multiple requests
    session['some_var'] = "IRWA 2021 home"

    user_agent = request.headers.get('User-Agent')
    print("Raw user browser:", user_agent)

    user_ip = request.remote_addr
    agent = httpagentparser.detect(user_agent)

    print("Remote IP: {} - JSON user browser {}".format(user_ip, agent))

    print(session)

    return render_template('index.html', page_title="Welcome")


@app.route('/search', methods=['POST'])
def search_form_post():
    search_query = request.form['search-query']

    session['last_search_query'] = search_query

    analytics_data.save_query_terms(search_query)
    
    # Store the query_id in the session
    #session['last_search_query_id'] = search_id  # This is the key change

    results = search_engine.search(search_query, corpus=corpus) #search_id, corpus)

    found_count = len(results)
    session['last_found_count'] = found_count
    session['docs_ids'] = [result.doc_id for result in results]

    print(session)

    return render_template('results.html', results_list=results, page_title="Results", found_counter=found_count, search=search_query, docs_ids=session.get('docs_ids'))


@app.route('/doc_details', methods=['GET'])
def doc_details():
    clicked_doc_id = request.args.get("id")  # Tweet/doc ID
    search_query = session.get('last_search_query')  # Make sure to store this when the search is performed

    print(f"click in id={clicked_doc_id}")
    print(f"search_query={search_query}")

    # Find the document by iterating through the corpus list of Document objects
    doc = None
    for document in corpus:  # Assuming corpus is a list of Document objects
        if document.doc_id == clicked_doc_id:  # Access the doc_id attribute directly
            doc = document
            break  # Stop the loop once the document is found

    # If doc not found, handle the error or show a 404 page
    if not doc:
        return "Document not found", 404

    # Record the click in analytics
    if clicked_doc_id:
        analytics_data.record_click(search_query=search_query, doc_id=clicked_doc_id, ranking=1)
        print(f"fact_clicks count for id={clicked_doc_id}: {analytics_data.fact_clicks.get(clicked_doc_id, 0)}")

    # Retrieve the last search query from the session for the "Back to Search Results" link
    tweet_url = doc.url 
    # Return the document details page
    return redirect(tweet_url)
    #return render_template('doc_details.html', item=doc, search_query=search_query)

@app.route('/stats', methods=['GET'])
def stats():
    """
    Show simple statistics example. ### Replace with dashboard ###
    :return:
    """

    docs = []
    # ### Start replace with your code ###

    for doc_id in analytics_data.fact_clicks:
        row: Document = corpus[int(doc_id)]
        count = analytics_data.fact_clicks[doc_id]
        doc = StatsDocument(row.id, row.title, row.description, row.doc_date, row.url, count)
        docs.append(doc)

    # simulate sort by ranking
    docs.sort(key=lambda doc: doc.count, reverse=True)
    return render_template('stats.html', clicks_data=docs)
    # ### End replace with your code ###


import time
from datetime import datetime
import httpagentparser
import geocoder  # to fetch country from IP (you may need to install the geocoder library)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    # Track the number of HTTP requests
    request_count = session.get('request_count', 0) + 1
    session['request_count'] = request_count

    # Track click data for documents
    visited_docs = []
    for doc_id in analytics_data.fact_clicks.keys():
        # Access the document in corpus using doc_id directly as a string key
        # Assuming corpus is a list of Document objects
        if doc_id.startswith('doc_'):  # Ensure doc_id format is correct
            # Find the document in the corpus list by matching doc_id
            d = next((doc for doc in corpus if doc.doc_id == doc_id), None)  # Get document by doc_id

            if d:  # Ensure the document exists
                doc_data = analytics_data.fact_clicks[doc_id]
                doc = ClickedDoc(doc_id, d.original_tweet, doc_data["click_count"], doc_data['search_queries'][-1], doc_data['rankings'][-1])  # Assuming description is original_tweet
                visited_docs.append(doc)

    # Sort documents by click count
    visited_docs.sort(key=lambda doc: doc.counter, reverse=True)

    # Track session data
    active_sessions = len(session)  # Example: Count the number of active sessions

    # Track query data: Number of unique terms, order of queries, etc.
    query_details = []
    unique_terms = set()
    for query in analytics_data.queries:
        query_terms = query['terms'].split()  # Split query terms
        query_hour = datetime.fromisoformat(query['timestamp']).strftime('%H')  # Hour of search
        query_details.append({
            'query': query['terms'],
            'term_count': len(query_terms),
            'hour': query_hour,
            #'query_id': query['query_id']
        })
        unique_terms.update(query_terms)

    # Track user context: browser, IP, etc.
    user_agent = request.headers.get('User-Agent')
    user_ip = request.remote_addr
    agent = httpagentparser.detect(user_agent)
    browser = agent.get('browser', 'Unknown')
    os = agent.get('os', 'Unknown')

    # Detect whether the device is a computer or mobile
    device_type = "Mobile" if "Mobile" in user_agent else "Desktop"

    # Fetch the country from the user's IP address
    location = geocoder.ip(user_ip)
    country = location.country if location else "Unknown"

    # Time of the day
    time_of_day = datetime.now().strftime('%H:%M:%S')

    # Pass all this data to the template
    return render_template('dashboard.html', 
                           visited_docs=visited_docs,
                           request_count=request_count,
                           active_sessions=active_sessions,
                           unique_terms=len(unique_terms),
                           query_details=query_details,
                           browser=browser,
                           os=os,
                           device_type=device_type,
                           country=country,
                           time_of_day=time_of_day,
                           user_ip=user_ip)



@app.route('/sentiment')
def sentiment_form():
    return render_template('sentiment.html')


@app.route('/sentiment', methods=['POST'])
def sentiment_form_post():
    text = request.form['text']
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    score = ((sid.polarity_scores(str(text)))['compound'])
    return render_template('sentiment.html', score=score)


if __name__ == "__main__":
    app.run(port=8088, host="0.0.0.0", threaded=False, debug=True)
