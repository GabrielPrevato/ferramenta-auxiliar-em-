from langchain_community.llms import HuggingFaceHub
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import warnings
from tkinter import Tk, Label, Entry, Button, Canvas, Scrollbar, Frame, messagebox
import random

warnings.filterwarnings("ignore", category=DeprecationWarning)

repo_id = "tiiuae/falcon-7b-instruct"
huggingfacehub_api_token = "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"
llm = HuggingFaceHub(huggingfacehub_api_token=huggingfacehub_api_token, 
                     repo_id=repo_id, 
                     model_kwargs={"temperature": 0.7, "max_new_tokens": 500})

template = """Question: {question}
            Answer: Let's give a detailed answer"""
prompt = PromptTemplate(template=template, input_variables=["question"])
chain = LLMChain(prompt=prompt, llm=llm)

pastel_colors = [
    "#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF", 
    "#D0BAFF", "#FFBAFF", "#BAFFBA", "#FFFABA", "#FFB7B2"
]

def gerar_cards():
    pergunta = pergunta_entry.get()
    if not pergunta:
        messagebox.showwarning("Aviso", "Insira a pergunta.")
        return
    
    resposta = chain.run(pergunta)
    cards = resposta.split('\n')[2:]
    
    for widget in cards_frame.winfo_children():
        widget.destroy()
    
    for i, card in enumerate(cards, start=1):
        if card.strip():
            color = random.choice(pastel_colors)
            card_label = Label(cards_frame, text=f"{card.strip()}", 
                               wraplength=400, justify="left", padx=50, pady=10,
                               font=("Arial", 12, "bold"), bg=color, anchor="w", relief="solid", bd=2)
            card_label.pack(pady=5, fill="x")

root = Tk()
root.title("Cards LLM")
root.geometry("600x600")
root.configure(bg="#f0f0f0")

pergunta_label = Label(root, text="Digite sua pergunta:", font=("Arial", 14), bg="#f0f0f0")
pergunta_label.pack(pady=10)

pergunta_entry = Entry(root, font=("Arial", 14), width=50)
pergunta_entry.pack(pady=5)

gerar_button = Button(root, text="Gerar Cards", command=gerar_cards, font=("Arial", 12))
gerar_button.pack(pady=10)

scroll_frame = Frame(root, bg="#f0f0f0")
scroll_frame.pack(pady=10, fill="both", expand=True)

canvas = Canvas(scroll_frame, highlightthickness=0, bg="#f0f0f0")
scrollbar = Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
cards_frame = Frame(canvas, bg="#f0f0f0")

cards_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=cards_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()