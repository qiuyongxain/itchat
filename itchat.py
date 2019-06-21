#!/usr/bin/python
# -*- coding: UTF-8 -*-
# pip install itchat
# https://github.com/littlecodersh/ItChat
import itchat, time, redis, sys
reload(sys)
sys.setdefaultencoding('utf8')
from itchat.content import *

r = redis.Redis()

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):

    result = itchat.search_friends() # 获取自己的信息
    if msg.FromUserName != result.UserName: # 自己的消息不发送给小冰
        r.set('fromuser',msg.fromUserName,10) # 保存最近一个发送人的id
        author = itchat.search_mps(name='小冰')[0] # 获取小冰的信息-需要先关注微软小冰公众号
        itchat.send( msg.text,toUserName=author.UserName) # 转发给小冰

@itchat.msg_register([PICTURE])
def download_files(msg):
    result = itchat.search_friends()
    if msg.FromUserName != result.UserName:
        msg.download(msg.fileName)
        author = itchat.search_mps(name='小冰')[0]
        itchat.send_image(msg.fileName, author.UserName)

@itchat.msg_register(TEXT, isMpChat=True)
def text_reply(msg):
    author = itchat.search_mps(name='小冰')[0]
    if msg.FromUserName == author.UserName:
      fromuser = r.get('fromuser')
      itchat.send(msg.text, toUserName=fromuser)

@itchat.msg_register([PICTURE, RECORDING], isMpChat=True)
def download_files(msg):
    author = itchat.search_mps(name='小冰')[0]
    if msg.FromUserName == author.UserName:
        msg.download(msg.fileName)
        fromuser = r.get('fromuser')
        if msg['MsgType'] == 3 or msg['MsgType'] == 47:  # picture
            itchat.send_image(msg.fileName, fromuser)
        elif msg['MsgType'] == 34: # voice
            itchat.send_video(msg.fileName, fromuser)

itchat.auto_login(True)
itchat.run(True)
