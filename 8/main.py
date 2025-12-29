import tkinter as tk
import requests
from dotenv import load_dotenv



HF_TOKEN = os.getenv('TOKEN')
API_URL = "https://api-inference.huggingface.co/models/ali-vilab/modelscope-damo-text-to-video-synthesis"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def generate():
    prompt = text.get("1.0", tk.END).strip()
    if not prompt:
        status.config(text="Текста нет")
        return

    status.config(text="Генерация...")
    root.update()

    r = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt},
        timeout=600
    )

    if r.status_code != 200:
        status.config(text="Ошибка API")
        return

    with open("output.mp4", "wb") as f:
        f.write(r.content)

    status.config(text="Готово: output.mp4")

root = tk.Tk()
root.title("Text → Video")

text = tk.Text(root, width=60, height=8)
text.pack(padx=10, pady=10)

btn = tk.Button(root, text="Сгенерировать видео", command=generate)
btn.pack(pady=5)

status = tk.Label(root, text="")
status.pack(pady=5)

root.mainloop()
