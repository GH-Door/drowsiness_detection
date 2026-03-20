import gradio as gr
import numpy as np


def process_frame(frame):
    if frame is None:
        return None, "NO FRAME"

    # 지금은 더미 상태
    status = "NORMAL"

    return frame, status


with gr.Blocks() as demo:
    gr.Markdown("## Drowsiness Detection Demo")

    with gr.Row():
        webcam = gr.Image(sources=["webcam"], type="numpy", label="Webcam Input")
        output = gr.Image(type="numpy", label="Output Preview")

    status_box = gr.Textbox(label="Status")

    webcam.stream(fn=process_frame, inputs=webcam, outputs=[output, status_box])

demo.launch(server_name="0.0.0.0", server_port=7860)
