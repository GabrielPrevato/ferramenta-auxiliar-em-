from langchain_community.llms import HuggingFaceHub
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import warnings
from tkinter import Tk, Label, Entry, Button, Canvas, Scrollbar, Frame, messagebox
import random

warnings.filterwarnings("ignore", category=DeprecationWarning)

repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
huggingfacehub_api_token = "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"
llm = HuggingFaceHub(
    huggingfacehub_api_token=huggingfacehub_api_token,
    repo_id=repo_id,
    model_kwargs={"temperature": 0.3, "max_new_tokens": 500}
)

#prompts
template = "Explique de forma clara e objetiva o que é {question}. Inclua os principais conceitos relacionados e, se possível, exemplos simples para facilitar o entendimento."

template2 = """Liste apenas os títulos de 3 temas únicos e relevantes relacionados a "{question}"."""

prompt = PromptTemplate(template=template, input_variables=["question"])
prompt2 = PromptTemplate(template=template2, input_variables=["question"])
chain = LLMChain(prompt=prompt, llm=llm)
chain2 = LLMChain(prompt=prompt2, llm=llm)

pastel_colors = [
    "#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF",
    "#D0BAFF", "#FFBAFF", "#BAFFBA", "#FFFABA", "#FFB7B2"
]

def processar_resposta(temas_resposta):
    temas = [tema.strip() for tema in temas_resposta.split('\n') if tema.strip()]
    return temas[1:4]

def gerar_cards(pergunta=None):
    if pergunta is None:
        pergunta = pergunta_entry.get()
    if not pergunta:
        messagebox.showwarning("Aviso", "Insira a pergunta.")
        return
    
    resumo_resposta = chain.run(pergunta)
    
    temas_resposta = chain2.run(pergunta)
    temas_cards = processar_resposta(temas_resposta)
    
    for widget in cards_frame.winfo_children():
        widget.destroy()
    
    resumo_label = Label(
        cards_frame, text=f"Resumo: {resumo_resposta}",
        wraplength=500, justify="left", padx=20, pady=10,
        font=("Arial", 12, "italic"), bg="#ffffff", anchor="w"
    )
    resumo_label.pack(pady=5, fill="x")

    for card in temas_cards:
        color = random.choice(pastel_colors)
        card_label = Label(
            cards_frame, text=card.strip(),
            wraplength=400, justify="left", padx=50, pady=10,
            font=("Arial", 12, "bold"), bg=color, anchor="w", relief="solid", bd=2
        )
        card_label.bind("<Button-1>", lambda event, card_text=card.strip(): gerar_cards(card_text))
        card_label.pack(pady=5, fill="x")

#configuração da interface
root = Tk()
root.title("Cards LLM")
root.geometry("600x600")
root.configure(bg="#f0f0f0")

#elementos
pergunta_label = Label(root, text="Digite seu tema:", font=("Arial", 14), bg="#f0f0f0")
pergunta_label.pack(pady=10)

pergunta_entry = Entry(root, font=("Arial", 14), width=50)
pergunta_entry.pack(pady=5)

gerar_button = Button(root, text="Gerar Cards", command=lambda: gerar_cards(), font=("Arial", 12))
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
