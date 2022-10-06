import load_data as ld
import numpy as np
import pandas as pd
from eunjeon import Mecab
from soynlp.normalizer import *
from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.feature_extraction.text import CountVectorizer
import re   

def clean_text(str):
    txt = re.sub('[-=+,#/\?:^@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', ' ', str)
    txt = only_text(txt)
    return txt

def get_nouns(str):   # 형용사 등도 이용할 수 있도록
    tagger = Mecab()
    nouns_list = tagger.nouns(str)
    return [ noun for noun in nouns_list if len(noun) != 1 ]

def get_stcs_nouns(ListOfSentence):
    return list(map(get_nouns, ListOfSentence))

def make_dic_count(word_list):
    word_counts = dict()
    for word in word_list:
        word_counts[word] = word_counts.get(word, 0) + 1    # 단어의 카운트 증가
    return word_counts

def get_stcs_dic(ListOfSentence):
    return list(map(make_dic_count, ListOfSentence))
    

def para2stcs(paragraph):
    return paragraph.split('. ')

def lst2str(lst):
    return ' '.join(lst)

def cal_tfidf(nouns_paras):  # TF-IDF뿐만 아니라 textrank 등도 이용할 수 있도록
    paragraphs = list(map(lst2str, nouns_paras))
    vectorizer = TfidfVectorizer()
    dtm = vectorizer.fit_transform(paragraphs)  # Document Term Matrix

    return dtm


def preprocessing(paragraphs):  # paragraphs : ["문단1", "문단2", ...]
    
    combine_para = ' '.join(paragraphs)
    
    clean_comb = clean_text(combine_para)
    clean_paras = list(map(clean_text, paragraphs))     # [ [문단1], [문단2], ...]
    clean_stcs = list(map(para2stcs, clean_paras))      # [ [문단1의 문장1, 문단1의 문장2, ...], [문단2의 문장1, ...] , ...]

    nouns_comb = get_nouns(clean_comb)
    nouns_paras = list(map(get_nouns, clean_paras))     # [ [문단1의 명사들], [문단2의 명사들], ... ]
    nouns_stcs = list(map(get_stcs_nouns, clean_stcs))  # [ [ [문단1의 문장1의 명사들], [문단1의 문장2의 명사들], ...], []]

    dic_comb = make_dic_count(nouns_comb)
    dic_paras = list(map(make_dic_count, nouns_paras))
    dic_stcs = list(map(get_stcs_dic, nouns_stcs))
    return nouns_comb, nouns_paras, nouns_stcs #dic_comb, dic_paras, dic_stcs
    