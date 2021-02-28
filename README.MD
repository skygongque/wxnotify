# wxnotify

`wxnotify`是一个基于企业微信应用API的微信通知（使用企业微信的`微信插件`可以实现推送消息至微信）


# 配置
> 略复杂但是一次性的  
> 个人也可以注册企业微信，不认证有所限制但不影响消息推送

1. **注册企业微信**[企业微信官网](https://work.weixin.qq.com)

2. **创建应用** 注册成功后，点`管理企业`进入管理界面（企业微信后台），选择`应用管理`[应用管理界面](https://work.weixin.qq.com/wework_admin/frame#apps) → `自建` → `创建应用`
    应用名称和logo随意 可见范围选择公司名。
创建完成后进入应用详情页，可以得到应用ID( `AgentId` )形式如`1000002`，应用Secret( `CORPSECRET` )形式如`92XHnUVXQ***************6pwRiUgnTx1A`。  
点击`我的企业`最下方有企业ID(`CORPID`)形式如`wwfaa43666b1****`。
3. **关注微信插件** 在企业微信管理界面（企业微信后台） 点击`我的企业` -> `微信插件` [微信插件](https://work.weixin.qq.com/wework_admin/frame#profile/wxPlugin)


# 安装
```
pip install wxnotify
```
使用pip豆瓣源的建议使用如下语句
```
pip install wxnotify -i https://pypi.python.org/simple
```

# 示例
```
# 企业ID
CORPID = 'wwfaa43666b1****'
# 应用Secret
CORPSECRET = '92XHnUVXQ***************6pwRiUgnTx1A'
# 应用ID
AgentId = '1000002'

t = wxnotify.WxNotify(CORPID,CORPSECRET,AgentId)
res = t.send('this is a message')
print(res)
```