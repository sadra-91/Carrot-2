from PyQt6.QtWidgets import QApplication,QListWidget,QListWidgetItem,QSizePolicy,QScrollArea,QWidget,QMainWindow,QFrame,QVBoxLayout,QHBoxLayout,QLabel,QTextEdit,QLineEdit,QPushButton,QGraphicsDropShadowEffect,QMessageBox,QInputDialog,QProgressBar,QComboBox
from PyQt6.QtGui import QIcon,QColor,QFont,QPixmap,QLinearGradient,QBrush,QPainter,QClipboard,QRegion
from PyQt6.QtGui import QShortcut,QKeySequence
from PyQt6.QtCore import QSize,Qt,QTimer
from imagegeneration import ImageGenerator
from configparser import ConfigParser
from answer import aianswer
from functools import partial
from openai import OpenAI
from pathlib import Path
from request import Answer
import sys
import requests
import sqlite3
import json
import os
import re
import webbrowser
app=QApplication(sys.argv)
app.setStyleSheet("""
QToolTip {
    background-color:rgba(50,50,50,0.5);color: white;border:none;padding:5px;border-radius:4px;font-size:14px;
}
""")
config=ConfigParser()
class DStyledListWidget(QListWidget):
    def addStyledItem(self,text):
        pattern=r'\*(.*?)\*'
        styledtext=re.sub(pattern,r'<i style="color:gray;">\1</i>',text)
        item=QListWidgetItem(styledtext)
        self.addItem(item)
settings_filename="settings.json"
if not os.path.exists(settings_filename):
    with open(settings_filename,"w") as f:
        json.dump({"mode":0},f,indent=4)
with open(settings_filename,"r") as f:
    settingsfile=json.load(f)
b=settingsfile["mode"]%2
chatmode=0
charcount=0
crw=None
prlabel=None
progress=None
resw=None
crew=None
prow=None
relabel=None
alshow=False
charper=None
charname="Carrot"
charage=None
charhobbies=None
chochname="Carrot"
retext="aa"
modelname="llama3.1:8b"
replyyy=False
replyonid=None
window=QMainWindow()
window.showMaximized()
window.setWindowTitle("PF-Carrot")
window.setWindowIcon(QIcon("carrot.png"))
if(b==0):
    window.setStyleSheet("background-color:#00011a")
elif(b==1):
    window.setStyleSheet("background-color:white")
frame=QFrame(window)
frame.setFixedSize(1170,700)
frame.setStyleSheet("border-radius:20px;border-color:navy blue;border:1px white")
x=350
y=70
frame.move(x,y)
frame.show()
a=True
client=OpenAI(base_url="https://api.gapgpt.app/v1", api_key="sk-paxScEL4ymELOMpgkSugxIO2HF4ikzsoONDKX9Oc8JKUPW3B")
mc=1
currentchatid=None
if(chatmode==0):
    under=QWidget(window)
    under.resize(1000,78)
    under.move(522,705)
    if(b==0):
        under.setStyleSheet("border-radius:20px;border:1px solid gray;background-color:#00022E")
    else:
        under.setStyleSheet("border-radius:20px;border:2px solid black;background-color:#D3D3D3")
    under.show()
    textbar=QTextEdit(window)
    textbar.setPlaceholderText("write your message...")
    if(b==0):
        textbar.setStyleSheet("background-color:#1E2A56;border:1px solid gray;border-radius:15px;padding:5px;")
    else:
        textbar.setStyleSheet("background-color:#EAEAEA;color:black;border:2px solid black;border-radius:15px;padding:5px")
    textbar.move(570,725)
    textbar.resize(900,40)
    textbar.show()
    send=QPushButton(window)
    send.move(1472,722)
    if(b==0):
        send.setIcon(QIcon("send.png"))
    else:
        send.setIcon(QIcon("light-send.png"))
    send.setStyleSheet("background:none;background:transparent;padding:0px;border:1px solid gray;border-radius:20px")
    send.setIconSize(QSize(42,42))
    send.setFixedSize(42,42)
    send.show()
    messages=[]
    sendcount=0
    ml=DStyledListWidget(window)
    ml.setWordWrap(True)
    ml.resize(1000,655)
    ml.move(504,41)
    if(b==0):
        ml.setStyleSheet("background-color:#00011a;border:none;padding:8px;font-size:14px;color:white")
    else:
        ml.setStyleSheet("background-color:white;border:none;padding:5px;font-size:14px;color:black")
    ml.show()
    def selected(item):
        def copymessage(indexno):
            QApplication.clipboard().setText(item.text())
            item.setSelected(False)
            copied=QLabel("copied to clipboard",window)
            copied.resize(120,40)
            copied.setStyleSheet("background-color:rgba(50, 50, 50, 0.5);border-radius:15px")
            copied.move(800,window.height()-150)
            copied.setAlignment(Qt.AlignmentFlag.AlignCenter)
            copied.show()
            QTimer.singleShot(4000, copied.hide)
        def reply():
            global retext
            global relabel
            retext=item.text()
            item.setSelected(False)
            options.hide()
            relabel=QLabel("Replying to a message",window)
            relabel.resize(200,40)
            relabel.setStyleSheet("background-color:#1e2a56;border:1px solid gray;border-radius:20px;color:gray")
            relabel.move(1320,650)
            relabel.setFont(QFont("Calibri",13))
            relabel.show()
            global replyyy
            replyyy=True
        index=ml.row(item)
        if index%2==0:
            copymessage(False)
        else:
            options=QWidget(window)
            options.move(503,0)
            options.setStyleSheet("background-color:#1E2A56")
            options.resize(bar.width(),bar.height())
            options.show()
            co=QPushButton(options)
            co.move(70,10)
            co.resize(30,35)
            co.setStyleSheet("border:none")
            co.setIcon(QIcon("copyicon.png"))
            co.setIconSize(QSize(30,35))
            co.setToolTip("copy to clipboard")
            co.show()
            canceli=QPushButton(options)
            canceli.resize(30,30)
            canceli.move(985,10)
            canceli.setIcon(QIcon("canceli.png"))
            canceli.setIconSize(QSize(30,30))
            canceli.setToolTip("back")
            canceli.show()
            replyb=QPushButton(options)
            replyb.setIcon(QIcon("reply.png"))
            replyb.resize(32,32)
            replyb.setIconSize(QSize(25,25))
            replyb.move(22,10)
            replyb.setStyleSheet("border:none")
            replyb.setToolTip("reply to the message")
            replyb.show()
            ml.itemClicked.connect(options.hide)
            co.clicked.connect(lambda:copymessage(True))
            co.clicked.connect(options.hide)
            canceli.clicked.connect(options.hide)
            canceli.clicked.connect(lambda:item.setSelected(False))
            replyb.clicked.connect(reply)
        
    ml.itemClicked.connect(selected)
    itemfont=QFont("Candara",21)
    # itemfont.setBold(True)
    mhistory=[]
    def streaming(text):
        global charcount
        if charcount==0:
            timer.stop()
        charcount+=1
        crw.setText(f"Carrot:\n{text}")
    def extract(output):
        crw.setText(f"Carrot:\n{output}")
        mhistoryc=len(mhistory)
        if mhistoryc==90:
            del mhistory[0]
        #mhistory.append(f"user message(old):{text}")
        mhistory.append(f"assistant:{output}")
        conn=sqlite3.connect("appdatabase.db")
        cursor=conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        forchat INTEGER,
        role TEXT,
        message TEXT,
        date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        cursor.execute("""
        INSERT INTO messages(forchat,role,message)
        VALUES(?,?,?)
        """,
        (currentchatid,"user",text))
        cursor.execute("""
        INSERT INTO messages(forchat,role,message)
        VALUES(?,?,?)
        """,
        (currentchatid,"assistant",output))
        conn.commit()
        conn.close()
        # if(replyyy==True):
        #     reply.hide()
        #     replyyy=False
        send.setIcon(QIcon("send.png"))
        send.blockSignals(False)
    prof=QPushButton(window)
    prof.resize(42,42)
    prof.setStyleSheet("background:none;border:none")
    prof.move(1420,722)
    prof.setIcon(QIcon("download.png"))
    prof.setIconSize(QSize(42,42))
    prof.setToolTip("improve my prompt")
    def desfi(aaanswer):
        textbar.setPlainText(aaanswer)
        prof.blockSignals(False)
        print("khodafez")
        prof.setIcon(QIcon("download.png"))
    def imppro():
        print("salam")
        cee=textbar.toPlainText()
        prom="""
        you are an AI Prompt Designer. Rewrite the user's request into a clear, professional, and optimized prompt while preserving its intent.

        Rules:
        - Do not answer the request.
        - Respond with only the final prompt.
        """
        thread = Answer(cee, prom)
        thread.signals.finished.connect(desfi)
        thread.start()
        prof.blockSignals(True)
        prof.setIcon(QIcon("answering.png"))
    prof.clicked.connect(imppro)
    def textch():
        global alshow
        ash=textbar.toPlainText()
        if len(ash)>50:
            if alshow==False:
                prof.show()
                textbar.setFixedWidth(840)
                alshow=True
            else:
                return
        else:
            if alshow==True:
                prof.hide()
                textbar.setFixedWidth(900)
                alshow=False
            else:
                return
    textbar.textChanged.connect(textch)

    def sendmessage():
        config.read("persona.ini",encoding="utf-8")
        personaa=config["AI"]["persona"]
        global charcount
        charcount=0
        global text
        global replyyy
        text=textbar.toPlainText()
        if text:
            item=QListWidgetItem(f"you:\n{text}")
            if replyyy==True:
                llwidget=QWidget()
                lllayout=QVBoxLayout(llwidget)
                lllayout.setAlignment(Qt.AlignmentFlag.AlignRight)
                lllayout.setContentsMargins(0, 0, 0, 0)
                lllayout.setSpacing(5)
                replyingwidget=QPushButton(retext)
                replyingwidget.setMaximumWidth(400)
                replyingwidget.setMaximumHeight(70)
                #replyingwidget.setFixedSize(300,50)
                replyingwidget.show()
                replyingwidget.setStyleSheet("border:2px solid gray;background-color:#1e2a56;border-radius:15px;color:gray")
                replyingwidget.setFont(QFont("Calibri",17))
                lllayout.addWidget(replyingwidget)
                messagew=QLabel(text)
                messagew.setFont(QFont("Candara",17))
                messagew.setStyleSheet("border:none;background:none;font-family:Candara;font-size:22pt")
                messagew.setWordWrap(True)
                lllayout.addWidget(messagew)
            
            item.setFont(itemfont)
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignBottom)
            ml.addItem(item)
            if(replyyy==True):
                ml.setItemWidget(item,llwidget)
                item.setSizeHint(llwidget.sizeHint())
            ml.scrollToBottom()
            textbar.clear()
            wLabel.hide()
            cpicture.hide()
            joke.hide()
            imusic.hide()
            translate.hide()
            global currentchatid
            if(currentchatid==None):
                conn=sqlite3.connect("appdatabase.db")
                cursor=conn.cursor()
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS chats(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chatname TEXT,
                date DATETIME DEFAULT CURRENT_TIMESTAMP)
                """)
                conn.commit()
                cursor.execute("""
                INSERT INTO chats(
                    chatname
                )
                VALUES(?)
                """,(
                    text,
                ))
                currentchatid=cursor.lastrowid
                conn.commit()
                cursor.close()
            mhistory.append(f"user:{text}")
            global crw
            crw=QListWidgetItem()
            crw.setFont(itemfont)
            crw.setTextAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)
            ml.addItem(crw)
            output=""
            dots=0
            def thinking():
                nonlocal dots
                crw.setText("Carrot is thinking"+"."*dots)
                dots+=1
                print("ok")
                if dots>3:
                    dots=0
            global timer
            timer=QTimer()
            timer.timeout.connect(thinking)
            timer.start(200)
            ai = aianswer(
                text,
                mhistory,
                extract,
                streaming,
                modelname,
                replyyy,
                retext,
                charname,
                charage,
                charper,
                charhobbies,
                personaa
            )

            ai.signals.stream.connect(streaming)
            ai.signals.finished.connect(extract)

            ai.start()
            if replyyy==True:
                replyyy=False
                relabel.hide()
            send.setIcon(QIcon("answering.png"))
            send.blockSignals(True)


 
    shortcut=QShortcut(QKeySequence("Return"),textbar)
    shortcut.activated.connect(sendmessage)
    send.clicked.connect(sendmessage)
    wLabel=QLabel("welcome...have a good conversation!",window)
    if(b>0):
        wLabel.setStyleSheet("color:black")
    font=QFont("calibri",24)
    wLabel.setFont(font)
    wLabel.move(630,100)
    wLabel.resize(600,95)
    wLabel.show()
    menu=QWidget(window)
    menu.resize(500,1000)
    menu.move(0,0)
    if(b==0):
        menu.setStyleSheet("background-color:#00011a;border:none")
    else:
        menu.setStyleSheet("background-color:white;border:2px solid black")
    shadow=QGraphicsDropShadowEffect()
    shadow.setXOffset(3)
    shadow.setYOffset(3)
    if(b==0):
        menu.setGraphicsEffect(shadow)
    def opensettings():
        setting=QWidget()
        setting.show()
    menu.show()
    name=QLabel("PF-Carrot",menu)
    namefont=QFont("times new roman",34)
    namefont.setBold(True)
    name.move(15,5)
    name.setFont(namefont)
    if(b==0):
        name.setStyleSheet("color:Orangered;border:none")
    else:
        name.setStyleSheet("color:black;border:none")
    name.resize(300,150)
    name.show()
    bar=QWidget(window)
    bar.move(503,0)
    bar.resize(1420,55)
    if(b==0):
         #bar.setStyleSheet("background-color:rgb(19,38,92)")
        bar.setStyleSheet("background-color:#0B0F2A")
    else:
         bar.setStyleSheet("background-color:#D3D3D3;border:1px solid black")
    bar.show()
    # tab=QWidget(window)
    # tab.setFixedSize(200,38)
    # tab.move(500,1)
    # if(b==0):
    #     tab.setStyleSheet("background-color:#0A3463;border-top-right-radius:15px;border-bottom-right-radius:15px;border:1px solid #808080 ;padding:5px;")
    #     tab.move(504,1)
    # else:
    #     tab.setStyleSheet("background-color:#E4E4E4;border-top-right-radius:15px;border-bottom-right-radius:15px;border:1px solid black;padding:5px;")
    #     tab.move(500,1)
    # tab.show()
    # c=1
    # tabname=QLabel("chat 1",tab)
    # tabname.setStyleSheet("background:none;border:none;background:transparent")
    # tabname.move(3,2)
    # tabnamefont=QFont("calibri",16)
    # tabname.setFont(tabnamefont)
    # ###tabname.show()
    # addtab=QLabel("+",window)
    # addtab.move(710,10)
    # addtab.resize(20,20)
    # addtab.setStyleSheet("border:noun;background:noun;background:transparent;")
    # if(b>0):
    #     addtab.setStyleSheet("color:black;background:none;border:none")
    # addtabfont=QFont("Arial",16)
    # addtab.setFont(addtabfont)
    # addtab.show()
    modelb=QComboBox(window)
    modelb.setPlaceholderText("click to choose the LLM model")
    modelb.setStyleSheet("""
    QComboBox{
        color:gray;
        background-color:#1E2A56;
        border:0.5px solid gray; 
        border-radius:10px;
    }
    QComboBox::drop-down{
        border:none;
        background:transparent
    }
    """)
    modelb.resize(900,40)
    modelb.move(525,7)
    modelb.show()
    modelb.addItem("gemma3:1b(less smart but very fast)","gemma3:1b")
    modelb.addItem("llama3.1:8b(Default)","llama3.1:8b")
    modelb.addItem("gemma3:12b","gemma3:12b")
    modelb.addItem("qwen3:14b","qwen3:14b")
    modelb.setCurrentIndex(-1)
    def onchange(text):
        global modelname
        modelname=modelb.currentData()
        print(modelname)
        modelch=QLabel(f"{modelname} will answer to your messages",window)
        modelch.move(700,window.height()-200)
        modelch.setFont(QFont("calibri",12))
        modelch.resize(300,50)
        modelch.setStyleSheet("background-color:rgba(0,0,0,0.5);border:none;border-radius:12px")
        modelch.setAlignment(Qt.AlignmentFlag.AlignCenter)
        modelch.show()
        QTimer.singleShot(2000,modelch.hide)
    modelb.textActivated.connect(onchange)
    thbutton=QPushButton("︙",bar)
    thbutton.move(1,15)
    thbutton.setFont(QFont("calibri",16))
    thbutton.setStyleSheet("border:none;color:gray")
    thbutton.show()
    barunderlay=QWidget(bar)
    barunderlay.resize(98,45)
    barunderlay.move(930,5)
    barunderlay.setStyleSheet("background-color:#1E2A56;border:1px solid gray;border-radius:20px")
    barunderlay.show()
    newchat=QPushButton(bar)
    newchat.setStyleSheet("background:none;background:transparent;border:none")
    newchat.setIcon(QIcon("newchat.png"))
    newchat.resize(35,35)
    newchat.setIconSize(QSize(33,33))
    newchat.move(983,12)
    newchat.setToolTip("new chat")
    newchat.show()
    def createnewchat():
        ml.clear()
        mhistory=[]
        mc=0
        wLabel.show()
        cpicture.show()
        joke.show()
        imusic.show()
        translate.show()
        global currentchatid
        currentchatid=None
        ncc=QLabel("new chat is ready now",window)
        ncc.resize(120,40)
        ncc.setStyleSheet("background-color:rgba(50, 50, 50, 0.5);border-radius:10px")
        ncc.move(800,window.height()-150)
        ncc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ncc.show()
        if(replyyy==True):
            reply.hide()
        QTimer.singleShot(2000, ncc.hide)
    newchat.clicked.connect(createnewchat)
    chath=QPushButton(bar)
    chath.setIcon(QIcon("chathistory.png"))
    chath.resize(35,35)
    chath.setIconSize(QSize(33,33))
    chath.move(940,10)
    chath.setStyleSheet("background:none;border:none")
    chath.setToolTip("chats history")
    chath.show()
    def showchat(idnumber):
        global currentchatid
        currentchatid=idnumber
        conn=sqlite3.connect("appdatabase.db")
        cursor=conn.cursor()
        cursor.execute("""
        SELECT message
        FROM messages
        WHERE forchat=?
        ORDER BY id
        """,(idnumber,))
        messages=cursor.fetchall()
        conn.close()
        messlist=[]
        for i in messages:
            messlist.append(i[0])
        wLabel.hide()
        cpicture.hide()
        joke.hide()
        translate.hide()
        imusic.hide()
        messcount=len(messlist)
        for i in range(0,messcount):
            if i%2==0:
                item=QListWidgetItem(f"you:\n{messlist[i]}")
                item.setFont(itemfont)
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignBottom)
                ml.addItem(item)
                ml.scrollToBottom()
                mhistory.append(f"user:{messlist[i]}")
            else:
                crw=QListWidgetItem(f"Carrot:\n{messlist[i]}")
                crw.setFont(itemfont)
                crw.setTextAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)
                ml.addItem(crw)
                mhistory.append(f"assitant:{messlist[i]}")
            global mc
            mc+=1
    def showhistory():
        disunder=QPushButton(window)
        disunder.resize(window.width(),window.height())
        disunder.move(0,0)
        disunder.setStyleSheet("background:none;border:none")
        disunder.show()
        historylist=QWidget(window)
        historylist.resize(985,135)
        historylist.setStyleSheet("background-color:#1E2A56;border-radius:30px;padding:7px")
        historylist.move(527,60)
        historylist.show()
        listlist=QScrollArea(historylist)
        listlist.setStyleSheet("border-radius:30px")
        listlist.resize(historylist.width(),historylist.height())
        listlist.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        listlist.setWidgetResizable(True)
        listlist.show()
        listlist.setStyleSheet("border:none;background:none")
        zxc=QWidget()
        listlist.setWidget(zxc)
        zxc.setStyleSheet("border:none;background:none;border-radius:30px")
        historylay=QHBoxLayout(zxc)
        historylay.setAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignCenter)
        conn=sqlite3.connect("appdatabase.db")
        cursor=conn.cursor()
        cursor.execute("""
        SELECT id,chatname,date FROM chats
        ORDER BY id
        """)
        chatslist=cursor.fetchall()
        i=0
        for i in chatslist:
            chatid=i[0]
            chatname=i[1]
            chatcrtime=i[2]
            print(f"chat {chatid}\n-------------\nchat id:{chatid}\nchat name={chatname}\nchat created at:{chatcrtime}")
            chatwidget=QWidget()
            chatwidget.setFixedSize(160,100)
            chatwidget.setStyleSheet("background-color:#01122E;border:1px solid gray;border-radius:25px;padding:0px")
            chatnamel=QLabel(chatname,chatwidget)
            chatnamel.resize(130,40)
            chatnamel.move(10,10)
            chatnamel.setStyleSheet("border:none;background:none;color:white")
            chatnamelfont=QFont("Calibri",18)
            chatnamelfont.setBold(True)
            chatnamel.setFont(chatnamelfont)
            chatnamel.show()
            chatdatel=QLabel(chatcrtime,chatwidget)
            chatdatel.setStyleSheet("color:gray;border:none;background:none")
            chatdatel.setFont(QFont("calibri",12))
            chatdatel.move(10,60)
            chatdatel.show()
            showbutton=QPushButton(chatwidget)
            showbutton.setStyleSheet("border-radius:25px;background:none;border:none")
            showbutton.resize(160,100)
            showbutton.move(0,0)
            showbutton.show()
            showbutton.clicked.connect(partial(showchat,chatid))
            showbutton.clicked.connect(historylist.hide)
            historylay.addWidget(chatwidget)

        disunder.clicked.connect(historylist.hide)
        disunder.clicked.connect(disunder.hide)
    chath.clicked.connect(showhistory)
    profile=QWidget(window)
    profile.resize(400,170)
    profile.move(20,600)
    if(b==0):
        profile.setStyleSheet("background-color:#000126;border:1px solid white;border-radius:20px;")
    else:
        profile.setStyleSheet("background-color:white;border:2px solid black;border-radius:20px;")
    profile.show()
    if(b==0):
        profilephoto=QPixmap("profilephoto.png")
    else:
        profilephoto=QPixmap("profilephoto-light.png")
    pfp=QLabel(window)
    pfp.setPixmap(profilephoto.scaled(75,75))
    pfp.resize(75,75)
    pfp.move(30,620)
    pfp.setStyleSheet("border:1px;background:none;background:transparent")
    pfp.show()
    file_name=("count.json")
    if not os.path.exists(file_name):
        with open(file_name,"w") as f:
            json.dump({"datacount":0},f,indent=4)
    with open(file_name,"r") as f:
        count=json.load(f)
    if count["datacount"]==0:
        config["AI"]={
            "persona":"None"
        }
        with open ("persona.ini","w",encoding="utf-8") as file:
            config.write(file)
    if count["datacount"]==0:
        nametag=QLabel("unknown",window)
        nametag.setStyleSheet("background:none;border:none;background:transparent")
        nametagfont=QFont("calibri",24)
        nametagfont.setBold(True)
        nametag.setFont(nametagfont)
        nametag.resize(200,75)
        nametag.move(125,620)
        nametag.show()
        agetag=QLabel("age:unknown",window)
        agetag.setStyleSheet("background:none;background:transparent;border:none")
        agetagfont=QFont("calibri",12)
        agetag.setFont(agetagfont)
        agetag.move(125,660)
        agetag.resize(150,50)
        agetag.show()
        etag=QLabel("email:unknown",window)
        etag.setStyleSheet("background:none;background:transparent;border:none")
        etag.move(125,680)
        etag.resize(300,50)
        etagfont=QFont("calibri",12)
        etag.setFont(etagfont)
        etag.show()
        QMessageBox.information(window,"PF-Carrot","lets get some info")
        name,OK=QInputDialog.getText(window,"PF-Carrot","enter your name..")
        age,ok=QInputDialog.getText(window,"PF-Carrot","enter your age...")
        email,ok=QInputDialog.getText(window,"PF-Carrot","enter your email")
        etag.hide()
        nametag.hide()
        agetag.hide()
        finish=QLabel("Finish!🤩",window)
        finish.setStyleSheet("color:Orange")
        finish.resize(1100,360)
        finishfont=QFont("impact",200)
        finish.setFont(finishfont)
        finish.move(300,220)
        finish.show()
        skip=QPushButton("skip>",window)
        skip.resize(75,75)
        skip.move(750,560)
        skipfont=QFont("calibri",18)
        skip.setFont(skipfont)
        skip.setStyleSheet("border:none")
        skip.show()
        skip.clicked.connect(skip.hide)
        skip.clicked.connect(finish.hide)
        file="data.json"
        if not os.path.exists(file):
            with open(file,"w") as f:
                json.dump({"name":name,"age":age,"email":email},f,indent=4)
        count["datacount"]+=1
        with open(file_name,"w") as f:
            json.dump(count,f,indent=4)
    with open("data.json","r") as f:
        data=json.load(f)
    hoora=QLabel("🎉",window)
    hoora.resize(1100,360)
    hoora.move(300,220)
    hoorafont=QFont("calibri",200)
    hoora.setFont(hoorafont)
    ca=0
    intage=int(data["age"])
    birthyear=(2026-intage)
    nametag=QLabel(data["name"],window)
    nametagfont=QFont("Arial",24)
    nametagfont.setBold(True)
    nametag.setFont(nametagfont)
    nametag.resize(200,75)
    nametag.move(125,620)
    nametag.show()
    agetag=QLabel(f"is {data['age']} years old ({birthyear})",window)
    agetagfont=QFont("calibri",12)
    agetag.setFont(agetagfont)
    agetag.move(125,660)
    agetag.resize(150,50)
    agetag.show()
    etag=QLabel(f"email: {data['email']}",window)
    etag.move(125,680)
    etag.resize(300,50)
    etagfont=QFont("calibri",12)
    etag.setFont(etagfont)
    if(b==0):
        nametag.setStyleSheet("background:none;border:none;background:transparent")
        agetag.setStyleSheet("background:none;background:transparent;border:none")
        etag.setStyleSheet("background:none;background:transparent;border:none")
    else:
        nametag.setStyleSheet("color:black;background:none;border:none;background:transparent")
        agetag.setStyleSheet("color:black;background:none;background:transparent;border:none")
        etag.setStyleSheet("color:black;background:none;background:transparent;border:none")
    etag.show()
    nametag.show()
    agetag.show()
    dmode=QPushButton("🌗dark/light mode",window)
    dmodefont=QFont("calibri",15)
    dmode.setFont(dmodefont)
    dmode.move(10,200)
    dmode.resize(160,50)
    if(b>0):
        dmode.setStyleSheet("color:black;")
    else:
        dmode.setStyleSheet("border:none;")
    dmode.show()
    def changemode():
        if(b>0):
            message=QMessageBox(window)
            message.setWindowTitle("PF-Carrot")
            message.setText("mode changed.saves will appear with openning the app again")
            message.setStyleSheet("background-color:white;color:black")
            mfont=QFont("calibri",12)
            message.setFont(mfont)
            message.show()
        else:
           QMessageBox.information(window,"PF-Carrot","mode changed.saves will appear with openning the app again")
        settingsfile["mode"]+=1
        with open(settings_filename,"w") as f:
          json.dump(settingsfile,f,indent=4)
    dmode.clicked.connect(changemode)
    pb=QPushButton("👤persona",window)
    pb.resize(95,50)
    pb.move(10,150)
    pbfont=QFont("calibri",15)
    pb.setFont(pbfont)
    if(b==0):
        pb.setStyleSheet("border:none")
    else:
        pb.setStyleSheet("color:black;")
    pb.show()
    def personaset():
        pwindow=QWidget(window)
        if(b==0):
            pwindow.setStyleSheet("background-color:#00011a;border:2px solid white;border-radius:20px;")
        else:
            pwindow.setStyleSheet("background-color:white;border:2px solid black;border-radius:20px;")
        pwindow.resize(1200,650)
        pwindow.move(50,50)
        pwindow.show()
        plabel=QLabel("Persona",pwindow)
        plabel.move(50,25)
        plabel.resize(600,75)
        plabelfont=QFont("calibri",32)
        if(b==0):
            plabel.setStyleSheet("border:none;")
        else:
            plabel.setStyleSheet("color:black;border:none;")
        plabelfont.setBold(True)
        plabel.setFont(plabelfont)
        plabel.show()
        plabel2=QLabel("this wil be your character and idenitity in the chats",pwindow)
        if(b==0):
            plabel2.setStyleSheet("border:none")
        else:
            plabel2.setStyleSheet("border:none;color:black")
        plfont=QFont("calibri",12)
        plabel2.setFont(plfont)
        plabel2.move(50,95)
        plabel2.resize(350,25)
        plabel2.show()
        personabox=QTextEdit(pwindow)
        personabox.setPlaceholderText("write what u want...")  
        if(b==0):
            personabox.setStyleSheet("background-color:#1E2A56;border:1px solid white;border-radius:20px;padding:5px;")
        else:
            personabox.setStyleSheet("background-color:#F8F8F8;color:black;border:2px solid black;border-radius:20px;padding:5px;")
        personabox.resize(800,350)
        personabox.move(200,180)
        personabox.show()
        savebtn=QPushButton("save",pwindow)
        if (b==0):
            savebtn.setStyleSheet("background-color:#ADD8E6;border-radius:20px;border:none;")
        else:
            savebtn.setStyleSheet("background-color:#D3D3D3;border-radius:20px;border:none;")
        savebtn.resize(120,40)
        savebtn.move(1050,580)
        savebtnfont=QFont("calibri",15)
        savebtn.setFont(savebtnfont)
        savebtn.show()
        cancelbtn=QPushButton("cancel",pwindow)
        cancelbtn.resize(120,40)
        cancelbtn.move(910,580)
        if (b==0):
            cancelbtn.setStyleSheet("background-color:rgb(19,38,92);border-radius:20px;border:none;")
        else:
            cancelbtn.setStyleSheet("background-color:white;color:black;border-radius:20px;border:none;")
        cancelbtnfont=QFont("calibri",15)
        cancelbtn.setFont(cancelbtnfont)
        cancelbtn.show()
        cancelbtn.clicked.connect(pwindow.hide)
        def save():
            persona=personabox.toPlainText()
            config.read("persona.ini")
            if persona:
                config["AI"]["persona"]=persona
                with open("persona.ini","w") as f:
                    config.write(f)
            if persona==None:
                config["AI"]["persona"]="None"
                with open("persona.ini","w") as f:
                    config.write(f)
            personabox.clear()
            pwindow.hide()
        savebtn.clicked.connect(save)
    pb.clicked.connect(personaset)

    ttd=QPushButton("💬talk to the developer",window)
    ttd.resize(200,50)
    ttd.move(10,250)
    ttdfont=QFont("calibri",15)
    ttd.setFont(ttdfont)
    if(b==0):
        ttd.setStyleSheet("border:none;")
    else:
        ttd.setStyleSheet("color:black")
    ttd.show()
    def talkttd():
        url="https://web.bale.ai/chat?uid=16557348"
        webbrowser.open(url)
    ttd.clicked.connect(talkttd)

    change=QPushButton("📝change info.",window)
    change.resize(130,50)
    change.move(10,300)
    changefont=QFont("calibri",15)
    change.setFont(changefont)
    if(b==0):
        change.setStyleSheet("border:none")
    else:
        change.setStyleSheet("color:black")
    change.show()
    def changeinformation():
        which,ok=QInputDialog.getText(window,"PF-Carrot","enter name for changing name\nenter age for changing age\nenter email for changing email")
        if (which=="name"):
            name,ok=QInputDialog.getText(window,"PF-Carrot","enter your name")
            with open("data.json","r") as file:
                data=json.load(file)
            data["name"]=name
            with open("data.json","w") as file:
                json.dump(data,file,indent=4)
        elif(which==age):
            with open("data.json","r") as file:
                data=json.load(file)
            data["age"]=age
            with open("data.json","w") as file:
                json.dump(data,file,indent=4)
        elif(which==age):
            with open("data.json","r") as file:
                data=json.load(file)
            data["email"]=email
            with open("data.json","w") as file:
                json.dump(data,file,indent=4)    
    change.clicked.connect(changeinformation)
    setc=QPushButton("👩set character",window)
    setc.resize(140,50)
    setc.move(10,350)
    setcfont=QFont("calibri",15)
    setc.setFont(setcfont)
    setc.setStyleSheet("border:none;")
    if(b>0):
        setc.setStyleSheet("color:black")
    setc.show()
    def setcharacter():
        characters=QWidget(window)
        characters.resize(1200,650)
        characters.move(50,50)
        if(b==0):
            characters.setStyleSheet("background-color:#00011a;border:2px solid white;border-radius:25px;")
        else:
            characters.setStyleSheet("background-color:white;border:2px solid black;border-radius:25px;")
        characters.show()
        clabel=QLabel("characters",characters)
        clabel.move(50,25)
        clabel.resize(600,75)
        clabelfont=QFont("calibri",32)
        if(b==0):
            clabel.setStyleSheet("border:none;")
        else:
            clabel.setStyleSheet("color:black;border:none;")
        clabelfont.setBold(True)
        clabel.setFont(clabelfont)
        clabel.show()
        clabel2=QLabel("here u can specify the default character of the bot during the chat",characters)
        if(b==0):
            clabel2.setStyleSheet("border:none")
        else:
            clabel2.setStyleSheet("border:none;color:black")
        clfont=QFont("calibri",12)
        clabel2.setFont(clfont)
        clabel2.move(50,95)
        clabel2.resize(500,25)
        clabel2.show()
        resetbtn=QPushButton("Reset",characters)
        if (b==0):
            resetbtn.setStyleSheet("background-color:#ADD8E6;border-radius:20px;border:none;")
        else:
            resetbtnbtn.setStyleSheet("background-color:#B8B8B8;border-radius:20px;border:none;")
        resetbtn.resize(120,40)
        resetbtn.move(1050,580)
        resetbtnfont=QFont("calibri",15)
        resetbtn.setFont(resetbtnfont)
        resetbtn.show()
        def reset():
            global charper
            global charname
            global charage
            global charhobbies
            charname="Carrot"
            charname=None
            charage=None
            charhobbies=None
            characters.hide()
            post=QLabel(window)
            post.resize(200,50)
            post.setText("character reset to Carrot")
            post.setStyleSheet("border:none;background:rgba(1,1,1,0.8);color:white;border-radius:15px")
            post.move(760,window.height()-200)
            post.setFont(QFont("calibri",14))
            post.setAlignment(Qt.AlignmentFlag.AlignCenter)
            post.show()
            QTimer.singleShot(1500,post.hide)
        resetbtn.clicked.connect(reset)
        cancelbtn=QPushButton("cancel",characters)
        cancelbtn.resize(120,40)
        cancelbtn.move(910,580)
        if (b==0):
            cancelbtn.setStyleSheet("background-color:rgb(19,38,92);border-radius:20px;border:none;")
        else:
            cancelbtn.setStyleSheet("background-color:white;color:black;border-radius:20px;border:none;")
        cancelbtnfont=QFont("calibri",18)
        cancelbtn.setFont(cancelbtnfont)
        cancelbtn.show()
        cancelbtn.clicked.connect(characters.hide)
        robert=QWidget(characters)
        robert.resize(350,150)
        robert.move(200,170)
        if(b==0):
            robert.setStyleSheet("background-color:#1E2A56;border:2px solid white;border-radius:25px")
        else:
            robert.setStyleSheet("border:2px solid black;border-radius:25px")
        robert.show()
        rlabel=QLabel("Robert",robert)
        rlabel.resize(100,30)
        rlabel.move(130,20)
        rlabelfont=QFont("calibri",24)
        rlabelfont.setBold(True)
        rlabel.setFont(rlabelfont)
        rlabel.setStyleSheet("background:none;background:transparent;border:none")
        if(b>0):
            rlabel.setStyleSheet("color:black;border:none;")
        rlabel.show()
        rphoto=QLabel("👦",robert)
        rphoto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rphoto.resize(100,100)
        rphoto.move(20,20)
        if(b==0):
            rphoto.setStyleSheet("background-color:white;border-radius:50px")
        else:
            rphoto.setStyleSheet("background-color:#D3D3D3;border:2px solid black;border-radius:50px")
        rphotofont=QFont("arial",58)
        rphoto.setFont(rphotofont)
        rphoto.show()
        rdetails=QPushButton("click here to view details >",robert)
        rdetails.resize(195,30)
        rdetails.move(120,50)
        detailsfont=QFont("calibri",12)
        detailsfont.setUnderline(True)
        rdetails.setFont(detailsfont)
        rdetails.setStyleSheet("background:npne;background:transparent;border:none;")
        if(b>0):
            rdetails.setStyleSheet("color:black;border:none;")
        rdetails.show()
        ctagsfont=QFont("calibri",18)
        cnametagsfont=QFont("calibri",26)
        cnametagsfont.setBold(True)
        robertage=26
        robertname="Robert"
        robertc="interovert,nerd,strict,curious,friendly,ready to teach"
        roberthobies="studying,reading books,talking to near friends,watching tv."
        robertsuggestion="practical discusstions and questions"

        chdetails=QWidget(window)
        chdetails.resize(1200,650)
        chdetails.move(50,50)

        if(b==0):
            chdetails.setStyleSheet("background-color:#00011a;border:2px solid white;border-radius:25px;")
        else:
            chdetails.setStyleSheet("background-color:white;border:2px solid black;border-radius:25px;")
        choosebtn=QPushButton("choose",chdetails)
        if (b==0):
            choosebtn.setStyleSheet("background-color:#ADD8E6;border-radius:20px;border:none;")
        else:
            choosebtn.setStyleSheet("background-color:#D3D3D3;border-radius:20px;border:none;")
        choosebtn.resize(120,40)
        choosebtn.move(1050,580)
        choosebtnfont=QFont("calibri",15)
        choosebtn.setFont(choosebtnfont)
        choosebtn.show()
        def choosed():
            global charper
            global charname
            global charage
            global charhobbies
            charper=cptag.text()
            charage=cagetag.text()
            charname=cnametag.text()
            charhobbies=chtag.text()
            chdetails.hide()
            characters.hide()
            msg=QMessageBox(window)
            msg.setText(f"set character to {charname}")
            #msg.setStandardButtons(QMessageBox.Ok)
            #msg.setStyleSheet("background-volor:#00011a;border:1px solid gray;border-radius:25px")
            msg.setFont(QFont("calibri",14))
            msg.show()
            global chochname
            chochname=charname
        choosebtn.clicked.connect(choosed)
        cancelbtn=QPushButton("cancel",chdetails)
        cancelbtn.resize(120,40)
        cancelbtn.move(910,580)
        if (b==0):
            cancelbtn.setStyleSheet("background-color:rgb(19,38,92);border-radius:20px;border:none;")
        else:
            cancelbtn.setStyleSheet("background-color:white;color:black;border-radius:20px;border:none;")
        cancelbtnfont=QFont("calibri",18)
        cancelbtn.setFont(cancelbtnfont)
        cancelbtn.show()
        cancelbtn.clicked.connect(chdetails.hide)
        def detailsshow():
            chdetails.show()
        rdetails.clicked.connect(detailsshow)
        mmd=QWidget(characters)
        mmd.resize(350,150)
        mmd.move(570,170)
        if(b==0):
            mmd.setStyleSheet("background-color:#1E2A56;border:2px solid white;border-radius:25px")
        else:
            mmd.setStyleSheet("border:2px solid black;border-radius:25px")
        mmd.show()
        mlabel=QLabel("mmd",mmd)
        mlabel.resize(100,30)
        mlabel.move(130,20)
        mlabelfont=QFont("calibri",24)
        mlabelfont.setBold(True)
        mlabel.setFont(rlabelfont)
        mlabel.setStyleSheet("background:none;background:transparent;border:none")
        if(b>0):
            mlabel.setStyleSheet("color:black;border:none;")
        mlabel.show()
        mphoto=QLabel("🧔",mmd)
        mphoto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mphoto.resize(100,100)
        mphoto.move(20,20)
        if(b==0):
            mphoto.setStyleSheet("background-color:white;border-radius:50px")
        else:
            mphoto.setStyleSheet("background-color:#D3D3D3;border:2px solid black;border-radius:50px;")
        mphotofont=QFont("arial",58)
        mphoto.setFont(rphotofont)
        mphoto.show()
        mdetails=QPushButton("click here to view details >",mmd)
        mdetails.resize(195,30)
        mdetails.move(120,50)
        metailsfont=QFont("calibri",12)
        mdetails.setFont(detailsfont)
        mdetails.setStyleSheet("background:none;background:transparent;border:none;")
        if(b>0):
            mdetails.setStyleSheet("color:black;border:none;")
        mdetails.show()
        mdetails.clicked.connect(chdetails.show)
        mmdname="mmd"
        mmdage=22
        mmdhobbies="playing soccer,playing basketball,talking to people,watching tv.,playing video games"
        mmdpersonality="extrovert,friendly,cool and chill"
        mmdsuggestion="daily conversations"
        lily=QWidget(characters)
        lily.resize(350,150)
        lily.move(200,340)
        if(b==0):
            lily.setStyleSheet("background-color:#1E2A56;border:2px solid white;border-radius:25px")
        else:
            lily.setStyleSheet("border:2px solid black;border-radius:25px")
        lily.show()
        lphoto=QLabel("👩‍🦰",lily)
        lphoto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lphoto.resize(100,100)
        lphoto.move(20,20)
        if(b==0):
            lphoto.setStyleSheet("background-color:white;border-radius:50px")
        else:
            lphoto.setStyleSheet("background-color:#D3D3D3;border:2px solid black;border-radius:50px;")
        lphotofont=QFont("arial",55)
        lphoto.setFont(lphotofont)
        lphoto.show()
        llabel=QLabel("Lily",lily)
        llabel.resize(100,30)
        llabel.move(130,20)
        llabelfont=QFont("calibri",24)
        llabelfont.setBold(True)
        llabel.setFont(rlabelfont)
        llabel.setStyleSheet("background:none;background:transparent;border:none")
        if(b>0):
            llabel.setStyleSheet("color:black;border:none;")
        llabel.show()
        ldetails=QPushButton("click here to view details >",lily)
        ldetails.resize(195,30)
        ldetails.move(120,50)
        letailsfont=QFont("calibri",12)
        ldetails.setFont(detailsfont)
        ldetails.setStyleSheet("background:none;background:transparent;border:none;")
        if(b>0):
            ldetails.setStyleSheet("color:black;border:none;")
        ldetails.show()
        lilyname="Lily"
        lilyage=19
        lilyhobbies="watching movies,reading books,hanging out with friends,scrolling,sleeping"
        lilyp="very extrovert,social,emotional,energetic"
        lilysuggestion="daily chats or chatting when u are bored"
        Marry=QWidget(characters)
        Marry.resize(350,150)
        Marry.move(570,340)
        if(b==0):
            Marry.setStyleSheet("background-color:#1E2A56;border:2px solid white;border-radius:25px")
        else:
            Marry.setStyleSheet("border:2px solid black;border-radius:25px")
        Marry.show()
        maphoto=QLabel("👩‍🦱",Marry)
        maphoto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        maphoto.resize(100,100)
        maphoto.move(20,20)
        if(b==0):
            maphoto.setStyleSheet("background-color:white;border-radius:50px")
        else:
            maphoto.setStyleSheet("background-color:#D3D3D3;border:2px solid black;border-radius:50px;")
        maphotofont=QFont("arial",55)
        maphoto.setFont(lphotofont)
        maphoto.show()
        malabel=QLabel("Marry",Marry)
        malabel.resize(100,30)
        malabel.move(130,20)
        malabelfont=QFont("calibri",24)
        malabelfont.setBold(True)
        malabel.setFont(rlabelfont)
        malabel.setStyleSheet("background:none;background:transparent;border:none")
        if(b>0):
            malabel.setStyleSheet("color:black;border:none;")
        malabel.show()
        madetails=QPushButton("click here to view details >",Marry)
        madetails.resize(195,30)
        madetails.move(120,50)
        madetailsfont=QFont("calibri",12)
        madetails.setFont(detailsfont)
        madetails.setStyleSheet("background:none;background:transparent;border:none;")
        if(b>0):
            madetails.setStyleSheet("color:black;border:none;")
        madetails.show()
        marryname="Marry"
        marryage="27"
        marryhobbies="reading books(scientific topics),watching movies,watching memes,talking(st)"
        marryp="hard working,a little extrovert,curious,cool"
        marrysuggestion="both daily conversations and practical discusstions and questions "
        cagetag=QLabel(chdetails)
        cagetag.move(50,180)
        cagetag.resize(100,30)
        cagetag.setStyleSheet("border:none;background:none;background:transparent;")
        if(b>0):
            cagetag.setStyleSheet("border:none;color:black;")
        cagetag.setFont(ctagsfont)
        cnametag=QLabel(chdetails)
        cnametag.resize(120,40)
        cnametag.move(160,75)
        cnametag.setFont(cnametagsfont)
        cnametag.setStyleSheet("border:none;background:none;background:transparent;")
        if(b>0):
            cnametag.setStyleSheet("border:none;color:black")
        cptag=QLabel(chdetails)
        cptag.move(50,230)
        cptag.resize(700,30)
        cptag.setFont(ctagsfont)
        cptag.setStyleSheet("border:none;background:none;background:transparent;")
        if(b>0):
            cptag.setStyleSheet("border:none;color:black;")
        chtag=QLabel(chdetails)
        chtag.resize(1000,30)
        chtag.move(50,280)
        chtag.setStyleSheet("border:none;background:none;background:transparent;")
        if(b>0):
            chtag.setStyleSheet("border:none;color:black;")
        chtag.setFont(ctagsfont)
        chtag.show()
        cstag=QLabel(chdetails)
        cstag.move(50,330)
        cstag.resize(700,30)
        cstag.setFont(ctagsfont)
        cstag.setStyleSheet("border:none;background:none;background:transparent;")
        if(b>0):
            cstag.setStyleSheet("border:none;color:black;")
        chphoto=QLabel(chdetails)
        chphoto.resize(100,100)
        chphoto.setFont(rphotofont)
        chphoto.move(50,50)
        chphoto.setStyleSheet("background-color:white;border-radius:45px")
        chphoto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        def robertdetails():
            cagetag.setText(f"age:{robertage}")
            cnametag.setText(robertname)
            cptag.setText(f"personality:{robertc}")
            chtag.setText(f"hobbies:{roberthobies}")
            cstag.setText(f"⭐suggested for{robertsuggestion}")
            chphoto.setText("👦")
            cagetag.show()
            cnametag.show()
            chtag.show()
            cstag.show()
            cptag.show()
        rdetails.clicked.connect(robertdetails)
        def mmddetails():
            cagetag.setText(f"age:{mmdage}")
            cnametag.setText("mmd")
            cptag.setText(f"personality:{mmdpersonality}")
            chtag.setText(f"hobbies:{mmdhobbies}")
            cstag.setText(f"⭐suggested for {mmdsuggestion}")
            chphoto.setText("🧔")
            cagetag.show()
            cnametag.show()
            chtag.show()
            cstag.show()
            cptag.show()
            chdetails.show()
        mdetails.clicked.connect(mmddetails)
        def lilydetails():
            cagetag.setText(f"age:{lilyage}")
            cnametag.setText(lilyname)
            cptag.setText(f"personality:{lilyp}")
            chtag.setText(f"hobbies:{lilyhobbies}")
            cstag.setText(f"⭐suggested for {lilysuggestion}")
            chphoto.setText("👩‍🦰")
            cagetag.show()
            cnametag.show()
            chtag.show()
            cstag.show()
            cptag.show()
            chdetails.show()
        ldetails.clicked.connect(lilydetails)
        def marrydetails():
            cagetag.setText(f"age:{marryage}")
            cnametag.setText(marryname)
            cptag.setText(f"personality:{marryp}")
            chtag.setText(f"hobbies:{marryhobbies}")
            cstag.setText(f"⭐suggested for {marrysuggestion}")
            chphoto.setText("👩‍🦱")
            cagetag.show()
            cnametag.show()
            chtag.show()
            cstag.show()
            cptag.show()
            chdetails.show()
        madetails.clicked.connect(marrydetails)


        




    
    setc.clicked.connect(setcharacter)


    joke=QPushButton("tell me a joke",window)
    if(b==0):
        joke.setStyleSheet("background-color:#1E2A56;border:1px solid gray;border-radius:20px;")
    else:
        joke.setStyleSheet("color:black;background-color:#F8F8F8;border:1px solid black;border-radius:15px;")
    joke.move(630,190)
    joke.resize(120,40)
    jokefont=QFont("Arial",12)
    joke.setFont(jokefont)
    joke.show()
    def ifinish(success,result):
        prlabel.hide()
        progress.hide()
        if success:
            print(f"image:{result}")
            resimagl=QLabel(resw)
            resimagl.resize(200,200)
            resimagl.move(200,20)
            resimage=QPixmap(result)
            resimagl.setPixmap(resimage)
            resimagl.show()
        else:
            errlabel=QLabel(result,resw)
            errlabel.setStyleSheet("border:none;color:orange")
            errlabel.show()
            errlabel.move(20,20)
            
    def generate(crew,crtextb,crnameb):
        global prlabel
        global progress
        global resw
        prompt=crtextb.toPlainText()
        name=crnameb.text()
        resw=QWidget(crew)
        resw.resize(crew.width(),crew.height())
        resw.move(0,0)
        resw.show()
        prlabel=QLabel("generating image...",resw)
        prlabel.setStyleSheet("border:none;color:white")
        prlabel.move(20,20)
        prlabel.setFont(QFont("Calibri",24))
        prlabel.show()
        progress=QProgressBar(resw)
        progress.setStyleSheet("border-radius:5px;border:none")
        progress.resize(500,30)
        progress.move(40,90)
        progress.setRange(0,0)
        progress.show()
        crew.generator=ImageGenerator(prompt,ifinish,name)
        crew.generator.finished.connect(ifinish)
        crew.generator.finished.connect(crew.generator.deleteLater)
        crew.generator.start()
    def create():
        global crew
        crew=QWidget(window)
        crew.resize(600,650)
        crew.move(550,100)
        crew.setStyleSheet("background-color:#00011a;border-radius:15px;border:1px solid white")
        crew.show()
        crback=QPushButton("←",crew)
        crback.setStyleSheet("""
        QPushButton{
            border:none;background:none;color:white}
        QPushButton::hover{
            border:1px solid white;border-radius:2px;color:white
        }""")
        crback.setFont(QFont("calibri",24))
        crback.move(20,20)
        crback.show()
        crback.clicked.connect(crew.hide)
        crlabel=QLabel("Image creation",crew)
        crlabel.setStyleSheet("color:white;border:none")
        crlabel.move(60,20)
        crlabel.setFont(QFont("Calibri",24))
        crlabel.show()
        crlabel2=QLabel("describe what u wanna create and just wait",crew)
        crlabel2.setStyleSheet("color:white;border:none")
        crlabel2.setFont(QFont("calibri",17))
        crlabel2.move(50,70)
        crlabel2.show()
        crtextb=QTextEdit(crew)
        crtextb.setPlaceholderText("describe the image you want...")
        crtextb.move(50,130)
        crtextb.resize(500,350)
        crtextb.setStyleSheet("background-color:#1e2a56;border:1px solid gray;border-radius:15px;padding:5px")
        crtextb.show()
        crnameb=QLineEdit(crew)
        crnameb.resize(400,50)
        crnameb.move(50,500)
        crnameb.show()
        crnameb.setPlaceholderText("enter the pictures name")
        crnameb.setStyleSheet("border:1px solid gray;background-color:#1e2a56;border-radius:15px;padding:5px")
        createb=QPushButton("Create →",crew)
        createb.setStyleSheet("""
        QPushButton{
        background-color:#1e2a56;border-radius:24px;border:none}
        QPushButton::hover{
        background-color:#1e2a56;border-radius:22px;border:1px solid gray;width:130;height:60
        }""")
        createb.move(460,570)
        createb.resize(120,50)
        createb.setFont(QFont("calibri",16))
        createb.show()
        createb.clicked.connect(lambda:generate(crew,crtextb,crnameb))
    cpicture=QPushButton("create a picture",window)
    cpicture.clicked.connect(create)
    if(b==0):
        cpicture.setStyleSheet("background-color:#1E2A56;border:1px solid gray;border-radius:20px;")
    else:
        cpicture.setStyleSheet("color:black;background-color:#F8F8F8;border:1px solid black;border-radius:15px;")
    cpicture.move(760,190)
    cpicture.resize(120,40)
    cpicturefont=QFont("Arial",12)
    cpicture.setFont(cpicturefont)
    cpicture.show()
    translate=QPushButton("translate for me",window)
    if(b==0):
        translate.setStyleSheet("background-color:#1E2A56;border:1px solid gray;border-radius:20px;")
    else:
        translate.setStyleSheet("color:black;background-color:#F8F8F8;border:1px solid black;border-radius:15px;")
    translate.move(890,190)
    translate.resize(120,40)
    translatefont=QFont("Arial",12)
    translate.setFont(translatefont)
    translate.show()
    imusic=QPushButton("introduce me some songs",window)
    if(b==0):
        imusic.setStyleSheet("background-color:#1E2A56;border:1px solid gray;border-radius:20px;")
    else:
        imusic.setStyleSheet("color:black;background-color:#F8F8F8;border:1px solid black;border-radius:20px;")
    imusic.resize(200,40)
    imusic.move(630,240)
    imusic.setFont(translatefont)
    imusic.show()

    add=QPushButton("+",window)
    add.move(535,730)
    add.resize(30,30)
    if(b==0):
        add.setStyleSheet("border:1px solid gray;border-radius:15px;background-color:rgb(19,38,92);")
    else:
        add.setStyleSheet("border:2px solid black;border-radius:15px;background:none;color:black")
    addfont=QFont("Arial",25)
    ###addfont.setBold(True)
    add.setFont(addfont)
    add.show()
    def addsmth():
        fk=QWidget(window)
        fk.resize(150,200)
        fk.move(535,530)
        if(b==0):
            fk.setStyleSheet("background-color:#00011a;border-radius:25px;border:2px solid white")
        else:
            fk.setStyleSheet("border-radius:25px;border:2px solid black")
        fk.show()
        aaa=QPushButton(window)
        aaa.resize(1235,window.height())
        aaa.move(685,0)
        aaa.setStyleSheet("background:none;border:none;background:transparent;")
        aaa.show()
        aaa.clicked.connect(fk.hide)
        bbb=QPushButton(window)
        bbb.resize(150,530)
        bbb.move(150,0)
        bbb.setStyleSheet("background:none;border:none;background:transparent;")
        bbb.show()
        bbb.clicked.connect(fk.hide)
        ccc=QPushButton(window)
        ccc.move(0,0)
        ccc.resize(535,window.height())
        ccc.setStyleSheet("background:none;border:none;background:transparent;")
        ccc.show()
        ccc.clicked.connect(fk.hide)
        ccc.clicked.connect(aaa.hide)
        ccc.clicked.connect(bbb.hide)
        ccc.clicked.connect(ccc.hide)
        aaa.clicked.connect(aaa.hide)
        aaa.clicked.connect(bbb.hide)
        aaa.clicked.connect(ccc.hide)
        bbb.clicked.connect(aaa.hide)
        bbb.clicked.connect(bbb.hide)
        bbb.clicked.connect(ccc.hide)
        photo=QPushButton("🖼️Photos",fk)
        if(b==0):
            photo.setStyleSheet("background:none;border:none;")
        else:
            photo.setStyleSheet("background:none;border:none;color:black")
        lfont=QFont("Arial",15)
        photo.setFont(lfont)
        photo.resize(90,25)
        photo.move(15,30)
        photo.show()
        camera=QPushButton("📸camera",fk)
        camera.setFont(lfont)
        camera.resize(95,25)
        camera.move(15,80)
        if(b==0):
            camera.setStyleSheet("background:none;border:none;")
        else:
            camera.setStyleSheet("background:none;border:none;color:black")
        camera.show()
        file=QPushButton("📁files",fk)
        file.resize(70,25)
        file.setFont(lfont)
        if(b==0):
            file.setStyleSheet("background:none;border:none;")
        else:
            file.setStyleSheet("background:none;border:none;color:black")
        file.move(15,130)
        file.show()
    add.clicked.connect(addsmth)
    crp=QPushButton("🎭role play",window)
    crp.setStyleSheet("border:none")
    if(b>0):
        crp.setStyleSheet("border:none;color:black")
    crp.move(10,400)
    crp.resize(105,50)
    crp.setFont(setcfont)
    crp.show()
    def roleplay():
        mhistory=[]
        rpblur=QWidget(window)
        rpblur.resize(window.width(),window.height())
        rpblur.setStyleSheet("background-color:rgba(0,0,0,0.7)")
        rpblur.move(0,0)
        rpblur.show()
        rpmenu=QWidget(window)
        rpmenu.resize(500,window.height())
        rpmenu.setStyleSheet("background-color:#00011a")
        shadow=QGraphicsDropShadowEffect()
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        if(b==0):
            rpmenu.setGraphicsEffect(shadow)
        rpmenu.show()
        underlay=QWidget(rpmenu)
        underlay.resize(401,95)
        underlay.move(50,13)
        underlay.setStyleSheet("background-color:#0A3463;border:1px solid white;border-radius:25px")
        underlay.show()
        guide=QPushButton("📃",underlay)
        guide.move(345,27)
        guide.setStyleSheet("border:none")
        guidef=QFont("Calibri",24)
        guide.setFont(guidef)
        guide.show()
        def info():
            gs=QWidget(rpmenu)
            gs.setStyleSheet("background-color:#0A3463;border:1px solid white;border-radius:25px")
            guide.setToolTip("what can I do in CRP?")
            gs.resize(401,180)
            gs.move(50,13)
            gs.show()
            guidet=QLabel("Here u can talk to movie and cartoon\ncharacters and even characters made by ys\nu can also have the role of a\ncharacter yourself\nand a good option is making scenarios!\njust use ** for telling what u do\nand "" for telling what u say",gs)
            guidet.setStyleSheet("border:none")
            guidetf=QFont("Arial",13)
            guidet.setFont(guidetf)
            guidet.move(10,10)
            guidet.show()
            guideok=QPushButton("ok",gs)
            guideokf=QFont("Arial",12)
            guideok.setFont(guideokf)
            guideok.move(360,150)
            guideok.setStyleSheet("border:none")
            guideok.show()
            guideok.clicked.connect(gs.hide)
        guide.clicked.connect(info)
        back=QPushButton("←",rpmenu)
        backf=QFont("Arial",28)
        back.setFont(backf)
        back.move(10,20)
        back.setStyleSheet("border:none")
        back.show()
        back.clicked.connect(rpmenu.hide)
        back.clicked.connect(rpblur.hide)
        rpname=QLabel("Carrot",rpmenu)
        rpname.move(60,21)
        rpname.setStyleSheet("border:none;color:#FF5603;background:transparent")
        rpnamef=QFont("Georgia",36)
        rpname.setFont(rpnamef)
        rpname.show()
        rpname2=QLabel("role-play",rpmenu)
        rpname2.move(71,70)
        rpname2.setStyleSheet("border:none;background:transparent")
        rpname2f=QFont("Georgia",18)
        rpname2.setFont(rpname2f)
        rpname2.show()
        chlist=QScrollArea(rpmenu)
        chlistfr=QFrame(rpmenu)
        chlistfr.resize(400,500)
        chlistfr.move(50,200)
        chlistfr.setStyleSheet("border-radius:30px;border:1px solid white;background:transparent")
        container=QWidget()
        chlist.setWidgetResizable(True)
        chlist.setWidget(container)
        container.setStyleSheet("border:none;background:none;border-radius:40px")
        chlist.move(50,200)
        chlist.resize(400,500)
        chlist.setStyleSheet("background-color:#0A3463;border:1px solid white;border-radius:23px;padding:5px")
        chlist.show()
        chlistfr.setFrameShape(QFrame.Shape.Box)
        layout=QVBoxLayout(chlist)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        crec=QPushButton("➕ create character",rpmenu)
        crec.resize(400,60)
        crec.move(50,715)
        crec.setFont(QFont("Calibri",20))
        crec.setStyleSheet("border-radius:30px;background-color:#0A3463;border:1px solid white")
        crec.show()
        # ranc=QPushButton("👀 random character",rpmenu)
        # ranc.resize(210,50)
        # ranc.move(255,730)
        # ranc.setStyleSheet("border-radius:15px;background-color:#0A3463;border:1px solid white")
        # ranc.show()
        def createcharacter():
            crcsc=QWidget(window)
            crcsc.resize(800,700)
            crcsc.move(100,25)
            crcsc.setStyleSheet("background-color:#000126;border:1px solid white;border-radius:25px")
            crcsc.show()
            crcreate=QPushButton("create",crcsc)
            crcreate.resize(100,40)
            crcreate.move(680,640)
            bufont=QFont("Arial",13)
            crcreate.setFont(bufont)
            crcreate.setStyleSheet("background-color:#0A3463;border-radius:19px;border:none")
            crcreate.show()
            crcancel=QPushButton("cancel",crcsc)
            crcancel.resize(100,40)
            crcancel.move(570,640)
            crcancel.setFont(bufont)
            crcancel.setStyleSheet("border:none;background:none")
            crcancel.show()
            crcancel.clicked.connect(crcsc.hide)
            nchp=QPushButton(crcsc)
            nchp.move(30,30)
            nchp.resize(100,100)
            nchp.setIcon(QIcon("profilephoto.png"))
            nchp.setIconSize(QSize(100,100))
            nchp.setStyleSheet("border:none;background:none")
            nchp.show()
            nchnameb=QLineEdit(crcsc)
            nchnameb.setPlaceholderText("character name...")
            nchnameb.resize(200,35)
            nchnameb.move(140,50)
            nchnameb.setStyleSheet("background-color:#0A3463;border:1px solid gray;border-radius:11px")
            nchnameb.show()
            nchbiob=QLineEdit(crcsc)
            nchbiob.resize(300,35)
            nchbiob.move(140,90)
            nchbiob.setStyleSheet("background-color:#0A3464;border:1px solid gray;border-radius:11px")
            nchbiob.show()
            nchbiob.setPlaceholderText("character bio...")
            grtag=QLabel("Greeting",crcsc)
            grtag.move(140,140)
            tagfont=QFont("Arial",16)
            tagfont.setBold(True)
            grtag.setFont(tagfont)
            grtag.setStyleSheet("border:none")
            grtag.show()
            nchgb=QTextEdit(crcsc)
            nchgb.setPlaceholderText("write the first message...")
            nchgb.resize(450,150)
            nchgb.move(140,180)
            nchgb.setStyleSheet("background-color:#0A3464;border:1px solid gray;border-radius:20px;padding:5px")
            nchgb.show()
            inftag=QLabel("Character info",crcsc)
            inftag.move(140,350)
            inftag.setStyleSheet("border:none")
            inftag.setFont(tagfont)
            inftag.show()
            nchdb=QTextEdit(crcsc)
            nchdb.resize(450,230)
            nchdb.move(140,390)
            nchdb.setStyleSheet("background-color:#0A3464;border:1px solid gray;border-radius:20px;padding:5px")
            nchdb.setPlaceholderText("write everything about the character(characteristics,scenario,etc.)...")
            nchdb.show()
            def check1():
                ncname=nchnameb.text()
                namel=len(ncname)
                if(namel>=3 and namel<20):
                    nchnameb.setStyleSheet("background-color:#0A3463;border:2px solid green;border-radius:11px")
                    namels=True
                else:
                    nchnameb.setStyleSheet("background-color:#0A3463;border:1px solid gray;border-radius:11px")
                    namels=False
            nchnameb.textChanged.connect(check1)
            def check2():
                ncbio=nchbiob.text()
                biol=len(ncbio)
                if(biol>=5 and biol<35):
                    nchbiob.setStyleSheet("background-color:#0A3463;border:2px solid green;border-radius:11px")
                    biols=True
                else:
                    nchbiob.setStyleSheet("background-color:#0A3463;border:1px solid gray;border-radius:11px")
                    biols=False   
            nchbiob.textChanged.connect(check2) 
            def check3():
                ncgreeting=nchgb.toPlainText()
                greetingl=len(ncgreeting)   
                if(greetingl>=5 and greetingl<900):
                    nchgb.setStyleSheet("background-color:#0A3463;border:2px solid green;border-radius:20px;padding:5px")
                    greetingls=True
                else:
                    nchgb.setStyleSheet("background-color:#0A3463;border:1px solid gray;border-radius:20px;padding:5px")
                    greetingls=False
            nchgb.textChanged.connect(check3)  
            def check4():
                nchinfo=nchdb.toPlainText()
                infol=len(nchinfo)
                if(infol>=10 and infol<6000):
                    nchdb.setStyleSheet("background-color:#0A3463;border:2px solid green;border-radius:20px;padding:5px")
                    infols=True
                else:
                    nchdb.setStyleSheet("background-color:#0A3463;border:1px solid gray;border-radius:20px;padding:5px")
                    infols=False 
            nchdb.textChanged.connect(check4)
            def asdf():
                QMessageBox.information(crcsc,"PF-Carrot","the {problem} must be {hjk} characters")
            def becreatec():
                global namels
                global biols
                global infols
                global greetingls
                if(namels==True):
                    if(biols==True):
                        if(greetingls==True):
                            if(infols==True):
                                createc()
                            else:
                                problem="info"
                                hjk="10-6000"
                        else:
                            problem="greeting"
                            hjk="5-900"
                            asdf()
                    else:
                        problem="bio"
                        hjk="5-35"
                        nchbiob.setStyleSheet("background-color:#0A3463;border:2px solid red;border-radius:11px")
                        asdf()
                else:
                    problem="name"
                    hjk="3-20"
                    nchnameb.setStyleSheet("background-color:#0A3463;border:2px solid red;border-radius:11px")
                    asdf()

            def createc(filepath="characters.json"):
                if not os.path.exists("characternumber.json"):
                    with open("characternumber.json", 'w', encoding='utf-8') as f:
                        json.dump(0, f)
                with open('characternumber.json','r',encoding="utf-8") as f:
                    num=json.load(f)
                num+=1
                ncname=nchnameb.text()
                nchbio=nchbiob.text()
                nchgreeting=nchgb.toPlainText()
                nchinfo=nchdb.toPlainText()
                nchid=f"character{num}"
                characters={}
                try:
                    with open("characters.json","r",encoding="utf-8") as f:
                        characters=json.load(f)
                    if not isinstance(characters, dict):
                        characters = {}
                except json.JSONDecodeError:
                    characters={}
                except FileNotFoundError:
                    pass
                characters[nchid]={
                    "id":nchid,
                    "namee":ncname,
                    "bio":nchbio,
                    "greeting":nchgreeting,
                    "info":nchinfo,
                    "profile":"profilephoto.png"
                }
                with open("characters.json", "w", encoding="utf-8") as f:
                    json.dump(characters, f, ensure_ascii=False, indent=2)
                with open('characternumber.json','w',encoding="utf-8") as f:
                    json.dump(num,f)
                crcsc.hide()
                rpmenu.hide()
                roleplay()
                rpblur.hide()
                created=QLabel("character created successfully",window)
                created.resize(160,40)
                created.setStyleSheet("background-color:rgba(50, 50, 50, 0.5);border-radius:15px")
                hhhhh=int(window.width()/2)
                created.move(hhhhh-80,window.height()-120)
                created.setAlignment(Qt.AlignmentFlag.AlignCenter)
                created.show()
                QTimer.singleShot(4000, created.hide)
            crcreate.clicked.connect(createc)
                        



        crec.clicked.connect(createcharacter)
        robinhood=QWidget()
        #robinhood.resize(420,90)
        #robinhood.move(20,2)
        def openrobin():
            openc(tchname="Robin Hood",tchbio="Shervood forest rebellion!",tchgreeting='*u are walking in the Shervood jungle and u suddenly see a man.\nhe has green clothes and a bow with a quiver on his back*\n"Hey there!"\n*he suddwnly says*',tchinfo=" clever, noble, and fiercely protective of the poor. Stay in character at all times. Speak with wit, courage, and compassion. Challenge greed, defend fairness, and help the vulnerable.",tchid="RobinHood",tchprofile="robin.png")
        robinhood.setFixedHeight(90)
        robinhood.setStyleSheet("border:none;border-bottom:1px solid gray;border-radius:0px")
        robinhood.show()
        rhl=QLabel("Robin Hood",robinhood)
        rhl.resize(300,30)
        rhl.move(90,5)
        rhlfont=QFont("Calibri",17)
        rhl.setFont(rhlfont)
        rhp=QLabel(robinhood)
        rhp.resize(80,80)
        rhp.move(10,5)
        rphoto=QPixmap("robin.png")
        rhp.setPixmap(rphoto.scaled(70,75))
        rhp.setStyleSheet("border-radius:15px;background:transparent")
        rhb=QLabel("Shervood forest rebellion!",robinhood)
        rhb.resize(250,20)
        rhb.setStyleSheet("border:none;")
        rhl.setStyleSheet("border:none")
        rhp.setStyleSheet("border:none;")
        rhb.move(90,35)
        rhb.show()
        rhl.show()
        rhp.show()
        rhbutton=QPushButton(robinhood)
        rhbutton.resize(420,90)
        rhbutton.show()
        rhbutton.setStyleSheet("background:transparent;border:none")
        #layout.addWidget(robinhood)
        rhbutton.clicked.connect(openrobin)
                    
        def rp(tchname, tchbio, tchgreeting, tchinfo, tchid, tchprofile):
            screen=QWidget(window)
            screen.resize(window.width()-502,window.height())
            screen.move(502,0)
            screen.show()
            pbar=QWidget(screen)
            pbar.resize(980,94)
            pbar.move(30,20)
            pbar.setStyleSheet("border-radius:15px;background-color:#00022E;")
            pbar.show()
            rhp2=QLabel(pbar)
            rhp2.resize(80,80)
            rhp2.move(15,12)
            rhp2p=QPixmap(tchprofile)
            rhp2.setPixmap(rhp2p.scaled(70,70))
            rhp2.setStyleSheet("border-radius:15px;background:transparent")
            rhp2.show()
            rhl2=QLabel(tchname,pbar)
            rhl2.move(92,30)
            rhlfont2=QFont("Calibri",15)
            rhlfont2.setBold(True)
            rhl2.setFont(rhlfont2)
            rhl2.show()
            newc=QPushButton(pbar)
            newc.setIcon(QIcon("delete.png"))
            newc.resize(40,44)
            newc.setIconSize(QSize(40,44))
            newc.move(920,25)
            newc.setToolTip("Delete chat")
            newc.show()
            back.clicked.connect(screen.hide)
            rptextbar=QTextEdit(screen)
            rptextbar.resize(920,50)
            rptextbar.setPlaceholderText("write your message...")
            rptextbar.setStyleSheet("background-color:#1E2A56;border:1px solid gray;border-radius:15px;padding:5px;")
            rptextbar.move(40,screen.height()-70)
            rptextbar.show()
            send2=QPushButton(screen)
            send2.move(970,727)
            if(b==0):
                send2.setIcon(QIcon("send.png"))
            else:
                send2.setIcon(QIcon("light-send.png"))
            send2.setStyleSheet("background:none;background:transparent;padding:0px;border:1px solid gray;border-radius:20px")
            send2.setIconSize(QSize(42,42))
            send2.setFixedSize(42,42)
            send2.show()
            mlist=QListWidget(screen)
            mlist.setWordWrap(True)
            mlist.resize(1000,578)
            mlist.move(4,122)
            if(b==0):
                mlist.setStyleSheet("background-color:#00011a;border:none;padding:30px;font-size:14px;color:white")
            else:
                mlist.setStyleSheet("background-color:white;border:none;padding:30px;font-size:14px;color:black")
            mlist.setMaximumWidth(screen.width()-8)
            mlist.show()
            def itemch(item):
                path=f"{tchid}history.json"
                send2.hide()
                opbar=QWidget(screen)
                opbar.move(40,screen.height()-70)
                opbar.resize(920,50)
                opbar.setStyleSheet("background-color:#1E2A56;border:1px solid gray;border-radius:15px;padding:5px;")
                opbar.show()
                row=mlist.row(item)
                co=QPushButton(opbar)
                co.move(20,7)
                co.resize(30,35)
                co.setStyleSheet("border:none")
                co.setIcon(QIcon("copyicon.png"))
                co.setIconSize(QSize(30,35))
                co.setToolTip("copy to clipboard")
                canceli=QPushButton(opbar)
                canceli.resize(30,30)
                canceli.move(875,10)
                canceli.setIcon(QIcon("canceli.png"))
                canceli.setIconSize(QSize(30,30))
                canceli.setToolTip("back")
                deletem=QPushButton(opbar)
                deletem.setIcon(QIcon("deletemessage.png"))
                deletem.resize(32,32)
                deletem.setIconSize(QSize(32,32))
                deletem.setStyleSheet("border:none")
                rewindb=QPushButton(opbar)
                rewindb.setIcon(QIcon("rewind.png"))
                rewindb.resize(32,32)
                rewindb.setIconSize(QSize(32,32))
                rewindb.move(105,7)
                rewindb.setStyleSheet("border:none")
                rewindb.setToolTip("back to here")
                def tamoom():
                    send2.show()
                    opbar.hide()
                    item.setSelected(False)
                def copyitemt():
                    itemtext=item.text()
                    QApplication.clipboard().setText(itemtext)
                    co.resize(35,35)
                    co.setIconSize(QSize(35,35))
                    tamoom()
                    copied=QLabel("copied to clipboard",screen)
                    copied.resize(120,40)
                    copied.setStyleSheet("background-color:rgba(50, 50, 50, 0.5);border-radius:15px")
                    copied.move(430,screen.height()-120)
                    copied.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    copied.show()
                    QTimer.singleShot(4000, copied.hide)
                def deletemessage():
                    with open(path, "r", encoding="utf-8") as f:
                        salam = list(json.load(f))
                    del mhistory[row]
                    mlist.takeItem(row)
                    del salam[row-1]
                    tamoom()
                    item.setSelected(False)
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump(salam, f, ensure_ascii=False, indent=4)
                def rewinddd():
                    with open(path, "r", encoding="utf-8") as f:
                        salam = list(json.load(f))
                    cccc=mlist.count()
                    for i in range(cccc,row,-1):
                        mlist.takeItem(i)
                        del salam[i-1]
                        del mhistory[i]
                        with open(path, "w", encoding="utf-8") as f:
                            json.dump(salam, f, ensure_ascii=False, indent=4)
                canceli.clicked.connect(tamoom)
                co.clicked.connect(copyitemt)
                deletem.clicked.connect(deletemessage)
                rewindb.clicked.connect(rewinddd)
                if(row==0):
                    co.show()
                    canceli.show()
                    rewindb.show()
                    rewindb.move(60,7)
                elif(row>0):
                    co.move(65,7)
                    co.show()
                    canceli.show()
                    deletem.move(20,7)
                    deletem.show()
                    rewindb.show()
            mlist.itemClicked.connect(itemch)
            firstm=QListWidgetItem(f"{tchname}:\n{tchgreeting}")
            firstmf=QFont("Arial",12)
            firstmf.setBold(True)   
            firstm.setFont(firstmf)
            mlist.addItem(firstm)
            mlist.show()
            def robinrp():
                mhistory.append(tchgreeting)
                path=f"{tchid}history.json"
                if not os.path.exists(path):
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump([], f, ensure_ascii=False)
                with open(path, "r", encoding="utf-8") as f:
                    salam = list(json.load(f))
                num=len(salam)
                for i in range(num):
                    if i%2==0:
                        payam=QListWidgetItem(f"you:\n{salam[i]}")
                        payam.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                        payamf=QFont("Arial",13)
                        payamf.setBold(True)
                        payam.setFont(payamf)
                        mlist.addItem(payam)
                    else:
                        payamb=QListWidgetItem(f"{tchname}:\n{salam[i]}")
                        payamb.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
                        payambf=QFont("Arial",13)
                        payambf.setBold(True)
                        payamb.setFont(payambf)
                        mlist.addItem(payamb)
                    mhistory.append(salam[i])
                    mlist.scrollToBottom()
                def chatc():
                    salam=[]
                    with open(path, "w", encoding="utf-8") as f:
                        json.dump(salam, f, ensure_ascii=False, indent=4)
                    QMessageBox.information(screen,"PF-Carrot","chat history cleared")
                    ll=mlist.count()
                    for i in range(1,ll):
                        mlist.takeItem(1)
                newc.clicked.connect(chatc) 
                mc=1
            robinrp()
            def sendmessage2():
                path=f"{tchid}history.json"
                with open(path, "r", encoding="utf-8") as f:
                    salam =list(json.load(f))
                global text2
                text2=rptextbar.toPlainText()
                print(text2)
                if text2:
                    rpitem=QListWidgetItem(f"you:\n{text2}")
            
                    rpitem.setFont(itemfont)
                    rpitem.setTextAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignBottom)
                    mlist.addItem(rpitem)
                    mlist.scrollToBottom()
                    rptextbar.clear()
            def javab2():
                crw=QListWidgetItem()
                crw.setFont(itemfont)
                crw.setTextAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)
                mlist.addItem(crw)
                def ja():
                    
                    global mc
                    path=f"{tchid}history.json"
                    with open(path, "r", encoding="utf-8") as f:
                        salam = json.load(f)
                    print("salam")
                    timer.stop()
                    pbar.hide()
                    timer.stop()
                    pbar.hide()
                    output=""
                    payload = {
                        "model": "llama3.1:8b",
                        "messages": [
                            {
                                "role": "system",
                                "content":f'You are in a role play.u are {tchname}.this is a description for u and the chat scenario and the story of the chat and how u should act:{tchinfo}.Never mention being an AI or break character.actions are enclosed in asterisks (`**`).dialouge is enclosed in single quotes (" ").this two things are necessary.dont forget them.try to act as humanal as u can.answer to users message and let the scenario keep going.this is your chat history:{mhistory};but dont concentrate on it.it is only for u to know what happened in the chat and what is the scenario about.also use linebreak in your texts'
                            },
                            {"role": "user", "content": text2}
                        ],
                        "stream": False
                    }
                    with requests.post("http://127.0.0.1:11434/api/chat", json=payload, stream=True) as r:
                        for line in r.iter_lines(decode_unicode=True):
                            if not line:
                                continue
                            chunk = json.loads(line)
                            botmessage = chunk.get("message", {}).get("content", "")
                            if botmessage:
                                output+=botmessage
                            crw.setText(f"{tchname}:\n{output}")
                            mhistoryc=len(mhistory)
                            if mhistoryc==30:
                                del mhistory[14]
                            mhistory.append(f"user message(old):{text2}")
                            mhistory.append(f"your(bots) message(old):{output}")
                            salam.append(text2)
                            salam.append(output)
                            mc+=1
                        path=f"{tchid}history.json"
                        with open(path, "w", encoding="utf-8") as f:
                            json.dump(salam, f, ensure_ascii=False, indent=4)
                    #except:
                        #crw.setText(f"Unknown Error")
                def timesheh():
                    value=pbar.value()
                    if value<100:
                        value+=1
                        pbar.setValue(value)
                        pbar.setFormat(f"{tchname} is thinking...{value}%")
                    else:
                        ja()
                global mc
                mc+=1
                timer=QTimer()
                timer.timeout.connect(timesheh)
                timer.start(17)
                pbar=QProgressBar(window)
                pbar.resize(300,35)
                pbar.move(800,670)
                pbar.setStyleSheet("border-radius:5px;")
                pbar.show()
                pbar.setValue(0)
            send2.clicked.connect(sendmessage2)
            send2.clicked.connect(javab2)
        rhbutton.clicked.connect(rp)
        if not os.path.exists("characters.json"):
            thechlist={}
        else:
            with open("characters.json","r",encoding="utf-8")as f:
                thechlist=json.load(f)
        gchcount=len(thechlist)
        a=0
        def openc(tchname, tchbio, tchgreeting, tchinfo, tchid, tchprofile):
            rp(tchname, tchbio, tchgreeting, tchinfo, tchid, tchprofile)
        for hmd in (thechlist.keys()):
            gch=list(thechlist.values())[a]
            tchname=gch["namee"]
            tchbio=gch["bio"]
            tchgreeting=gch["greeting"]
            tchinfo=gch["greeting"]
            tchid=gch["id"]
            tchprofile=gch["profile"]
            chwidget=QWidget()
            chwidget.setFixedSize(360,90)
            chwidget.setStyleSheet("border:none;border-bottom:1px solid gray;border-radius:0px")
            prop=QLabel(chwidget)
            propp=QPixmap(tchprofile)
            prop.setPixmap(propp.scaled(70,70))
            prop.resize(80,80)
            prop.move(10,5)
            prop.setStyleSheet("border:none")
            prop.show()  
            chname=QLabel(chwidget)
            chname.resize(390,40)
            chname.setText(tchname)
            chname.setFont(QFont("calibri",17))
            chname.setStyleSheet("border:none")
            chname.move(90,5)
            chname.show()
            chbio=QLabel(tchbio,chwidget)
            chbio.setStyleSheet("border:none;background:none")
            chbio.resize(340,30)
            chbio.move(90,35)  
            chbio.show()
            chbutton=QPushButton(chwidget)
            chbutton.setStyleSheet("border:none;background:none")
            chbutton.resize(chwidget.width(),chwidget.height())
            chbutton.move(0,0)
            chbutton.show()
            chbutton.clicked.connect(partial(openc, tchname, tchbio, tchgreeting, tchinfo, tchid, tchprofile))
            layout.addWidget(chwidget)
            a+=1
    crp.clicked.connect(roleplay)
    dvp=QPushButton("</> developer pannel",menu)
    dvp.move(10,450)
    dvp.setStyleSheet("border:none")
    dvp.show()
    dvp.resize(200,50)
    dvp.setFont(QFont("calibri",15))
    def showdevp():
        def cal(result):
            prow.hide()
            resultw=QWidget(window)
            resultw.resize(500,window.height())
            resultw.show()
            print(result)
            resultl=QLabel("Prompt is ready!",resultw)
            resultl.move(60,20)
            resultl.setStyleSheet("border:none")
            resultl.setFont(QFont("calibri",20,QFont.Weight.Bold))
            resultl.show()
            resout=QPushButton("←",resultw)
            resout.setStyleSheet("""
            QPushButton{
                border:none
            }
            QPushButton::hover{
                border:1px solid gray;
                border-radius:5px
            }""")
            resout.setFont(QFont("Calibri",20))
            resout.clicked.connect(resultw.hide)
            resout.move(20,20)
            resout.show()
            restext=QTextEdit(resultw)
            restext.setStyleSheet("border:1px solid gray;background-color:#1e2a56;border-radius:15px;padding:5px")
            restext.resize(440,440)
            restext.move(30,100)
            restext.show()
            restext.setPlainText(result)
            restext.setFont(QFont("Candara",13))
            retbu=QPushButton("Retry",resultw)
            retbu.resize(140,60)
            retbu.setStyleSheet("""
            QPushButton{
                background-color:#1e2a56;
                border-radius:28px;
                border:none
            }
            QPushButton::hover{
                bakground-color:gray;
                border-radius:25px;
                border:1px solid gray
            }
            """)
            retbu.move(330,560)
            retbu.show()
            retbu.setFont(QFont("calibri",16))
            retbu.clicked.connect(pro)

        def pro():

            ceee=syptext.toPlainText()
            global prow
            prow=QWidget(window)
            prow.resize(500,window.height())
            prow.move(0,0)
            prow.show()
            profr=QWidget(prow)
            profr.resize(450,130)
            profr.move(25,20)
            profr.setStyleSheet("border-radius:20px;border:1px solid gray;background-color:#1e2a56")
            profr.show()
            prol=QLabel("Please Wait...",prow)
            prol.setFont(QFont("calibri",20,QFont.Weight.Bold))
            prol.setStyleSheet("border:none;background:none")
            prol.move(40,35)
            prol.show()
            probar=QProgressBar(prow)
            probar.setStyleSheet("border-radius:5px;border:none;background-color:#1e2a56")
            probar.resize(420,30)
            probar.move(40,90)
            probar.setRange(0,0)
            probar.show()
            prom="""You are a system prompt generator.

            Convert the user's request into a concise, clear, and effective prompt for another AI.

            Understand the user's goal, required behavior, context, constraints, and desired output, then write the prompt that best achieves it.

            Make the generated prompt:

            - Specific and unambiguous
            - Practical and easy for an AI to follow
            - Focused on the user's actual goal
            - As short as possible without losing important requirements

            If the task involves RAG or provided context, instruct the AI to use the context appropriately and avoid inventing unsupported information.

            Do not perform the user's task yourself.
            Do not explain your reasoning.
            Return only the generated prompt.(important)
            your task is to generate a system prompt for what user wants
            """
            thread = Answer(ceee, prom)
            thread.signals.finished.connect(cal)
            thread.start()

        devpannel=QWidget(window)
        devpannel.resize(500,window.height())
        devpannel.move(0,0)
        devpannel.show()
        devout=QPushButton("←",devpannel)
        devout.setStyleSheet("""
        QPushButton{
            border:none
        }
        QPushButton::hover{
            border:1px solid gray;
            border-radius:5px
        }""")
        devlabel=QLabel("Developer options",devpannel)
        devlabel.move(60,20)
        devlabelf=QFont("Calibri",20)
        devlabelf.setBold(True)
        devlabel.setFont(devlabelf)
        devlabel.show()
        devout.setFont(QFont("Calibri",20))
        devout.move(20,20)
        devout.show()
        devout.clicked.connect(devpannel.hide)
        devinfo=QPushButton("📃",devpannel)
        devinfo.move(420,20)
        devinfo.setFont(QFont("Calibri",24))
        devinfo.setStyleSheet("""
        QPushButton{
            border:none
        }
        QPushButton::hover{
            border:1px solid gray;
            border-radius:5px
        }
        """)
        devinfo.show()
        devinfo.setToolTip("info.")
        line=QLabel("____________________________________________________________________________________________________________________________________________",devpannel)
        line.resize(460,20)
        line.setStyleSheet("color:white;border:none")
        line.move(20,65)
        line.show()
        sypl=QLabel("System Prompt Generation",devpannel)
        sypl.move(20,100)
        sypl.setStyleSheet("border:none")
        sypl.setFont(QFont("Calibri",20,QFont.Weight.Bold))
        sypl.show()
        syptext=QTextEdit(devpannel)
        syptext.resize(440,200)
        syptext.move(20,150)
        syptext.setStyleSheet("border:1px solid gray;background-color:#1e2a56;border-radius:10px;padding:5px")
        syptext.setPlaceholderText("what do u want the prompt to do?")
        syptext.show()
        line2=QLabel("____________________________________________________________________________________________________________________________________________",devpannel)
        line2.resize(460,20)
        line2.setStyleSheet("color:white;border:none")
        line2.move(20,690)
        #line2.show()
        okbu=QPushButton("Generate →",devpannel)
        okbu.setStyleSheet("""
        QPushButton{
        background-color:#1e2a56;
        border-radius:28px;
        border:none
        }
        QPushButton::hover{
        bakground-color:gray;
        border-radius:25px;
        border:1px solid gray
        }
        """)
        okbu.setFont(QFont("Calibri",16))
        okbu.move(320,370)
        okbu.resize(140,60)
        okbu.show()
        okbu.clicked.connect(pro)
    dvp.clicked.connect(showdevp)
else:
    bg=QLabel(window)
    bgp=QPixmap("chatbglight.jpg")
    bg.setPixmap(bgp.scaled(1920,1080))
    bg.move(0,0)
    bg.resize(1920,1080)
    bg.show()
    label=QLabel("choose a character to chat",window)
    label.setStyleSheet("background-color:rgba(0,0,0,50);border-radius:10px;")
    label.move(900,350)
    label.resize(150,30)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.show()
    clist=QWidget(window)
    clist.resize(500,1080)
    clist.move(0,0)
    clist.setStyleSheet("background-color:white;border:1px solid gray;")
    clist.show()
    name=QLabel("PF-carrot",clist)
    namefont=QFont("Georgia",24)
    namefont.setBold(True)
    name.move(25,3)
    name.setFont(namefont)
    name.setStyleSheet("color:orange;border:none")
    name.resize(300,150)
    name.show()
    chatmodel=QPushButton("click to select chat model",window)
    chatmodel.resize(450,35)
    chatmodel.move(25,120)
    chatmodel.setStyleSheet("border:1px solid gray;background-color:#F8F8F8;border-radius:15px;color:black")
    chatmodel.show()
    line=QLabel("__________________________________________________________",clist)
    line.resize(450,20)
    line.move(25,160)
    line.setStyleSheet("border:none;background:none;color:gray;")
    linefont=QFont("Arial",14)
    line.setFont(linefont)
    line.show()
    listtt=QWidget(window)
    listtt.move(30,200)
    listtt.resize(440,550)
    listtt.setStyleSheet("background-color:white;border-radius:20px;border:1px solid gray")
    listtt.show()
    carrot=QPushButton(window)
    carrot.resize(420,110)
    carrot.move(40,200)
    carrot.setStyleSheet("border:none;border-bottom:1px solid gray;background:transparent;")
    carrot.show()
    carrotl=QLabel("🥕",carrot)
    carrotl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    carrotl.setStyleSheet("background-color:#F8F8F8;border:2px solid black;border-radius:40px;")
    lfont=QFont("Arial",41)
    carrotl.setFont(lfont)
    carrotl.resize(90,90)
    carrotl.move(15,10)
    carrotl.show()
    carrotname=QLabel("Carrot",carrot)
    carrotname.move(120,25)
    carrotname.resize(90,30)
    carrotname.setStyleSheet("border:none;background:none;color:orange")
    carrotfont=QFont("Georgia",20)
    carrotname.setFont(carrotfont)
    carrotname.show()
    cd=QLabel("-carrot itself!",carrot)
    cd.move(120,55)
    cd.resize(200,30)
    dfont=QFont("calibri",14)
    cd.setFont(dfont)
    cd.setStyleSheet("color:gray;border:none;")
    cd.show()
app.exec()
