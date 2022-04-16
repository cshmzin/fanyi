import json
import pandas as pd
from data_analys import centext_ltp
import numpy as np

def pos(df):
    # 初始化 pos json 文件
    # 用于词性计数
    fanyi_lists = ['百度', '有道', '谷歌']
    pos_tags = {'a': '形容词', 'n': '名词', 'v': '动词', 'm': '量词', 'd': '副词', 'r': '代词'}
    results = []
    for fanyi_key in fanyi_lists:
        dicts = {"形容词": 0, "名词": 0, "动词": 0, "量词": 0, '代词': 0, '副词': 0}
        df2 = df[df['用户选择的翻译引擎'] == fanyi_key]['输入文本']
        lists = np.array(df2).tolist()
        context = centext_ltp(lists)
        poses = context.pos()
        for pos in poses:
            for p in pos:
                if p in pos_tags: dicts[pos_tags[p]] += 1
        results.append(dicts)
    with open('nlp_analys/nlp_pos.json','w',encoding='utf-8') as f:
        json.dump(results,f)

def ner(df):
    # 初始化 ner json 文件
    # 用于实体计数
    fanyi_lists = ['百度', '有道', '谷歌']
    ner_tags = {'Nh':'人名','Ni':'机构名','Ns':'地名'}
    results = []
    for fanyi_key in fanyi_lists:
        dicts = {"人名": 0, "机构名": 0, "地名": 0}
        df2 = df[df['用户选择的翻译引擎'] == fanyi_key]['输入文本']
        lists = np.array(df2).tolist()
        context = centext_ltp(lists)
        ners = context.ner()
        for ner in ners:
            for n in ner:
                dicts[ner_tags[n[0]]] += 1
        results.append(dicts)
    with open('nlp_analys/nlp_ner.json','w',encoding='utf-8') as f:
        json.dump(results,f)

if __name__ == '__main__':
    df = pd.read_csv('data.csv', encoding='utf-8')
    pos(df)
    ner(df)