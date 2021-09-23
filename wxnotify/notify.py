import requests
import json
import time
from functools import wraps


def cheak_access_token(f):
    """ 拦截需要access_token的函数添加access_token参数 """
    @wraps(f)
    def wrapper(*arg,**kwargs):
        if len(arg) < 3:
            assert isinstance(arg[0],WxNotify)
            result = f(*arg,arg[0].get_access_token(),**kwargs)
            return result
        else:
            raise
    return wrapper


class WxNotify:
    def __init__(self, corpid, corpsecret, agentid,is_store_access_token):
        """ 
        is_store_access_token    是否本地缓存 access_token 不缓存适合云函数等存储困难的场景使用
        """
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.is_store_access_token = is_store_access_token
        self.access_token = None
        self.access_start_time = None

    def __get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        params = {
            'corpid': self.corpid,
            'corpsecret': self.corpsecret
        }
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        resp_json = resp.json()
        if 'access_token' in resp_json.keys():
            return resp_json['access_token']
        else:
            raise Exception(
                'Please check if corpid and corpsecret are correct \n'+resp.text)

    def get_access_token(self):
        """ 
        启用本地缓存 access_token 的情况
        先从access_token.conf 获取
        计算是否过期，过期重新获取
        """

        if self.is_store_access_token:
            # 本地缓存的情况
            try:
                with open('access_token.conf', 'r') as f:
                    t, access_token = f.read().split()
            except:
                with open('access_token.conf', 'w') as f:
                    access_token = self.__get_access_token()
                    cur_time = time.time()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token
            else:
                cur_time = time.time()
                if 0 < cur_time - float(t) < 7200:#token的有效时间7200s
                    return access_token
                else:
                    with open('access_token.conf', 'w') as f:
                        access_token = self.__get_access_token()
                        f.write('\t'.join([str(cur_time), access_token]))
                        return access_token
        else:
            # 本地不缓存的情况
            if not self.access_token:
                # self存一份返回一份
                self.access_token = self.__get_access_token()
                self.access_start_time = time.time()
                return self.access_token
            else:
                cur_time = time.time()
                if 0 < cur_time - float(self.access_start_time) < 7200:#token的有效时间7200s
                    return self.access_token
                else:
                    self.access_token = self.__get_access_token()
                    self.access_start_time = time.time()
                    return self.access_token

    @cheak_access_token
    def upload_picture(self, pic_path,access_token): 
        # access_token = self.access_token if self.access_token else self.__get_access_token()
        url = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload'
        params = {
            'access_token':access_token,
            'type': 'image'
        }
        files = {
            'media': open(pic_path, 'rb')
        }
        resp = requests.post(url, params=params, files=files)
        resp.raise_for_status()
        return resp.json()["media_id"]

    @cheak_access_token
    def send_picture(self, pic_path,access_token):
        # access_token = self.access_token if self.access_token else self.__get_access_token()
        media_id = self.upload_picture(pic_path)
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='+ access_token
        payload = {
            "touser": "@all",
            "msgtype": "image",
            "agentid": self.agentid,
            "image": {
                "media_id": media_id
            },
            "safe": 0
        }
        resp = requests.post(url, data=json.dumps(payload))
        resp.raise_for_status()
        return resp.json()

    @cheak_access_token
    def send(self, text,access_token):
        """ 强行使用装饰器 """
        # access_token = self.get_access_token()
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='+ access_token
        payload = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": text
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        resp = requests.post(url, data=json.dumps(payload))
        resp.raise_for_status()
        return resp.json()


if __name__ == "__main__":
    # 企业ID
    CORPID = ''
    # 应用Secret
    CORPSECRET = ''
    AgentId = '1000002'
    wn = WxNotify(corpid=CORPID, corpsecret=CORPSECRET, agentid=AgentId,is_store_access_token=False)
    print(wn.send("test message"))
