FINAL PROJECT PART 2 (README)

- Iria Quintero (254373)
- Javier González (243078)
- Mireia Pou (251725)

The objective of this project is to develop a search engine. In this second part, we focus on building an indexing system and evaluating the relevance of search results.


Project Structure

- Part 0: Imports and Drive setup
- Part 1.1: Text Preprocessing 
- Part 1.2: Further Data Analysis
- Part 2.1: Indexing
	2.1.1: Inverted Index
	2.1.2: Querying
	2.1.3: Ranking with TF-IDF
- Part 2.2: Evaluation
	2.2.1: Evaluation Functions
	2.2.2: Evaluation of Provided Queries
	2.2.3: Evaluation of Proposed Queries
	2.2.4: Two-dimensional Representation with T-SNE



Important Notes

- Execution Order: To execute this part, you must first run Part 1.1 to load and preprocess the data. Part 1.2 is not required for this section.
- Library Imports: Part 0 includes all necessary library imports. Ensure all required libraries are installed; use pip install if needed.
  
Detailed Explanation

- Part 0 initializes the libraries and connects to Google Drive.
  
- Part 1.1 loads the data directly from a specified ZIP path. Note: Ensure the dataset file path is updated accordingly.
  
- Part 1.2 expands on the analysis performed in Part 1, introducing new functions to extract deeper insights from the data and visualize key findings.

- Part 2.1 builds an inverted index to organize the document collection, allowing efficient retrieval of documents containing specific terms.

- Part 2.2 implements a function to search the inverted index, processing queries by identifying documents that contain all query terms (AND operation).




