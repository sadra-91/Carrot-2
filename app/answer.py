import requests
import json
from openai import OpenAI
from threading import Thread
from PyQt6.QtCore import QObject, pyqtSignal

apikey=requests.get("https://pf-c.ir/key.txt").text.strip()
client = OpenAI(base_url="https://api.gapgpt.app/v1",api_key=apikey)
class aianswer(Thread):
    def __init__(self, message, history, callback, streamf, model,replying,retext,charname,charage,charper,charhobbies,persona):
        super().__init__(daemon=True)
        self.message = message
        self.history = history
        self.callback = callback
        self.streamf = streamf
        self.modeln = model
        self.remessage=retext
        self.replying=replying
        self.signals = SignalEmitter()
        self.charname=charname
        self.charhobbies=charhobbies
        self.charage=charage
        self.charper=charper
        self.persona=persona
        if charname=="Carrot":
            self.command1="""You are an AI chatbot named Carrot.

                            Rules:
                            - Be friendly and natural."""
        else:
            self.command1=f"""This is who u are:
                            -{self.charname}"
                            -{self.charage}
                            -{self.charper}
                            -{self.charhobbies}
                            
                            rule:
                            be useful and act natural"""
        if replying==False:
            self.command=f"""
                            - Introduce yourself only if this is the first message of the conversation.
                            - If this is the first message, greet the user.
                            - Otherwise, do not greet the user or introduce yourself again.
                            - Reply only to the latest user message.
                            - Use the chat history only for context and continuity. Do not respond to earlier messages unless the latest message refers to them.
                            -dont repeat anything

                            Chat history:
                            {self.history}
                            """
        elif replying==True:
            self.command=f"""
                and notice that users message is about this message of yours in the chat:
                
                assitant:{self.remessage}
                """

    def run(self):
        messagesl=[
                {
                    "role":"system",
                    "content":self.command1
                },
                {
                    "role": "system",
                    "content":self.command
                }
        ]
        if self.persona!="None":
            personam={
                "role":"system",
                "content":f"This is who user is:{self.persona}"
            }
            print(personam)
            messagesl.append(personam)
        messagesl.append({
            "role": "user",
            "content": f"{self.message}"
        })
        try:
            response = client.chat.completions.create(
                model=self.modeln,
                messages=messagesl,
                stream=True
            )

            answer = ""

            for chunk in response:
                if not chunk.choices:
                    continue

                content = chunk.choices[0].delta.content

                if content:
                    answer += content
                    self.signals.stream.emit(answer)
                    print("STREAM:", answer)


        except Exception as e:
            answer = f"Error:{e}"


        self.signals.finished.emit(answer)



class SignalEmitter(QObject):
    stream = pyqtSignal(str)
    finished = pyqtSignal(str)
