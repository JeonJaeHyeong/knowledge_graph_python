import load_data as ld
import numpy as np
import pandas as pd
from eunjeon import Mecab
from konlpy.tag import Komoran
from soynlp.normalizer import *
from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.feature_extraction.text import CountVectorizer
import re   

stopwords = ['관련', '때']

def mecab_tokenize(sent):
    mecab = Mecab("C:\mecab\mecab-ko-dic") 
    # 여기서 mecab 경로 인식을 못할시 _mecab.py에서 Tagger('--rcfile %s' % dicpath)
    # 를 Tagger('-d %s' % dicpath) 로 바꾸어 주면 됨

    words = mecab.pos(sent)
    words = [w[0] for w in words if ('NNG' in w[1] or 'NNP' in w[1])]
    # XR : 어근, NNP : 고유명사, NNG : 보통명사, VA : 형용사
    return words

def clean_text(str):
    txt = re.sub('[-=+,#/\?:^@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', ' ', str)
    txt = only_text(txt)
    return txt

def clean_stopword(tokens):
    clean_tokens = []
    for token in tokens:
        if token not in stopwords:
            clean_tokens.append(token)
    return clean_tokens

def preprocessing(paragraph): # paragraph는 문서 하나

    clean_txt = clean_text(paragraph)
    clean_tokens = mecab_tokenize(clean_txt)
    clean_tokens = clean_stopword(clean_tokens)

    return clean_tokens # [토큰1, 토큰2, 토큰3, ...]
    

def stc_preprocessing(listOfstcs):
    return list(map(preprocessing, listOfstcs))

def para2stcs(paragraph):
    return paragraph.split('. ')

def lst2str(lst):
    return ' '.join(lst)


def preprocess_node(paragraphs):  # paragraphs : ["문서1", "문서2", ...]
    
    tokens_of_paras = list(map(preprocessing, paragraphs))
    return tokens_of_paras  # [ [문서1의 단어들], [문서2의 단어들], ... ]

def preprocess_edge(paragraphs):  # paragraphs : ["문서1", "문서2", ...]
    
    listOfsentences = list(map(para2stcs, paragraphs))      # [ [문서1의 문장1, 문서1의 문장2, ...], [문서2의 문장1, ...] , ...]
    clean_stc_tokens = list(map(stc_preprocessing, listOfsentences))

    return clean_stc_tokens


def make_dic_tfidf(list_of_wordlist):
    total_word_counts = dict()
    word_frequency = dict()
    for word_list in list_of_wordlist:
        word_counts = dict()
        for word in word_list:
            if word_counts.get(word, 0) == 0:
                word_frequency[word] = word_frequency.get(word, 0) + 1
            word_counts[word] = word_counts.get(word, 0) + 1    # 단어의 카운트 증가
        
        for item in word_counts.items():
            total_word_counts[item[0]] = total_word_counts.get(item[0], 0) + item[1]

    tfidfs = []
    for item in word_frequency.items():
        idf = np.log(len(list_of_wordlist) / (1 + item[1]))
        tf = total_word_counts[item[0]]
        tfidfs.append(tf * idf)

    tfidfs = np.array(tfidfs) 
    tfidfs = tfidfs / np.linalg.norm(tfidfs)
    for idx, item in enumerate(word_frequency.items()):
        total_word_counts[item[0]] = round(tfidfs[idx], 2)

    return total_word_counts

def make_dic_count(paragraphs):
    word_counts = dict()
    for word in paragraphs:
        word_counts[word] = word_counts.get(word, 0) + 1    # 단어의 카운트 증가

    return word_counts


def stcs_dic_count(ListOfSentence):
    return list(map(make_dic_count, ListOfSentence))
    