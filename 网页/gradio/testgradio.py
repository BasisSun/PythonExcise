import gradio as gr
import numpy as np
import random
import string
from PIL import Image

def greet(name, intensity,im,num):
    random_string = ''.join(random.choices(string.ascii_letters, k=20)) + '.png'
    pil_image = Image.fromarray(im)
    pil_image.save(random_string)
    return "Hello, " + name + "!" * int(intensity),np.flipud(im)

demo = gr.Interface(
    fn=greet,
    inputs=[gr.Text(label="产品名"), gr.Number(label='Age', info='In years, must be greater than 0'),gr.Image(sources=["webcam"])],
    
    outputs=["text","image"],
    additional_inputs=[
        gr.Slider(0, 1000),
    ],
    live=True
)

demo.launch()#share=True