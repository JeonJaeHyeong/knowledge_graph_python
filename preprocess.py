import load_data as ld
import numpy as np
import pandas as pd
from eunjeon import Mecab
from soynlp.normalizer import *
from sklearn.feature_extraction.text import CountVectorizer
import re   

def clean_text(paragraph):
    txt = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', ' ', paragraph)
    txt = only_text(txt)
    return txt

def get_nouns(paragraph):
    tagger = Mecab()
    nouns_list = tagger.nouns(paragraph)
    nouns_str = ' '.join(nouns_list)
    return nouns_str

def cal_tfidf(paragraphs):
    vectorizer = CountVectorizer()
    dtm = vectorizer.fit_transform(paragraphs)  # Document Term Matrix
    
    tf = pd.DataFrame(dtm.toarray(), columns = vectorizer.get_feature_names())  # Term Freqeuncy
    df = tf.astype(bool).sum(axis = 0)  # Document Frequency 

    D = len(tf)         # 문서 개수
    idf = np.log((D+1) / (df+1)) + 1    # Inverse Document Frequency
    
    # TF-IDF
    tfidf = tf * idf                      
    tfidf = tfidf / np.linalg.norm(tfidf, axis = 1, keepdims = True)
    
    # change the form of dataframe
    tfidf = tfidf.T
    tfidf.columns = ['tfidf']
    return tfidf.sort_values(by='tfidf')

def preprocessing(paragraphs):
    clean_paras = list(map(clean_text, paragraphs))
    nouns_paras = list(map(get_nouns, clean_paras)) 
    tfidf = cal_tfidf(nouns_paras)
    return nouns_paras, tfidf
    