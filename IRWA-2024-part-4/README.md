# FINAL PROJECT PART 4

- **Mireia Pou Oliveras** (251725)  
- **Iria Quintero García** (254373)  
- **Javier González Otero** (243078)  

## Project Overview

The objective of this project is to develop a complete search engine, culminating in the creation of a user interface and the integration of web analytics. This final part focuses on user interaction and tracking mechanisms to analyze how users interact with the system.

## Project Structure

- **Part 1**: User Interface  
  - **1.1**: Search Page, Search Action, Search Function, and Search Algorithms  
  - **1.2**: Results Page and Document Details Page  

- **Part 2**: Web Analytics  
  - **2.1**: Data Collection  
  - **2.2**: Data Storage  
  - **2.3**: Analytics Dashboard  

## Important Notes

- **Execution Requirements**:  
  Ensure the search engine functionality from previous parts is fully implemented, as this part builds upon those features.  
- **Dependencies**:  
  The `web_app.py` and `dashboard.html` files require proper integration with the search engine's codebase, specifically for processing queries and displaying results.  

## Usage

To run the project, follow these steps:

1. Open a terminal and navigate to the project directory:  cd IRWA-2024-part-4

2. Execute the following command to start the web application:  python web_app.py

3. Once the application is running, open your web browser and go to the displayed URL (typically `http://127.0.0.1:5000`) to access the search engine interface.

4. Use the interface to perform searches, view results, and interact with the analytics dashboard.

## Detailed Explanation

### Part 1: User Interface

#### **1.1 Search Page, Action, Function, and Algorithms**
Created a web page with a search box to receive user queries. Modified the `search function` to call algorithms such as `search_tf_idf` for ranking results. Refactored classes in `objects.py` and adapted functions for indexing and ranking documents using a corpus.

#### **1.2 Results Page and Document Details Page**
Adapted the `results.html` file to display tweets with detailed metadata, including:  
- Tweet creation date, username, followers, likes, retweets, replies, and the original content summary.  

### Part 2: Web Analytics

#### **2.1 Data Collection**
Expanded the `AnalyticsClass` to track:  
- Search queries, document clicks, session details, and HTTP requests.  
- Stored analytics data in JSON format for easy visualization and storage.  

#### **2.2 Data Storage**
Integrated `AnalyticsData` in `web_app.py` to manage user interactions:  
- Logged search queries, session activities, and HTTP requests.  
- Recorded click data for analyzing user behavior and search relevance.  

#### **2.3 Analytics Dashboard**
Enhanced the `dashboard.html` file to visualize collected data, including:  
- Most popular queries, clicked documents, and request counts.  
- Applied styling to improve readability and user experience.  

## Final Remarks

This part of the project provides a functional interface and a robust analytics dashboard, enabling user-friendly search experiences and insights into user behavior.


