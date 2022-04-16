# pip install googletrans==4.0.0rc1
from googletrans import Translator

# 构建google翻译器
translator = Translator(
    service_urls=['translate.google.cn'] # 输入google翻译网址：translate.google.cn
)
def Google_fanyi_api(src,dest,content):
    '''
    进行翻译操作
    :param src: 文本语言
    :param dest:  目标语言
    :param content: 输入文本内容
    :return:  翻译结果
    '''
    return translator.translate(content,dest=dest,src=src).text

if __name__ == '__main__':
    # 测试案例
    content = '对于HTTP流量头部的每个字段，我们需要对出现的每个关键词分配一个分数，要获取关键词，需要对字段进行分词处理，这里将通过空格，符号“/”，符号“，”，'
    print(Google_fanyi_api('auto','en',content))