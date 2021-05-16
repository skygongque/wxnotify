import requests
import json


class WxNotify:
    def __init__(self, corpid, corpsecret, agentid):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.access_token = self.__get_access_token(corpid, corpsecret)

    def __get_access_token(self, corpid, corpsecret):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        params = {
            'corpid': corpid,
            'corpsecret': corpsecret
        }
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        resp_json = resp.json()
        if 'access_token' in resp_json.keys():
            return resp_json['access_token']
        else:
            raise Exception(
                'Please check if corpid and corpsecret are correct \n'+resp.text)

    def upload_picture(self, pic_path):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload'
        params = {
            'access_token': self.access_token,
            'type': 'image'
        }
        files = {
            'media': open(pic_path, 'rb')
        }
        resp = requests.post(url, params=params, files=files)
        resp.raise_for_status()
        return resp.json()["media_id"]

    def send_picture(self, pic_path):
        media_id = self.upload_picture(pic_path)
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='+self.access_token
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


    def send(self, text):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='+self.access_token
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
    CORPID = 'wwfaa*********'
    CORPSECRET = '***********ZgYcf5QGUYLc5YK-********'
    AgentId = '******'
    wn = WxNotify(corpid=CORPID, corpsecret=CORPSECRET, agentid=AgentId)
    print(wn.send("test message"))
