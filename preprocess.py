import load_data as ld
import numpy as np
import pandas as pd
from eunjeon import Mecab
from konlpy.tag import Komoran
from soynlp.normalizer import *
from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.feature_extraction.text import CountVectorizer
import re   

def clean_text(str):
    txt = re.sub('[-=+,#/\?:^@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', ' ', str)
    txt = only_text(txt)
    return txt

def get_stcs_tokens(ListOfSentence):
    return list(map(mecab_tokenize, ListOfSentence))

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

def mecab_tokenize(sent):
    mecab = Mecab()
    words = mecab.pos(sent)
    words = [w[0] for w in words if ('NNG' in w[1])]
    # XR : 어근, NNP : 고유명사, NNG : 보통명사, VA : 형용사
    return words


def cal_tfidf(tokens_paras):  # TF-IDF뿐만 아니라 textrank 등도 이용할 수 있도록
    paragraphs = list(map(lst2str, tokens_paras))
    vectorizer = TfidfVectorizer()
    dtm = vectorizer.fit_transform(paragraphs)  # Document Term Matrix

    return dtm


def preprocess_node(paragraphs):  # paragraphs : ["문단1", "문단2", ...]
    
    combine_para = ' '.join(paragraphs)
    
    clean_comb = clean_text(combine_para)
    tokens_comb = mecab_tokenize(clean_comb)

    return tokens_comb

def preprocess_edge(paragraphs):  # paragraphs : ["문단1", "문단2", ...]
    
    clean_paras = list(map(clean_text, paragraphs))     # [ [문단1], [문단2], ...]
    clean_stcs = list(map(para2stcs, clean_paras))      # [ [문단1의 문장1, 문단1의 문장2, ...], [문단2의 문장1, ...] , ...]

    tokens_paras = list(map(mecab_tokenize, clean_paras))     # [ [문단1의 명사들], [문단2의 명사들], ... ]
    tokens_stcs = list(map(get_stcs_tokens, clean_stcs))  # [ [ [문단1의 문장1의 명사들], [문단1의 문장2의 명사들], ...], []]

    return tokens_paras, tokens_stcs #dic_comb, dic_paras, dic_stcs
    