"""
This file provides the main ingredients for the register of documents
and for markingn a document against a number of keywords.
"""

import os
import glob
from os.path import expanduser
import json
import hashlib
import tempfile
import subprocess
import re
import string
import pickle
from collections import Counter


def mark_corpus(corpus, keywords):
    """ This is where the marking algorithm is implemented.
    At the moment it is simply the sum of the occurences of the
    keywords in the document.
    """
    mark = 0
    for keyword in keywords:
        if keyword in corpus:
            mark += corpus[keyword]
    return(mark)


def file_to_corpus(file):
    """ This function takes a PDF file, extract the text,
    and collect a dictionary of words with the number of occurences.
    """
    from nltk.corpus import stopwords
    from nltk.tokenize import sent_tokenize, word_tokenize
    output = tempfile.NamedTemporaryFile()
    subprocess.call(["pdftotext", file, output.name])
    content = str(output.read().decode('unicode_escape')).lower()
    sentences = sent_tokenize(content)
    tokens = []
    for sentence in sentences:
        tokens += word_tokenize(sentence)
    corpus = Counter(tokens)
    keys = []
    for key in corpus:
        if len(key) == 1:
            keys.append(key)
        if corpus[key] == 1:
            keys.append(key)
        if key in stopwords.words('english'):
            keys.append(key)
        if any(i.isdigit() for i in key) :
            keys.append(key)
    for key in keys:
        del corpus[key]
    return(corpus)


def file_hash(name):
    hasher = hashlib.sha1()
    with open(name, "rb") as file:
        hasher.update(file.read())
    return(hasher.hexdigest())


class Register(object):
    """ This is the register of documents which can add new documents to
    its list. For each list we have a corpus of words and occurences.
    """
    def __init__(self, shelves, name):
        self.shelves = shelves
        self.name = expanduser(name)
        self.db = {}

    def write(self):
        with open(self.name, "wb") as file:
            pickle.dump(self.db, file)

    def read(self):
        if self.exists():
            with open(self.name, "rb") as file:
                self.db = pickle.load(file)

    def exists(self):
        return(os.path.exists(self.name))

    def update(self):
        """ This method scans each shelf and check if each document is 
        already in the register and hasn't changed (through a checksum).
        If needed a file is added or updated.
        """
        print("\nUpdating register of documents")
        for shelf in self.shelves:
            shelf_path = expanduser(shelf)
            print("Scanning " + shelf_path)
            pattern = expanduser(os.path.join(shelf_path, "*.pdf"))
            for file in glob.glob(pattern):
                if file in self.db:
                    if self.db[file][0] != file_hash(file):
                        print("Updating " + file)
                        corpus = file_to_corpus(file)
                        hash = file_hash(file)
                        self.db[file] = (hash, corpus)
                else:                    
                    print("Adding " + file)
                    corpus = file_to_corpus(file)
                    hash = file_hash(file)
                    self.db[file] = (hash, corpus)

    def rank_documents(self, keywords):
        """ To rank documents we mark each one individually and then
        order them based on their scores. The marks are scaled with 
        respect to the best document so that it has a mark of 1.
        """
        marks = []
        for key in self.db:
            mark = mark_corpus(self.db[key][1], keywords)
            marks.append([key, mark])
        marks.sort(key=lambda x: -x[1])
        if marks[0][1] == 0:
            return([])
        files = [(x[0], x[1]/marks[0][1]) for x in marks[0:5] if x[1]>0]
        return(files)


def read_config_file():
    name = os.path.join(expanduser("~"), '.ook')
    config = {}
    if os.path.exists(name):
        with open(name, "rb") as fp:
            config = json.load(fp)
    if "register" not in config:
        config["register"] = '~/.ook_register'
    return(config)
