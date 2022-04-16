import matplotlib.pyplot as plt
from ltp import LTP
import numpy as np
import pandas as pd
import json

class centext_ltp():
    def __init__(self,sents):
        '''
        自然语言处理类，用于实现各自然语言处理技术。
        :param sents: 输出句子
        '''
        self.ltp = LTP(path='pretrained_model') # 默认加载 Small 模型
        self.sents = sents
    def __len__(self):
        # 计算句子长度
        return len("".join(self.sents))
    def sent_split(self):
        # 句子分句
        return self.ltp.sent_split(self.sents)
    def seg(self):
        # 句子分词
        seg, hidden = self.ltp.seg([sent for sent in self.sent_split()])
        return seg, hidden
    def pos(self):
        # 词性标注
        seg, hidden = self.seg()
        return self.ltp.pos(hidden)
    def ner(self):
        # 命名实体识别
        seg, hidden = self.seg()
        return self.ltp.ner(hidden)

def fanyi_language_count(df):
    # 各翻译引擎翻译各语种数量柱状图构建
    plt.style.use('ggplot')
    plt.rcParams["font.sans-serif"] = ['SimHei']
    plt.rcParams["axes.unicode_minus"] = False
    fanyi_lists = ['百度', '有道', '谷歌']
    language_lists = ['汉语', '英语', '日语', '韩语']
    x_data = language_lists
    x_width = [i for i in range(len(x_data))]
    for fanyi_key in fanyi_lists:
        y_data = []
        for language_key in language_lists:
            # dataframe搜索目标语言
            df2 = df[df['目标语言'] == language_key]
            # dataframe搜索翻译引擎 count 计数函数
            y_data.append(df2[df2['用户选择的翻译引擎'] == fanyi_key]['翻译结果'].count())
        plt.bar(x_width, y_data, width=0.2, align='center', label=fanyi_key)
        x_width = [(i + 0.2) for i in x_width]
    plt.xticks([0.3, 1.3, 2.3, 3.3], x_data)
    plt.legend()
    return plt

def pos_radar():
    fanyi_lists = ['百度', '有道', '谷歌']
    with open('nlp_analys/nlp_pos.json','r',encoding='utf-8') as f:
        results = json.load(f)
    return radar('翻译引擎不同类型词性分析能力', fanyi_lists, results)

def ner_radar():
    fanyi_lists = ['百度', '有道', '谷歌']
    with open('nlp_analys/nlp_ner.json', 'r', encoding='utf-8') as f:
        results = json.load(f)
    return radar('翻译引擎不同类型实体分析能力', fanyi_lists, results)


def radar(title,fanyi_lists,results):
    '''
    构建雷达图
    :param title: 雷达图名称
    :param fanyi_lists: 翻译引擎
    :param results: 翻译引擎结果
    :return: 雷达图
    '''
    plt.style.use('ggplot')
    plt.rcParams["font.sans-serif"] = ['SimHei']
    plt.rcParams["axes.unicode_minus"] = False

    # pos_tags = {'a': '形容词', 'n': '名词', 'v': '动词', 'm': '量词', 'd': '副词', 'r': '代词'}
    # ner_tags = {'Nh': '人名', 'Ni': '机构名', 'Ns': '地名'}
    # results = [{"形容词": 87, "名词": 79, "动词": 95, "量词": 92,'代词':150,'副词':120}]

    max_length = max([r for result in results for r in result.values()])
    data_length = len(results[0])
    # 将极坐标根据数据长度进行等分
    angles = np.linspace(0, 2 * np.pi, data_length, endpoint=False)
    labels = [key for key in results[0].keys()]
    score = [[v for v in result.values()] for result in results]
    # 使雷达图数据封闭
    angles = np.concatenate((angles, [angles[0]]))
    labels = np.concatenate((labels, [labels[0]]))
    # 设置图形的大小
    fig = plt.figure(figsize=(8, 6), dpi=100)
    # 新建一个子图
    ax = plt.subplot(111, polar=True)
    # 绘制雷达图
    for s in score:
        score_a = np.concatenate((s, [s[0]]))
        ax.plot(angles, score_a)
    # 设置雷达图中每一项的标签显示
    ax.set_thetagrids(angles * 180 / np.pi, labels)
    # 设置雷达图的0度起始位置
    ax.set_theta_zero_location('N')
    # 设置雷达图的坐标刻度范围
    ax.set_rlim(0, max_length)
    # 设置雷达图的坐标值显示角度，相对于起始角度的偏移量
    ax.set_rlabel_position(270)
    ax.set_title(title)
    plt.legend(fanyi_lists, loc='best')
    return plt


if __name__ == '__main__':
    contexts = centext_ltp(["小明去深圳宝安区参加了一场腾讯会议","阿里巴巴公司正在进行裁员"])
    print(contexts.sent_split())
    print(contexts.seg()[0])
    print(contexts.pos())
    print(contexts.ner())
    print(len(contexts))
    pos_radar()
    ner_radar()


