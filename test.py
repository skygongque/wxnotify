import wxnotify

# 企业ID
CORPID = 'wwfaa43666b1****'
# 应用Secret
CORPSECRET = '92XHnUVXQ***************6pwRiUgnTx1A'
AgentId = '1000002'

t = wxnotify.WxNotify(CORPID,CORPSECRET,AgentId)
res = t.send('this is a message')
print(res)