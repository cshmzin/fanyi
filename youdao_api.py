import time
import uuid
import requests
import hashlib
import json

class Youdao_Fanyi_Api():
    def __init__(self):
        # 请在有道翻译接口申请自己的api_id和密钥。
        # https://ai.youdao.com/console/
        '''
        app_id:申请API的id号。
        miyao:申请API的密钥。
        salt:随机生成码，使用uuid生成随机字符串，保证请求的唯一性。
        header:request请求访问的头部
        '''
        self.app_id = '5ba7e71b21d70dd0'
        self.miyao = 'a7LfO3DdPy1HSP7he0u5I168AVyCpQKL'
        self.salt = str(uuid.uuid1())
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def truncate(self,q):
        '''
        进行内容长度截取，当输入文本长度大于20时，隔10个字符进行截取，并加入长度信息。
        :param q:输入的文本内容
        :return:长度截取后的文本内容
        '''
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

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
        data['from'] = from_language
        # key = to，value = 翻译的目标语言
        data['to'] = to_language
        # key = signType，value = 接口版本号v3
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        # key = curtime，value = 当前时间
        data['curtime'] = curtime
        # key = appkey，value = 申请API的id号
        data['appKey'] = self.app_id
        # key = q，value = 输入的文本内容
        data['q'] = content
        # key = salt，value = 随机生成码
        data['salt'] = self.salt
        # 构建sign，sign = appkey + content + salt + curtime + miyao
        x = self.app_id + self.truncate(content) + self.salt + curtime + self.miyao
        # 使用sha256，计算hash值
        data['sign'] = hashlib.sha256(x.encode('utf8')).hexdigest()

        url = 'https://openapi.youdao.com/api'
        # 使用post方法发起请求
        result = json.loads(requests.post(url,data=data,headers=self.headers).text)
        if 'translation' not in result: return ''
        # 返回结果
        return result['translation'][0]


if __name__ == '__main__':
    # 测试案例
    api = Youdao_Fanyi_Api()
    print(api.Make_request('auto','en','根据课题的研究背景，本系统主要分析流量中的HTTP协议，因此在对数据集的提取过程中，只需要提取HTTP流量作为数据集，并根据需要对HTTP请求头部进行字段的提取。'))





