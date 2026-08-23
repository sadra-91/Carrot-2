from PyQt6.QtCore import QThread, pyqtSignal
from openai import OpenAI
import requests


apikey=requests.get("https://pf-c.ir/key.txt").text.strip()
client = OpenAI(base_url="https://api.gapgpt.app/v1",api_key=apikey)

planner_prompt = """
You are an expert image planner.

Your task is to analyze the user's image request and create a detailed visual specification for another AI that will draw the image.

Rules:
- Do not write code.
- Do not explain your reasoning.
- Only describe the final image.

Include:
- Main subject details
- Objects and their positions
- Background
- Colors
- Lighting
- Style
- Composition
- Important visual details

Think like a professional illustrator preparing instructions for another artist.
"""


generator_prompt = """
You are an expert generative graphics programmer.

Create an image based on the detailed image specification provided by the user.

Rules:
- Output ONLY executable Python code.
- Do not write explanations, markdown, or comments outside the code.
- The final result MUST be a Pillow Image object named exactly: image
- Do not call image.save().
- Do not call image.show().

Available libraries:
- Pillow (PIL)
- Cairo / pycairo
- svgwrite
- Python standard libraries (math, random, etc.)

Choose the best tool:
- Use SVG for logos, icons, and vector graphics.
- Use Cairo for advanced 2D rendering, gradients, paths, and smooth shapes.
- Use Pillow for image processing and final image handling.

Requirements:
- Create the image at 1024x1024 resolution.
- Use anti-aliasing when possible.
- Import every required library yourself.
- Use random module for randomness, never math.random.

At the end:
- The variable "image" must contain the final Pillow Image object.
"""


class ImageGenerator(QThread):

    finished = pyqtSignal(bool, str)

    def __init__(self, prompt, callback, name):
        super().__init__()

        self.prompt = prompt
        self.callback = callback
        self.name = name


    def run(self):

        try:
            plan_response = client.chat.completions.create(
                    model= "deepseek-v4-flash",
                    messages=[
                        {
                            "role": "system",
                            "content":planner_prompt
                        },
                        {
                            "role": "user",
                            "content": self.prompt
                        }
                    ],
                    stream=False
            )
            image_description = plan_response.choices[0].message.content

            code_response = client.chat.completions.create(
                    model= "deepseek-v4-flash",
                    messages=[
                        {
                            "role": "system",
                            "content": generator_prompt
                        },
                        {
                            "role": "user",
                            "content": image_description
                        }
                    ],
                    stream=False
            )


            code=code_response.choices[0].message.content

            code = code.replace("```python", "")
            code = code.replace("```", "")
            code = code.strip()


            namespace = {
                "__builtins__": __builtins__
            }

            exec(code, namespace)


            image = namespace["image"]

            image.save(f"{self.name}.png")


            self.finished.emit(True, f"{self.name}.png")


        except Exception as e:

            self.finished.emit(False, str(e))
