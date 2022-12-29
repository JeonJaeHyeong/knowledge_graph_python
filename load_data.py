import os

def read_txt(name):
    data_dir = os.path.join('data/txt', name)
    f = open(data_dir, 'r', encoding="utf8")
    paragraphs = f.readlines()        # newline을 하나의 문단 구분으로 봄
    f.close()
    return paragraphs

