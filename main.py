import streamlit as st
import pandas as pd
from apis import baidu,youdao,google
import csv
from st_aggrid import AgGrid
import matplotlib.pyplot as plt
from data_analys import fanyi_language_count, centext_ltp, pos_radar, ner_radar
from annotated_text import annotated_text
import json
from init_nlp_json import pos,ner


# 使用streamlit搭建科学数据分析web界面
st.set_page_config(layout="centered", page_icon="🎓", page_title="翻译对比平台")
st.title("🎓 基于Python的翻译对比平台")

def sidebar():
    # 侧栏
    st.sidebar.title("💬 相关信息\n") #界面标题（侧栏）
    st.sidebar.markdown('#### 已实现翻译器：') # 界面文本内容（侧栏）
    st.sidebar.markdown('* 百度') # 界面文本内容（侧栏）
    st.sidebar.markdown('* 谷歌') # 界面文本内容（侧栏）
    st.sidebar.markdown('* 有道') # 界面文本内容（侧栏）
    st.sidebar.markdown('#### 已实现翻译的语言：') # 界面文本内容（侧栏）
    st.sidebar.markdown('* 英语') # 界面文本内容（侧栏）
    st.sidebar.markdown('* 汉语') # 界面文本内容（侧栏）
    st.sidebar.markdown('* 日语') # 界面文本内容（侧栏）
    st.sidebar.markdown('* 韩语') # 界面文本内容（侧栏）
    st.sidebar.markdown('#### 已实现自然语言处理的语言：') # 界面文本内容（侧栏）
    st.sidebar.markdown('* 汉语') # 界面文本内容（侧栏）

def analys():
    # 翻译功能
    # 构建翻译选择器字典
    dicts = {'百度': baidu, '有道': youdao, '谷歌': google}
    # 构建语百度翻译器语言字典
    baidu_language = {'英语':'en','汉语':'zh','日语':'jp','韩语':'kor'}
    # 构建语有道翻译器语言字典
    youdao_language = {'英语': 'en', '汉语': 'zh-CHS','日语':'ja','韩语':'ko'}
    # 构建语google翻译器语言字典
    google_language = {'英语': 'en', '汉语': 'zh-cn','日语':'ja','韩语':'ko'}

    # 生成可选语言类型
    languages = pd.DataFrame([key for key in baidu_language])

    # 构建语言选择器
    st.markdown('#### 选择目标语言：') # 语言器标题（主栏）
    option = st.selectbox('',languages)

    st.markdown('#### 输入文本：') # 输入文本框标题（主栏）
    # 构建输入文本框
    context = st.text_area('','',key='content')

    if context: # 判断文本框不为空时，进行自动化分析
        with st.spinner('wait for it...'):
            pos_dicts, ner_dicts = nlp(context)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown('##### 百度翻译结果：')
                # 返回百度翻译器分析结果
                baidu_result = st.text_area('',dicts['百度'](context,baidu_language[option]),key='baidu')
            with col2:
                st.markdown('##### 有道翻译结果：')
                # 返回有道翻译器分析结果
                youdao_result = st.text_area('',dicts['有道'](context,youdao_language[option]) ,key='youdao')
            with col3:
                st.markdown('##### 谷歌翻译结果：')
                # 返回google翻译器分析结果
                google_result = st.text_area('',dicts['谷歌'](context,google_language[option]),key='google')

            st.markdown('##### 选择合适的翻译引擎：')
            # 构建翻译结果字典，供用户选择
            results = {'百度':baidu_result,'有道':youdao_result,'谷歌':google_result}
            fanyi_apis = pd.DataFrame([key for key in results])

            # 结果选择器
            option2 = st.selectbox('',fanyi_apis)
            btn = st.button('确定')

        if btn: # 当用户选择结果后，记录用户选择
            with open('data.csv','a',newline='',encoding='utf-8') as f:
                # 使用csv文件对用户选择结果进行记录
                writer = csv.writer(f)
                # 通过追加方式，追加用户选择结果
                writer.writerow([option2,option,context,results[option2]])

            print(pos_dicts,ner_dicts)
            fanyi_lists = ['百度', '有道', '谷歌']
            # 通过追加方式，追加词性数量
            with open('nlp_analys/nlp_pos.json','r',encoding='utf-8') as f:
                results = json.load(f)
            index = fanyi_lists.index(option2)
            for key in results[index]:
                results[index][key] += pos_dicts[key]
            with open('nlp_analys/nlp_pos.json', 'w', encoding='utf-8') as f:
                json.dump(results,f)

            # 通过追加方式，追加实体数量
            with open('nlp_analys/nlp_ner.json','r',encoding='utf-8') as f:
                results = json.load(f)
            index = fanyi_lists.index(option2)
            for key in results[index]:
                results[index][key] += ner_dicts[key]
            with open('nlp_analys/nlp_ner.json', 'w', encoding='utf-8') as f:
                json.dump(results, f)

            st.success('成功添加')

def show():
    # 分析功能
    df = pd.read_csv('data.csv',encoding = 'utf-8')
    ### 读取记录的用户选择信息内容并显示
    with st.expander("显示用户选择信息"):
        AgGrid(df)

    ### 各翻译引擎翻译各语种数量柱状图
    with st.expander("显示各翻译引擎翻译各语种数量"):
        plt = fanyi_language_count(df)
        st.pyplot(plt)

    ### 各翻译引擎词性和实体类型能力图
    with st.expander("显示各翻译引擎能力图"):
        plt = pos_radar()
        st.pyplot(plt)
        plt = ner_radar()
        st.pyplot(plt)



def nlp(sents):
    # 自然语言处理功能
    # 例子：小明去深圳参加了一场腾讯会议
    # contexts.sent_split() 分句
    # ['小明去深圳参加了一场腾讯会议']
    # contexts.seg()[0]  分词
    # [['小明', '去', '深圳', '参加', '了', '一', '场', '腾讯会议']]
    # contexts.pos() 词性标注
    # [['nh', 'v', 'ns', 'v', 'u', 'm', 'q', 'n']]
    # contexts.ner() 命名实体识别
    # [[('Nh', 0, 0), ('Ns', 2, 2)]]
    contexts = centext_ltp([sents])
    pos_tags = {'a': '形容词', 'n': '名词', 'v': '动词', 'm': '量词', 'd': '副词', 'r': '代词'}
    ner_tags = {'Nh': '人名', 'Ni': '机构名', 'Ns': '地名'}
    pos_lists = []
    ner_lists = []
    ner_dicts = {"人名": 0, "机构名": 0, "地名": 0}
    pos_dicts = {"形容词": 0, "名词": 0, "动词": 0, "量词": 0, '代词': 0, '副词': 0}
    # 取分词、词性标注、命名实体识别结果进行拼接
    for segs, poss, ners in zip(contexts.seg()[0], contexts.pos(), contexts.ner()):
        # 组合词语与词性
        for seg, pos in zip(segs, poss):
            pos_lists.append((seg, pos_tags[pos]) if pos in pos_tags else seg)
            if pos in pos_tags: pos_dicts[pos_tags[pos]] += 1
        # 标注实体
        ner_segs = ['O'] * len(segs)
        for ner in ners:
            ner_segs[ner[1]] = ner[0]
            ner_dicts[ner_tags[ner[0]]] += 1
        # 组合词语与实体
        for seg, ner_seg in zip(segs, ner_segs):
            ner_lists.append((seg, ner_tags[ner_seg]) if ner_seg != 'O' else seg)

    with st.expander("显示自然语言分析结果"):
        st.markdown('##### 词性标注结果：')
        annotated_text(*pos_lists)
        st.markdown('##### 实体识别结果：')
        annotated_text(*ner_lists)

    return pos_dicts,ner_dicts


def main():
    sidebar()
    analys()
    show()

if __name__ == '__main__':
    # df = pd.read_csv('data.csv', encoding='utf-8')
    # 第一次启动时进行初始化
    # pos(df)
    # ner(df)
    # 启动
    main()


