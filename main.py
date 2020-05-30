from Speech_Synthesis import *
from Sound_Recording import *
from xunfei import *
import xunfei
#唐诗宋诗数据库
from poem_data import *

from playsound import playsound
import os

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia

import re,sys,win32api,win32con

import threading

from PyQt5.QtCore import *

class Example(QThread):
    signal = pyqtSignal()    # 括号里填写信号传递的参数
    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        self.signal.emit()    # 发射信号
        
# 收到websocket连接建立的处理
def on_open(ws):
    def run(*args):
        frameSize = 8000  # 每一帧的音频大小
        intervel = 0.04  # 发送音频间隔(单位:s)
        status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧

        with open(wsParam.AudioFile, "rb") as fp:
            while True:
                buf = fp.read(frameSize)
                # 文件结束
                if not buf:
                    status = STATUS_LAST_FRAME
                # 第一帧处理
                # 发送第一帧音频，带business 参数
                # appid 必须带上，只需第一帧发送
                if status == STATUS_FIRST_FRAME:

                    d = {"common": wsParam.CommonArgs,
                         "business": wsParam.BusinessArgs,
                         "data": {"status": 0, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    d = json.dumps(d)
                    ws.send(d)
                    status = STATUS_CONTINUE_FRAME
                # 中间帧处理
                elif status == STATUS_CONTINUE_FRAME:
                    d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    ws.send(json.dumps(d))
                # 最后一帧处理
                elif status == STATUS_LAST_FRAME:
                    d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                  "audio": str(base64.b64encode(buf), 'utf-8'),
                                  "encoding": "raw"}}
                    ws.send(json.dumps(d))
                    time.sleep(1)
                    break
                # 模拟音频采样间隔
                time.sleep(intervel)
        ws.close()

    thread.start_new_thread(run, ())
 
    
def seach(strs): 
#--------------------------------唐诗------------------------------------------------#
    all_poem=[]
    a=tang_poem_selectParagraphs(strs)
    if a!=[]:
        for i in a:
            all_poem.append(i)
#------------------------------------------宋诗----------------------------------------#
    b=song_poem_selectParagraphs(strs)
    if b!=[]:
        for i in b:
            all_poem.append(i)
#--------------------------------------宋词------------------------------------------#
    c=ci_poem_selectParagraphs(strs)
    if c!=[]:
        for i in c:
            all_poem.append(i)
#——------------------------------------------整理------------------------------#            
    poemList=[]
    for i in all_poem:
        try:
            poemDict={}
            poemDict['poemName']=i[1]
            poemDict['author']=i[2]
            poemDict['poem']=i[4]
            poemList.append(poemDict)
        except:
            poemDict['poem']=i[3]
    return poemList

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 632)
        MainWindow.setStyleSheet("#MainWindow{border-image:url(2.jpg);}")
        #禁止放大
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height()) 
        #只显示关闭按钮
        MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(90, 10, 321, 51))
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setStyleSheet("font: 20pt \"Adobe 楷体 Std R\";\n"
"color: rgb(255, 0, 0);")
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(460, 50, 321, 51))
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setStyleSheet("font: 20pt \"Adobe 楷体 Std R\";\n"
"color: rgb(255, 0, 0);")
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(5, 371, 791, 141))
        self.textBrowser.setStyleSheet("background:transparent;\n"
"border:0px;border-bottom:1px solid #000")
        self.textBrowser.setObjectName("textBrowser")
        
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(360, 510, 70, 72))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet("QPushButton{border-image: url(2.png)}")
        self.pushButton.clicked.connect(self.fun)
        
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 0, 66, 66))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet("QPushButton{border-image: url(4.png)}")
        
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(720, 40, 66, 66))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setStyleSheet("QPushButton{border-image: url(3.png)}")
        
#         self.label = QtWidgets.QLabel(self.centralwidget)
#         self.label.setGeometry(QtCore.QRect(360, 0, 91, 31))
#         self.label.setObjectName("label")
#         self.label_2 = QtWidgets.QLabel(self.centralwidget)
#         self.label_2.setGeometry(QtCore.QRect(360, 30, 91, 31))
#         self.label_2.setObjectName("label_2")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def hui_fu(self,result):
        global poem,strss
        strss=''
        if result!='':
            strs=result[:-1]
            a=seach(strs)
            if a!=[]:
                poem_list=re.split("，|。|!|？",a[0]['poem'])
                for i in range(len(poem_list)):
                    poem+='<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:18pt; color:#ff0000;">%s</span></p>'%poem_list[i]+'\n'
                    if strs in poem_list[i]:
                        index=i
                    else:
                        pass
#                         print("else"+str(index))
                next_index=index+1
                print(next_index)
                if poem_list[next_index]=='':
                    strss+='该句是最后一句哦！上一句是：%s'%poem_list[next_index-2]
                else:
                    strss+=poem_list[next_index]
            else:
                strss+='没有找到该诗哦！'
        else:
            strss+='你想说啥呢？再说一次吧！'
        self.label_5.setText("%s"%strss)
        self.textBrowser.setHtml("""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
    <html><head><meta name="qrichtext" content="1" /><style type="text/css">
    p, li { white-space: pre-wrap; }
    </style></head><body style=" font-family:'SimSun'; font-size:8pt; font-weight:400; font-style:normal;">%s</body></html>"""%poem)
        poem=''

    def play(self):
        """
        播放图灵机器人合成语音1.MP3
        """
        playsound("1.mp3")
    
    def fun(self):
        """
        录音
        参数 1 音频文件
        参数 2 录音时长 单位（秒）
        """
        win32api.MessageBox(0,'点击确定开始录音！', "提醒",win32con.MB_ICONWARNING)
        audio_record("yinping.wav", 4)
        self.thread = Example()
        self.thread.signal.connect(self.start)
        self.thread.start()    # 启动线程


    def start(self):
        global poem
        """
        讯飞音频识别
        APPID=ID, 
        APIKey=KEY,
        APISecret=Secret,
        AudioFile=音频文件
        全局变量result：拼接返回结果
        """
        time1 = datetime.now()
        websocket.enableTrace(False)
        wsUrl = wsParam.create_url()
        ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
        ws.on_open = on_open
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        time2 = datetime.now()
        print("录音音频识别结果："+xunfei.result)
        
        self.label_4.setText("%s"%xunfei.result)
        self.hui_fu(xunfei.result)
        xunfei.result=''
        """
        百度语音合成
        getBaiduVoice(参数)
        参数：图灵机器人回传字符串
        结果：合成音频文件1.MP3
        """
        getBaiduVoice(strss)
#         time.sleep(0.5)
        
        self.thread = Example()
        self.thread.signal.connect(self.play)
        self.thread.start()    # 启动线程
        print("-------------------")
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "诗一句"))
        MainWindow.setWindowIcon(QtGui.QIcon('5.png'))
        self.pushButton.setText(_translate("MainWindow", ""))
        
if __name__ == '__main__':
    wsParam = Ws_Param(APPID='5e0c3e6b', APIKey='04b5b1500b180d91c7450fc2e80ab325',APISecret='90983cd4da12416b457b7a65d41e8279',AudioFile=r'yinping.wav')
    global poem,strss
    poem=''
    strss=''
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
