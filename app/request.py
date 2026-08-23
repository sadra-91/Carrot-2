import requests
from threading import Thread
from openai import OpenAI
from PyQt6.QtCore import pyqtSignal, QObject

apikey=requests.get("https://pf-c.ir/key.txt").text.strip()
client = OpenAI(base_url="https://api.gapgpt.app/v1",api_key=apikey)

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
            response=client.chat.completions.create(
                model="deepseek-v4-flash",
                    messages=[
                        {
                            "role":"system",
                            "content":self.command
                        },
                        {
                            "role":"user",
                            "content":self.message
                        }
                    ],
                    stream=False

            )
            answer=response.choices[0].message.content
        except Exception as e:
            answer=f"Error:{e}(this isnt your fault!)"
        self.signals.finished.emit(answer)
