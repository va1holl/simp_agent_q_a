import os
import tkinter as tk
import requests
from dotenv import load_dotenv



HF_TOKEN = os.getenv('TOKEN')
API_URL = "https://api-inference.huggingface.co/models/suno/bark"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def speak():
    text = entry.get("1.0", tk.END).strip()
    if not text:
        return
    r = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": text}
    )
    if r.status_code != 200:
        status.config(text="Ошибка API")
        return
    with open("output.wav", "wb") as f:
        f.write(r.content)
    status.config(text="Готово: output.wav")

root = tk.Tk()
root.title("Text → Speech (Bark)")

entry = tk.Text(root, width=60, height=10)
entry.pack(padx=10, pady=10)

btn = tk.Button(root, text="Озвучить", command=speak)
btn.pack(pady=5)

status = tk.Label(root, text="")
status.pack(pady=5)

root.mainloop()