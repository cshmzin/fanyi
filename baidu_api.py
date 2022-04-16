import uuid

import requests
import hashlib
import json

class Baidu_Fanyi_Api():
    def __init__(self):
        # 请在百度翻译接口申请自己的api_id和密钥。
        # https://api.fanyi.baidu.com/api/trans/product/desktop
        '''
        app_id:申请API的id号。
        miyao:申请API的密钥。
        salt:随机生成码，使用uuid生成随机字符串，保证请求的唯一性。
        header:request请求访问的头部
        '''
        self.app_id = '20220413001171280'
        self.miyao = 'xQvi_09Mr2NfIhn56yZJ'
        self.salt = str(uuid.uuid1())

    def Make_request(self,from_language,to_language,content):
        '''
        构建请求，并提交请求，使用POST方法。
        :param from_language: 输入的文本语言
        :param to_language: 翻译的目标语言
        :param content: 输入文本内容
        :return:
        '''
        # 初始化字典用于存储请求内容
        data = {}
        # key = from，value = 输入的文本语言
        data['q'] = content
        # key = from，value = 输入的文本语言
        data['from'] = from_language
        # key = to，value = 翻译的目标语言
        data['to'] = to_language
        # key = appkey，value = 申请API的id号
        data['appid'] = self.app_id
        # key = salt，value = 随机生成码
        data['salt'] = self.salt
        # 构建sign，sign = appkey + content + salt +  miyao
        x = self.app_id + content + self.salt + self.miyao
        # 使用md5，计算hash值
        data['sign'] = hashlib.md5(x.encode('utf8')).hexdigest()

        url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        result = json.loads(requests.post(url,data=data).text)
        if 'trans_result' not in result:return ''
        return result['trans_result'][0]['dst']


if __name__ == '__main__':
    api = Baidu_Fanyi_Api()
    print(api.Make_request('auto','en','对于HTTP流量头部的每个字段，我们需要对出现的每个关键词分配一个分数，要获取关键词，需要对字段进行分词处理，这里将通过空格，符号“/”，符号“，”，'))





