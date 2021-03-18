#!/usr/bin/python3
from ssl import DER_cert_to_PEM_cert
from spimi import count_word
from config import make_pointer

import re
import nltk
import sys
import getopt
import os
import pickle
import math
import shutil

def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")
    

# main function
def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    stemmer = nltk.stem.PorterStemmer()
    filename_list = []

    if (in_dir[-1] != '/'):
        in_dir += '/'
    for filename in os.listdir(in_dir):
        filename_list.append(int(filename))
    filename_list.sort()

    dictionary = {}
    dictionary['LENGTH'] = {}

    for filename in filename_list:
        document = open(in_dir + str(filename), 'r', encoding="utf8")
        document_text = document.read().splitlines()
        document.close()
        document_list = [nltk.tokenize.word_tokenize(text) for text in document_text]
        flattened_list = [text for ls in document_list for text in ls]
        token_list = list(map(lambda x: stemmer.stem(x).lower(), flattened_list))
        count_dict = count_word(token_list)

        length = 0
        for term, tf in count_dict.items():
            if term not in dictionary:
                dictionary[term] = (1, [(int(filename), tf)])
            else:
                df = dictionary[term][0] + 1
                posting_list = dictionary[term][1] + [(int(filename), tf)]
                dictionary[term] = (df, posting_list)
            length += (1 + math.log(tf, 10)) ** 2
        dictionary['LENGTH'][int(filename)] = length

    posting_file = open(out_postings, 'wb')
    dictionary_file = open(out_dict, 'wb')
    posting_file.truncate(0)
    dictionary_file.truncate(0)

    for term, value in dictionary.items():
        if term == 'LENGTH':
            continue
        df, posting_list = value
        pickle.dump(posting_list, posting_file)
        pointer = posting_file.tell()
        dictionary[term] = (df, pointer)
        
    pickle.dump(dictionary, dictionary_file)
    posting_file.close()
    dictionary_file.close()


input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

print("start indexing...")
build_index(input_directory, output_file_dictionary, output_file_postings)
