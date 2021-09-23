import wxnotify

# 企业ID
CORPID = 'wwfaa********1ae5fd7'
# 应用Secret
CORPSECRET = '92XHn***************RiUgnTx1A'
AgentId = '1000002'

t = wxnotify.WxNotify(CORPID,CORPSECRET,AgentId,False) # 最后一个参数是否本地缓存access_token
res = t.send('this is a message 1241552')
print(res)

res = t.send_picture('example.png')
print(res)