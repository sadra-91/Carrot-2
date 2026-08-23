from PyQt6.QtWidgets import QApplication, QWidget,QPushButton,QLabel,QProgressBar,QScrollArea,QVBoxLayout
from PyQt6.QtCore import Qt,QTimer,QThread,pyqtSignal,QSize
from PyQt6.QtGui import QFont,QIcon
from openai import OpenAI
import subprocess
import requests
import keyboard
import time
import sys

print("salam")
shouldshow=False
ragt=""
ustext=""
apikey=requests.get("https://pf-c.ir/key.txt").text.strip()
client = OpenAI(base_url="https://api.gapgpt.app/v1",api_key=apikey)
app = QApplication(sys.argv)
clipboard=app.clipboard()
lctime = 0
window = QWidget()
window.setWindowFlags(
    Qt.WindowType.FramelessWindowHint |
    Qt.WindowType.WindowStaysOnTopHint |
    Qt.WindowType.Tool
)
window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
window.resize(340, 120)
container = QWidget(window)
container.resize(340, 120)
container.setStyleSheet("""
    background-color: #f8f8f8;
    border: 1px solid gray;
    border-radius: 25px;
""")
container2=QWidget(container)
container2.resize(300,50)
container2.move(20,10)
container2.setStyleSheet("border-radius:20px;background-color:#d3d3d3;border-bottom:1px solid gray;border-top:none;border-right:none;border-left:none")
container2.show()
name=QLabel("PF-Carrot",container2)
name.setStyleSheet("border:none;background:none;color:gray")
namefont=QFont("times new roman",24)
namefont.setBold(True)
name.setFont(namefont)
name.move(10,8)
name.show()
explainb=QPushButton("explain",container)
explainb.setStyleSheet("""
QPushButton{
border:none;
background:none;
color:gray
}
QPushButton:hover{
background-color:#d0d0d0;
border-radius:8px
}""")
buttfont=QFont("Nato Serif",16)
explainb.setFont(buttfont)
explainb.show()
explainb.move(10,70)
summarizeb=QPushButton("summarize",container)
summarizeb.setStyleSheet("""
QPushButton{
border:none;
background:none;
color:gray
}
QPushButton:hover{
background-color:#d0d0d0;
border-radius:8px
}""")
summarizeb.move(90,70)
summarizeb.setFont(buttfont)
summarizeb.show()
rewriteb=QPushButton("rewrite",container)
rewriteb.setFont(buttfont)
rewriteb.move(205,70)
rewriteb.setStyleSheet("""
QPushButton{
border:none;
background:none;
color:gray
}
QPushButton:hover{
background-color:#d0d0d0;
border-radius:8px
}""")
rewriteb.show()
moreb=QPushButton("⋯",container)
moreb.move(290,63)
moreb.setFont(QFont("Nato Serif",28))
moreb.setStyleSheet("""
QPushButton{
border:none;
background:none;
color:gray
}
QPushButton:hover{
background-color:#d0d0d0;
border-radius:8px
}""")
moreb.show()
backb=QPushButton("<",container)
backb.setFont(QFont("calibri",18))
backb.move(5,15)
backb.show()
backb.setStyleSheet("""
QPushButton
{
color:#4B9EFF;
border:none;
background:none
}
QPushButton:hover
{
background-color:#d0d0d0;
border-radius:3px
}
""")
class OllamaThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, systemprompt, userprompt):
        super().__init__()
        self.systemprompt = systemprompt
        self.userprompt = userprompt
    def run(self):
        try:
            response = client.chat.completions.create(
                model="deepseek-v4-flash",
                messages= [
                       {
                           "role": "system",
                        "content": self.systemprompt
                    },
                    {
                        "role": "user",
                        "content": self.userprompt
                    }
                ],
                 stream=False
            
            )


            answer = response.choices[0].message.content

            self.finished.emit(answer)

        except Exception as e:
            self.error.emit(str(e))
def finish(text):
    text=text
    window.resize(340,400)
    container3=QWidget(window)
    container3.resize(340,400)
    container3.setStyleSheet("""
    background-color: #f8f8f8;
    border: 1px solid gray;
    border-radius: 25px;
    """)
    container3.show()
    responsew=QScrollArea(container3)
    responsew.setWidgetResizable(True)
    responsew.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    widget=QWidget()
    buttw=QWidget(container3)
    buttw.resize(300,50)
    buttw.setStyleSheet("border-radius:25px;background-color:#d3d3d3;border-bottom:1px solid gray;border-top:none;border-right:none;border-left:none")
    buttw.move(20,10)
    buttw.show()
    responsew.setWidget(widget)
    responsew.resize(300,305)
    responsew.move(20,80)
    responsew.setStyleSheet("border:none;background:none")
    widget.setStyleSheet("border-radius:25px;background-color:#d3d3d3;border:none")
    responsew.show()
    widget.move(0,50)
    widget.show()
    layout=QVBoxLayout(widget)
    responsel=QLabel(text)
    responsel.setStyleSheet("border:none;background:none;color:gray")
    responsel.setFont(QFont("calibri",15))
    responsel.setWordWrap(True)
    responsel.setMaximumWidth(260)
    layout.addWidget(responsel)
    responsel.adjustSize()
    responsel.move(10,50)
    responselheight=responsel.height()+10
    responsel.setFixedHeight(responselheight)
    copyb=QPushButton(buttw)
    copyb.setStyleSheet("border:1px solid gray;background:none;border-radius:20px")
    copyb.setIcon(QIcon("copy-icon.png"))
    copyb.resize(40,40)
    copyb.setIconSize(QSize(30,30))
    copyb.move(250,5)
    copyb.show()
    def copyr():
        QApplication.clipboard().setText(text)
        copyb.setIcon(QIcon("check.png"))
    copyb.clicked.connect(copyr)
    back=QPushButton("Back",buttw)
    back.move(10,10)
    back.setFont(QFont("calibri",14))
    back.setStyleSheet("""
    QPushButton{
    color:#4b9eff;
    border:none;
    background:none
    }
    QPushButton:hover{
    background-color:#d0d0d0;
    border-radius:3px
    }
    """)
    back.show()
    back.clicked.connect(container3.hide)
    def retryy():
        container3.hide()
        global ragt
        starting(ragt)
    translateb=QPushButton("Retry")
    translateb.clicked.connect(retryy)
    translateb.setStyleSheet("""
    QPushButton{
    color:#4b9eff;
    border:none;
    background:none
    }
    QPushButton:hover{
    background-color:#d0d0d0;
    border-radius:3px
    }
    """)
    translateb.setFont(buttfont)
    layout.addWidget(translateb)
def gotresponse(text):
    global response
    response=text
    print(response)
    finish(text)
def goterror(err):
    print(err)
def starting(rag):
    waitw=QWidget(window)
    waitw.resize(340,120)
    waitw.setStyleSheet("border-radius:20px;background-color:#d3d3d3;border-bottom:1px solid gray;border-top:none;border-right:none;border-left:none")
    waitw.show()
    waitl=QLabel("Please wait...",waitw)
    waitl.setFont(QFont("Nato Serif",16))
    waitl.setStyleSheet("background:none;border:none;color:gray")
    waitl.move(20,20)
    waitl.show()
    progress=QProgressBar(waitw)
    progress.setStyleSheet("border-radius:5px;border:none")
    progress.resize(300,30)
    progress.move(20,80)
    progress.setRange(0,0)
    progress.show()
    global ustext
    ustext=clipboard.text()
    global thread
    thread = OllamaThread(
        rag,
        ustext
    )
    thread.finished.connect(gotresponse)
    thread.finished.connect(waitw.hide)
    thread.error.connect(goterror)

    thread.start()
sumrag=("""You summarize text.

rules:

1-Return only the summary.

2-Keep the same language as the input(important)

3-Make the summary short, natural, and easy to understand.

4-Keep the main ideas and important details. Remove unnecessary information.""")
summarizeb.clicked.connect(lambda:starting(sumrag))
def ragiss():
    global ragt
    ragt=sumrag
summarizeb.clicked.connect(ragiss)
explainrag=("""You are a text explanation engine.

Explain the input text in a simple and easy-to-understand way.

Rules:

1-Return only the explanation.
2-Use the same language as the input.this is very important
3-Make the explanation clear, natural, and easy to understand.
4-Preserve the original meaning.
5-Do not add information that is not supported by the input.
6-If the input contains technical terms, explain them in simple words.
7-If the input is already simple, rewrite it only if it improves clarity.
""")
explainb.clicked.connect(lambda:starting(explainrag))
def ragisex():
    global ragt
    ragt=explainrag
explainb.clicked.connect(ragisex)
rewriterag=("""You rewrite text.

Rewrite the input to make it clearer, more natural, and easier to read.

Rules:

1-Return only the rewritten text.
2-Use the same language as the input.this is very important
3-Keep the original meaning.
4-Correct grammar, spelling, punctuation, and wording.
5-Improve sentence flow and readability.
6-Do not add new information or remove important details.
6-Keep the style close to the original unless changes improve the writing.
""")
rewriteb.clicked.connect(lambda:starting(rewriterag))
def ragisre():
    global ragt
    ragt=rewriterag
rewriteb.clicked.connect(ragisre)
def showmore():
    window.setFixedWidth(500)
    morewid=QWidget(window)
    morewid.move(350,0)
    morewid.resize(120,90)
    morewid.setStyleSheet("background-color:#f8f8f8;border:1px solid gray;border-radius:15px")
    def hidemore():
        morewid.hide()
        window.resize(340,120)
        hidebbb.hide()
    hidebbb=QPushButton(window)
    hidebbb.setStyleSheet("border:none;background:none")
    hidebbb.resize(340,window.height())
    hidebbb.show()
    hidebbb.clicked.connect(hidemore)
    morewid.show()
    answb=QPushButton("Answer",morewid)
    answb.setStyleSheet("""
QPushButton{
border:none;
background:none;
color:gray
}
QPushButton:hover{
background-color:#d0d0d0;
border-radius:8px
}""")
    answb.setFont(QFont("calibri",18))
    answb.move(20,10)
    answb.show()
    openappb=QPushButton("ask Carrot",morewid)
    openappb.setStyleSheet("""
    QPushButton{
    border:none;
    background:none;
    color:gray
    }
    QPushButton:hover{
    background-color:#d0d0d0;  
    border-radius:8px
    }""")
    openappb.setFont(QFont("calibri",17))
    openappb.move(10,50)
    openappb.show()
    answerp="""
    you have to design an answer for the input
    your answer should be natural
    and your answer should only contain the final answer
    """
    answb.clicked.connect(lambda:starting(answerp))
    def answbbb():
        global ragt
        ragt=answerp
        morewid.hide()
    answb.clicked.connect(answbbb)
    def openapp():
        if getattr(sys, "frozen", False):
            subprocess.Popen([
                os.path.join(BASE_DIR, "PF-Carrot.exe")
            ])
        else:
            subprocess.Popen([
                sys.executable,
                os.path.join(BASE_DIR, "main.py")
            ])
    openappb.clicked.connect(openapp)

chapp.clicked.connect(openapp)

moreb.clicked.connect(showmore)
backb.clicked.connect(window.hide)
def showwindow():
    print("show")
    global shouldshow
    shouldshow=True
def copied():
    global lctime
    lctime = time.time()
    print("Copy detected")
def checkshow():
    if time.time()-lctime<=2:
        showwindow()
    else:
        print("Last copy was more than 2 seconds ago.")
clipboard.dataChanged.connect(copied)
keyboard.add_hotkey("ctrl+m", checkshow)
def check():
    global shouldshow
    if shouldshow==True:
        print("hey")
        window.show()
        window.raise_()
        shouldshow=False
timer = QTimer()
timer.timeout.connect(check)
timer.start(10)

sys.exit(app.exec())
