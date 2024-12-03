import json
import random
from datetime import datetime


class AnalyticsData:
    """
    An enhanced in-memory persistence object.
    Stores analytics tables for tracking website and search engine usage.
    """

    # Query-related statistics
    queries = []  # List of dictionaries storing query details

    # Click statistics: key = doc ID, value = dictionary with click metadata
    fact_clicks = {}

    # Session and user context: session ID as key
    sessions = {}

    # Log HTTP requests and metadata
    http_requests = []

    def save_query_terms(self, terms: str) -> int:
        """
        Save query terms with metadata like timestamp and term count.
        """
        #query_id = random.randint(0, 100000)
        self.queries.append({
            #"query_id": query_id,
            "terms": terms,
            "term_count": len(terms.split()),
            "timestamp": datetime.now().isoformat()
        })
        #return query_id
        

    def record_click(self, search_query: str, doc_id: str, ranking: int):
        """
        Save click details with associated query and ranking.
        """
        if doc_id not in self.fact_clicks:
            self.fact_clicks[doc_id] = {
                "click_count": 0,
                "last_clicked": None,
                "search_queries": [],
                "rankings": []
            }
        self.fact_clicks[doc_id]["click_count"] += 1
        self.fact_clicks[doc_id]["last_clicked"] = datetime.now().isoformat()
        self.fact_clicks[doc_id]["search_queries"].append(search_query)
        self.fact_clicks[doc_id]["rankings"].append(ranking)

    def log_http_request(self, ip: str, browser: str, os: str):
        """
        Log HTTP request details (IP, browser, OS).
        """
        self.http_requests.append({
            "ip": ip,
            "browser": browser,
            "os": os,
            "timestamp": datetime.now().isoformat()
        })

    def start_session(self, session_id: str, user_ip: str, user_agent: dict):
        """
        Start a new session with context details.
        """
        self.sessions[session_id] = {
            "start_time": datetime.now().isoformat(),
            "user_ip": user_ip,
            "user_agent": user_agent,
            "queries": [],
            "clicks": []
        }

    def record_session_activity(self, session_id: str, activity_type: str, activity_data: dict):
        """
        Record activity (queries or clicks) in a session.
        """
        if session_id in self.sessions:
            self.sessions[session_id][activity_type].append(activity_data)

    def to_json(self):
        """
        Convert the entire analytics data to JSON for storage or debugging.
        """
        return json.dumps({
            "queries": self.queries,
            "fact_clicks": self.fact_clicks,
            "sessions": self.sessions,
            "http_requests": self.http_requests
        }, indent=4)

    def __str__(self):
        """
        Pretty-print the analytics data.
        """
        return self.to_json()

class ClickedDoc:
    def __init__(self, doc_id, description, counter, queries, rankings):
        self.doc_id = doc_id
        self.description = description
        self.counter = counter
        self.queries = queries
        self.rankings = rankings

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)