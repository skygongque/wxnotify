import wxnotify

# 企业ID
CORPID = 'wwfaa4*******e5fd7'
# 应用Secret
CORPSECRET = '92XHn****************wRiUgnTx1A'
AgentId = '1000002'

t = wxnotify.WxNotify(CORPID,CORPSECRET,AgentId)
res = t.send('this is a message')
print(res)

res = t.send_picture('example.png')
print(res)