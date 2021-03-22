from collections import Counter
import nltk
import pickle
import math


def search(query, dictionary, postings_file):
    """rank the list of document based on the query given

    Args:
        query (str): the query string to be ranked against
        dictionary (dictionary): dictionary of the posting lists
        postings_file (str): address to the posting file list

    Returns:
        str: search rank result
    """
    posting_file = open(postings_file, 'rb')

    # all tokenization should consistent with the one from index.py
    stemmer = nltk.stem.PorterStemmer()
    token_list = list(map(lambda x: stemmer.stem(x).lower(), query.split(" ")))
    query_counter = Counter(token_list)
    query_keys = list(query_counter.keys())

    query_length = 0
    query_term_vector = []

    # To get a faster quering, we precomute the value for tf_idf query vector
    # Next time, we only need to do dot product with each of the given document 
    for i in range(len(query_keys)):
        term = query_keys[i]
        tf_idf_score = 0

        # dictionary is in the form of:
        # dict = {
        #   "term1": (df1, pointer_to_posting_file),
        #   "term2": (df2, pointer_to_posting_file),
        #   ...
        # }
        #
        # posting_list is in the form of:
        # [(docID_1, tf1), (docID2, tf2), ...]
        if (term in dictionary):
            term_info = dictionary[term]
            term_df = term_info[0]
            term_pointer = term_info[1]
            no_of_document = len(dictionary["LENGTH"])

            posting_file.seek(term_pointer)
            posting_list = pickle.load(posting_file)

            tf_idf_score = (1 + math.log(query_counter[term], 10)) * math.log(no_of_document / term_df)
            query_length += (tf_idf_score ** 2)
        
        query_term_vector.append(tf_idf_score)

    normalize_denominator = math.sqrt(query_length)
    if (normalize_denominator != 0):
        # final precompute query vector
        query_term_vector = normalize_list(query_term_vector, normalize_denominator)


    # dictionary["LENGTH"] is the normalize denominator for a particular document_id which precomputed in index stage
    document_file_index = dictionary["LENGTH"].keys()   # get all document_id
    ranking_list = []

    for doc_id in document_file_index:
        doc_length = dictionary["LENGTH"][doc_id]
        document_term_vector = []

        for i in range(len(query_keys)):
            term = query_keys[i]
            tf_idf_score = 0
            
            if (term in dictionary):
                term_info = dictionary[term]
                term_pointer = term_info[1]
                
                posting_file.seek(term_pointer)
                posting_list = pickle.load(posting_file)
                
                term_freq = get_term_freq(doc_id, posting_list)
                
                if (term_freq != 0):
                    tf_idf_score = 1 + math.log(term_freq, 10)

            document_term_vector.append(tf_idf_score)
        
        if (doc_length != 0):
            # final computed document vector for a particular doc_id
            document_term_vector = normalize_list(document_term_vector, doc_length)
        
        # calculate cosine score
        score = sum([x * y for x, y in zip(query_term_vector, document_term_vector)])
        
        # cosine score == 0, skipped
        if (score == 0):
            continue

        # maintain the top k results and store it in ranking_list
        k = 10

        if (not ranking_list):
            ranking_list.append((score, doc_id))
        else:
            if (score > ranking_list[-1][0]):
                for x in range(len(ranking_list)):
                    if (ranking_list[x][0] < score):
                        ranking_list.insert(x, (score, doc_id))
                        break
                
                if (len(ranking_list) > k):
                    ranking_list = ranking_list[:k]
            else:
                if (len(ranking_list) < k):
                    ranking_list.append((score, doc_id))

    return " ".join([str(y) for x, y in ranking_list])


def normalize_list(lst, denominator):
    return list(map(lambda x: x/denominator, lst))


def get_term_freq(doc_id, term_pointer):
    # Example:
    #   term_pointer: [(1,2), (2,3), (4,6), ...]
    #   doc_id: 2
    #   return value: 3

    left = 0
    right = len(term_pointer) - 1

    while (left <= right):
        mid = (left + right) // 2
        
        if (term_pointer[mid][0] == doc_id):
            return term_pointer[mid][1]
        elif (term_pointer[mid][0] < doc_id):
            left = mid + 1
        else:
            right = mid - 1

    return 0