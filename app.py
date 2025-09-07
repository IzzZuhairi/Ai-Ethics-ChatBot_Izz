from openai import OpenAI
import gradio as gr
import os

# API Key akan diambil dari Secrets Hugging Face
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Fungsi chatbot
def ai_ethics_chat(user_input, history):
    messages = [{"role": "system", "content": (
        "You are an AI Policy & Ethics expert. "
        "Jawab semua soalan tentang AI ethics, governance, risiko, "
        "dan polisi dengan bahasa mudah difahami oleh pelajar."
    )}]
    
    for human, ai in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": ai})
    
    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    bot_reply = response.choices[0].message.content
    history.append((user_input, bot_reply))
    return history, ""

# UI
with gr.Blocks(
    theme=gr.themes.Base(primary_hue="gray", secondary_hue="slate"),
    css="""
    body {background: linear-gradient(180deg, #1e1e1e, #2c2c2c); color: #f5f5f5; font-family: 'Segoe UI', sans-serif;}
    h1 {color: #ffffff; text-align:center; font-size:2.5em; animation: fadeIn 2s;}
    p {text-align:center; color: #cccccc; font-size:1.1em; animation: fadeInUp 2s;}
    .gr-button-primary {background: linear-gradient(90deg, #444, #777); color: white; border-radius: 12px; font-weight:bold; transition:0.3s;}
    .gr-button-primary:hover {background: linear-gradient(90deg, #666, #999); transform: scale(1.05);}
    .gr-textbox textarea {background:#2a2a2a; color:#ffffff; border-radius:12px; border:1px solid #444;}
    .gr-chatbot {background:#1b1b1b; border:1px solid #333; border-radius:18px;}
    
    @keyframes fadeIn {
        from {opacity:0;}
        to {opacity:1;}
    }
    @keyframes fadeInUp {
        from {opacity:0; transform:translateY(25px);}
        to {opacity:1; transform:translateY(0);}
    }
    """
) as demo:
    gr.Markdown(
        """
        <h1>AIzz Ethics Chatbot</h1>
        <p>Tanya apa-apa tentang <b>AI Ethics & Policy</b><br>
        Dibina oleh <i>Izz (16y AI Builder)</i></p>
        """
    )

    chatbot = gr.Chatbot(height=450, bubble_full_width=False, show_label=False)
    with gr.Row():
        msg = gr.Textbox(
            show_label=False, 
            placeholder="Tulis soalan anda di sini...",
            container=False
        )
        submit = gr.Button("Hantar", variant="primary")
    clear = gr.Button("Clear Chat")

    submit.click(ai_ethics_chat, [msg, chatbot], [chatbot, msg])
    msg.submit(ai_ethics_chat, [msg, chatbot], [chatbot, msg])
    clear.click(lambda: [], None, chatbot, queue=False)

demo.launch()
