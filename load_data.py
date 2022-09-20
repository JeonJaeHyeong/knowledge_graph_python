import os

def read_txt(name):
    data_dir = os.path.join('data', name)
    f = open(data_dir, 'r', encoding="utf8")
    contents = []
    while True:
        paragraph = f.readline()        #  newline을 하나의 문단 구분으로 봄
        lines = paragraph.split('. ')   # 같은 문단 내의 문장을 '.'을 기준으로 나눔
        if not paragraph: break
        contents.append(lines)
    f.close()
    return contents