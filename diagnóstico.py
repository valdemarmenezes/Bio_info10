import tkinter as tk
from tkinter import messagebox, filedialog
import wikipedia
import re

wikipedia.set_lang("pt")

palavras_chave_exames = [
    "sorologia", "pcr", "elisa", "hemograma", "microbiologia",
    "imunologia", "exame", "teste", "diagnóstico", "análise",
    "cultura", "bioquímica", "antígeno", "anticorpo"
]

def extrair_secao(texto, secao):
    pattern = rf"==+\s*{re.escape(secao)}\s*==+(.*?)(==+[^=]|$)"
    match = re.search(pattern, texto, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def destacar_exames(texto):
    def destaque(match):
        return f"[{match.group(0).upper()}]"
    
    pattern = re.compile(r'\b(' + '|'.join(palavras_chave_exames) + r')\b', re.IGNORECASE)
    return pattern.sub(destaque, texto)

def buscar_diagnostico():
    termo = entrada.get().strip()
    if not termo:
        messagebox.showwarning("Aviso", "Digite o nome da doença.")
        return
    
    texto_resultado.delete("1.0", tk.END)
    texto_resultado.insert(tk.END, f"🔍 Buscando meios de diagnóstico laboratorial para: {termo}\n\n")
    
    try:
        pagina = wikipedia.page(termo)
        texto = pagina.content
        
        secoes_possiveis = ["Diagnóstico", "Diagnóstico laboratorial", "Diagnóstico e tratamento", "Diagnóstico e manejo"]
        secao_texto = None
        secao_encontrada = None
        for secao in secoes_possiveis:
            secao_texto = extrair_secao(texto, secao)
            if secao_texto:
                secao_encontrada = secao
                break
        
        if secao_texto:
            texto_destacado = destacar_exames(secao_texto)
            texto_resultado.insert(tk.END, f"Seção '{secao_encontrada}' encontrada:\n\n{texto_destacado}\n")
        else:
            padrao = re.compile(r"([^.]*\b(diagnóstico|exame|teste|laboratorial|análise|sorologia|PCR|ELISA|hemograma|microbiologia|imunologia)[^.]*\.)", re.IGNORECASE)
            resultados = padrao.findall(texto)
            
            if resultados:
                texto_resultado.insert(tk.END, "Principais meios de diagnóstico laboratorial encontrados:\n\n")
                for i, (frase, _) in enumerate(resultados[:10], 1):
                    frase_destacada = destacar_exames(frase)
                    texto_resultado.insert(tk.END, f"{i}. {frase_destacada.strip()}\n\n")
            else:
                texto_resultado.insert(tk.END, "Nenhum meio de diagnóstico laboratorial encontrado diretamente no texto.\n")
    
    except wikipedia.exceptions.DisambiguationError:
        texto_resultado.insert(tk.END, "O termo é ambíguo. Tente ser mais específico.\n")
    except wikipedia.exceptions.PageError:
        texto_resultado.insert(tk.END, "Página não encontrada na Wikipédia para este termo.\n")
    except Exception as e:
        texto_resultado.insert(tk.END, f"Ocorreu um erro: {e}")

def salvar_resultado():
    conteudo = texto_resultado.get("1.0", tk.END).strip()
    if not conteudo:
        messagebox.showinfo("Salvar", "Nenhum conteúdo para salvar.")
        return
    arquivo = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Arquivos de texto", "*.txt")],
        title="Salvar resultado como"
    )
    if arquivo:
        with open(arquivo, "w", encoding="utf-8") as f:
            f.write(conteudo)
        messagebox.showinfo("Salvar", f"Resultado salvo em:\n{arquivo}")

janela = tk.Tk()
janela.title("Buscador de Diagnóstico Laboratorial")
janela.geometry("700x550")

tk.Label(janela, text="Digite o nome da doença:").pack(pady=5)
entrada = tk.Entry(janela, width=50)
entrada.pack()

tk.Button(janela, text="Buscar Diagnóstico Laboratorial", command=buscar_diagnostico).pack(pady=5)

texto_resultado = tk.Text(janela, wrap=tk.WORD, height=25)
texto_resultado.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

tk.Button(janela, text="Salvar Resultado", command=salvar_resultado).pack(pady=5)

janela.mainloop()
