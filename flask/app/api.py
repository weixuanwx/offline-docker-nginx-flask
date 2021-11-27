from app import app

from flask import Flask, request
import requests
import json

import pandas as pd
import numpy as np
from gensim.models import Word2Vec
import pymysql
import json
from sklearn.metrics.pairwise import cosine_similarity as cossim
from sklearn.feature_extraction.text import TfidfVectorizer
from fuzzywuzzy import fuzz

import sys
from nltk.corpus import stopwords

sys.path.append('./app')

# TODO
# Add your analytics methods here!
# Some example imports above (fuzzywuzzy, Word2Vec, nltk etc)


@app.route('/check_status')
def check_status():
    app.logger.info('My offline Flask API app is OK!')
    return 'API app is OK!'

# if __name__ == "__main__":
# application.run(host="0.0.0.0", debug=True, port=5000)
