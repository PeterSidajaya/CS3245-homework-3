This is the README file for A0184586M and A0170766X submission
E0196721@u.nus.edu and E0313575@u.nus.edu

== Python Version ==

I'm (We're) using Python Version <3.8.7> for this assignment.

== General Notes about this assignment ==

INDEXING

The indexing process is contained in index.py, with spimi.py containing the helper functions.
First, we do word_tokenization, followed by removing punctuation (as suggested in the forum), then stem it.
The process continues by calculating the doc_freq of each term from the document list and save the postings list (doc ID, term freq) to postings.txt.
We also need to store information at indexing time about the document length, in order to do document normalization.

SEARCHING

The searching process is contained in search.py, with query.py containing the helper functions.
In the query process, our purpose is to calculate cosine score shown in the lecture that will help us rank
our list of documents. We gather the precomputed data from INDEXING to do our searching. First, we
calculate and precompute the tf_idf score for query list for faster multiplication later for cosine score. Next for
each query term t, we calculate the tf score of the possible document id, normalize it and store it in a dictionary. 
Finally we do cross multiplication between our query_vector with document_vector to yield our cosine score.
Maintain the top 10 score of the document_id for our final results.

== Files included with this submission ==

index.py  : main file for indexing
search.py : main file for searching
spimi.py  : file containing helper functions, mostly for index.py
query.py  : file containing helper functions, mostly for search.py

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I/We, A0184586M and A0170766X, certify that I/we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I/we
expressly vow that I/we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I/We, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason: -

We suggest that we should be graded as follows: -

== References ==

- CS3245 Piazza forum for comparing results of our search engine