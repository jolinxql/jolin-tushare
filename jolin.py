import tushare as ts
import itchat
from itchat.content import *
from math import floor
from random import randint
history={}

itchat.auto_login(hotReload=True)
juyingqun = [c['UserName'] for c in itchat.get_contact() if '巨婴' in c['NickName']][0]
xiawangye = [c['UserName'] for c in itchat.get_contact() if '夏王爷' in c['NickName']][0]
me = itchat.search_friends()['UserName']
print(me)
enable_autore=True

def auto_re(target_user):
    if randint(1,7)%7==0:
        news_id=randint(1,9)
        reply = "自动新闻彩蛋 %s"%ts.get_latest_news(top=news_id)['title'][news_id-1]
    else:
        reply = "自动回复: "+["你真棒!","真的嘛?","然后呢~"][floor(randint(0,2))]
    itchat.send(reply, target_user)
# 带对象参数注册，对应消息对象将调用该方法
@itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=True)
def text_reply1(msg):
    global enable_autore
    if msg['ToUserName'] == 'filehelper':
        if msg['Text'] == '自动回复':
            enable_autore=True
            return
        elif msg['Text'] == '关闭回复':
            enable_autore=False
            return
    if not enable_autore:
        return
    if msg['ToUserName'] == 'filehelper':
        auto_re('filehelper')
    if msg['FromUserName'] == juyingqun or msg['FromUserName'] == xiawangye:
        auto_re(msg['FromUserName'])
        history[(msg['FromUserName'],msg['MsgId'])] = msg['Text']
    # elif msg['FromUserName'] == me and (msg['ToUserName'] == juyingqun or msg['ToUserName'] == xiawangye):
    #     itchat.send('%s(自带回音' % (msg['Text']), msg['ToUserName'])


@itchat.msg_register(NOTE, isFriendChat=True, isGroupChat=True)
def text_reply3(msg):
    if msg['FromUserName'] == juyingqun or msg['FromUserName'] == xiawangye:
    #if msg['FromUserName'] == '@30e3567974bf2efcc308f406c43eb935':
        if msg['ActualUserName']!=me and '撤回' in msg['Text']:
            itchat.send('撤回的消息: %s' % (history[(msg['FromUserName'],msg['Content'][msg['Content'].find('<msgid>')+7:msg['Content'].find('</msgid')])]), msg['FromUserName'])

itchat.run()

#
# itchat.send('Hello, world', toUserName=juyingqun)
