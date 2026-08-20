import requests
from threading import Thread
from PyQt6.QtCore import pyqtSignal, QObject

class AnswerSignals(QObject):
    finished = pyqtSignal(str)


class Answer(Thread):
    def __init__(self,message,command):
        super().__init__(daemon=True)
        self.message=message
        self.signals = AnswerSignals()
        self.command=command
        
    def run(self):
        try:
            response=requests.post(
                "http://127.0.0.1:11434/api/chat",
                json={
                    "model":"llama3.1:8b",
                    "messages":[
                        {
                            "role":"system",
                            "content":self.command
                        },
                        {
                            "role":"user",
                            "content":self.message
                        }
                    ],
                    "stream":False
                }
            )
            answer=response.json()["message"]["content"]
        except Exception as e:
            answer=f"Error:{e}(this isnt your fault!)"
        self.signals.finished.emit(answer)