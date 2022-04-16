from baidu_api import Baidu_Fanyi_Api
from youdao_api import Youdao_Fanyi_Api
from google_api import Google_fanyi_api

'''
构建翻译选择器
目前已完成的翻译器：
百度、有道、google
'''

def baidu(content='Please Input',dest='zh'):
    # 构建百度翻译器
    # 初始值：
    # 输入文本语言->自动检测
    # 翻译目标语言->中文
    api = Baidu_Fanyi_Api()
    return api.Make_request('auto',dest,content)

def youdao(content='Please Input',dest='zh-CHS'):
    # 构建有道翻译器
    # 初始值：
    # 输入文本语言->自动检测
    # 翻译目标语言->中文
    api = Youdao_Fanyi_Api()
    return api.Make_request('auto',dest,content)

def google(content='Please Input',dest='zh-cn'):
    # 构建google翻译器
    # 初始值：
    # 输入文本语言->自动检测
    # 翻译目标语言->中文
    return Google_fanyi_api('auto',dest,content)