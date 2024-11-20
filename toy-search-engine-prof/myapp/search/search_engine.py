import random
from myapp.search.objects import ResultItem, Document


def build_demo_results(corpus: dict, search_id, search_query):
    """
    Build demo results for tweets based on the search query.
    :param corpus: Dictionary of Document objects (tweets) indexed by DocID
    :param search_id: Unique identifier for the search session
    :param search_query: The search term entered by the user
    :return: A list of ResultItem objects sorted by ranking
    """
    res = []
    size = len(corpus)

    ll = list(corpus.values())

    for index in range(random.randint(5, 15)):  # Limit results to 5-15 items for demo purposes
        item: Document = ll[random.randint(0, size - 1)]  # Get a random tweet

        # Check if the search query matches any token in the tokenized tweet
        if any(token.startswith(search_query.lower()) for token in item.tokenized_tweet):
            ranking = random.uniform(0, 1)  # Assign a random ranking for demo
            res.append(
                ResultItem(
                    doc_id=item.doc_id,
                    original_tweet=item.original_tweet,
                    tokenized_tweet=item.tokenized_tweet,
                    date=item.date,
                    username=item.username,
                    followers_count=item.followers_count,
                    hashtags=item.hashtags,
                    likes=item.likes,
                    retweets=item.retweets,
                    reply_count=item.reply_count,
                    url=item.url,
                    ranking=ranking
                )
            )

    # Simulate sort by ranking
    res.sort(key=lambda doc: doc.ranking, reverse=True)
    return res


class SearchEngine:
    """Educational search engine adapted for tweets."""

    def search(self, search_query, search_id, corpus):
        """
        Perform a search over the tweets corpus.
        :param search_query: The search query entered by the user
        :param search_id: Unique identifier for the search session
        :param corpus: Dictionary of Document objects (tweets) indexed by DocID
        :return: List of ranked ResultItem objects
        """
        print("Search query:", search_query)

        # For now, we're using the demo results builder
        results = build_demo_results(corpus, search_id, search_query)  

        return results
