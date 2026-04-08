import gradio as gr
import subprocess

def run_inference():
    try:
        # Run inference.py and capture exact output
        result = subprocess.run(['python', 'inference.py'], capture_output=True, text=True, timeout=30)
        return result.stdout + "\n" + result.stderr
    except subprocess.TimeoutExpired:
        return "Process timed out after 30 seconds."
    except Exception as e:
        return str(e)

with gr.Blocks(title="OpenEnv Code Review Hackathon", theme=gr.themes.Soft()) as app:
    gr.Markdown("# OpenEnv Environment: Code Review")
    gr.Markdown("This interface runs the `inference.py` backend and displays the `[START]`, `[STEP]`, `[END]` output strictly required by the hackathon spec.")
    
    with gr.Row():
        run_btn = gr.Button("Run Inference Agent")
    
    with gr.Row():
        output_display = gr.Textbox(label="Agent Output Log", lines=15, interactive=False)
        
    run_btn.click(fn=run_inference, outputs=output_display)

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860)