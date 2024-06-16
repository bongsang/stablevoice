import gradio as gr

# File selection
def greet(names):
    return "\n".join(names)

# Create a Gradio File Dropdown
file_dropdown = gr.Files(label="Select your file")

# Create a Gradio Output
output_text = gr.Textbox()

# Create a Gradio Interface
gr.Interface(fn=greet, inputs=file_dropdown, outputs=output_text).launch()
