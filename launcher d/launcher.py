from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from configparser import ConfigParser
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from switch import DeSwitch
import subprocess
import sys
import os

app = QApplication(sys.argv)

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

config = ConfigParser()
config.read(os.path.join(BASE_DIR, "Settings.ini"))
show = config.getboolean("Settings", "show")
print(show)

widget = QWidget()
widget.setWindowTitle("PF-Carrot launcher")
widget.resize(850, 600)
widget.setStyleSheet("background-color:#00011a")
widget.show()

chapl = QLabel("Chat App", widget)
chapl.move(30, 20)
chapl.setStyleSheet("border:none;color:white")
labfont = QFont("Calibri", 24)
labfont.setBold(True)
chapl.setFont(labfont)
chapl.show()

chapw = QWidget(widget)
chapw.setStyleSheet("background-color:#00011a;BORDER:2px solid white;border-radius:30px")
chapw.resize(380, 510)
chapw.move(30, 70)
chapw.show()

chapl2 = QLabel(
    "In our chat application,u can chat with diffrent AI models including "
    "Gemma3:1b,Gemma3:4b,llama3.1:8b,Gemma3:12b and Qwen3:14b.\n \n"
    "u will have access to diffrent chat features like choosing character "
    "for the bot and setting your own character.\n \n"
    "There is even a part for role-playing with AI characters in the app\n \n"
    "Carrot is waiting to talk to u!",
    chapw
)
chapl2.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
chapl2.setStyleSheet("color:white;border:none")
chapl2.setWordWrap(True)
chapl2.resize(320, 470)
chapl2.move(20, 20)
chapl2f = QFont("Calibri", 16)
chapl2.setFont(chapl2f)
chapl2.show()

chapp = QPushButton("Open The Chat App", chapw)
chapp.setFont(chapl2f)
chapp.setStyleSheet("background-color:#0A3463;border-radius:25px;border:none")
chapp.resize(350, 50)
chapp.move(15, 440)
chapp.show()

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

chapp.clicked.connect(openapp)

assl = QLabel("Assistant", widget)
assl.setFont(labfont)
assl.setStyleSheet("color:white")
assl.move(440, 20)
assl.show()

assw = QWidget(widget)
assw.setStyleSheet("background-color:#00011a;BORDER:2px solid white;border-radius:30px")
assw.resize(380, 510)
assw.move(440, 70)
assw.show()

assl2 = QLabel(
    "Carrot assistant app,lets u to use AI anywhere without even leaving the page."
    "u can use it to summarize a long message,rewrite your text,"
    "understand a complicated scientific text,and etc.\n \n"
    "for using all this features,u only need to select the text and press ctrl + c + m\n \n"
    "But before that,please activate the assistant ↓",
    assw
)
assl2.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
assl2.setStyleSheet("color:white;border:none")
assl2.setWordWrap(True)
assl2.resize(330, 470)
assl2.move(20, 20)
assl2.setFont(chapl2f)
assl2.show()

activatel = QLabel("Assistant", assw)
activatel.setStyleSheet("color:white;border:none")
acf = QFont("Calibri", 18)
acf.setBold(True)
activatel.setFont(acf)
activatel.move(20, 340)
activatel.show()

activateb = DeSwitch(assw)
activateb.show()

if show:
    activateb.setChecked(True)
    if getattr(sys, "frozen", False):
        subprocess.Popen([
            os.path.join(BASE_DIR, "C-Assistant.exe")
        ])
    else:
        subprocess.Popen([
            sys.executable,
            os.path.join(BASE_DIR, "assistant.py")
        ])
else:
    activateb.setChecked(False)

def clicked():
    if not activateb.isChecked():
        activateb.setChecked(True)
        config["Settings"]["show"] = "true"
        with open(os.path.join(BASE_DIR, "Settings.ini"), "w") as f:
            config.write(f)
    else:
        activateb.setChecked(False)
        config["Settings"]["show"] = "false"
        with open(os.path.join(BASE_DIR, "Settings.ini"), "w") as f:
            config.write(f)

activateb.clicked.connect(clicked)
activateb.move(120, 340)
activateb.setToolTip("activate the assistant")
activateb.setColors(
    active="#1d4ed8"
)

app.exec()
