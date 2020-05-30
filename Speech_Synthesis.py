#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/12/27 19:38
# @Author  : Cxk
# @File    : Speech_Synthesis.py

from aip import AipSpeech
# import random
    
def getBaiduVoice(text):
    """ 你的 APPID AK SK """
    APP_ID = '18152818'
    API_KEY = '37cAjhZud9EdbxuixmMCk448'
    SECRET_KEY = 'rYmYBtNc17mKd96xamEOWXaaLtRL07MR'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    result = client.synthesis(text = text, options={'vol':5,'per':4})

    if not isinstance(result,dict):
#         i=random.randint(1,10) 
        with open('1.mp3','wb') as f:
            f.write(result)
#         return i
    else:
        print(result)
