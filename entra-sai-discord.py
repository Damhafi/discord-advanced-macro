import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import time
import threading
import keyboard
import json
import os

CONFIG_FILE = 'posicoes_advanced.json'

# Global State
sequences = {
    "perfil_1": [], # list of dicts: {"pos": [x,y], "delay": 2.0, "name": "Ação 1"}
    "perfil_2": []
}

executando_p1 = False
executando_p2 = False
thread_p1_ativa = False
thread_p2_ativa = False
duration = 0.0

def carregar_config():
    global sequences
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                if "perfil_1" in data: sequences["perfil_1"] = data["perfil_1"]
                if "perfil_2" in data: sequences["perfil_2"] = data["perfil_2"]
        except Exception:
            pass

def salvar_config():
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(sequences, f)
    except Exception as e:
        print("Erro ao salvar:", e)

def executar_sequencia(perfil_key):
    global executando_p1, executando_p2
    while True:
        is_active = False
        if perfil_key == "perfil_1" and thread_p1_ativa and executando_p1:
            is_active = True
        elif perfil_key == "perfil_2" and thread_p2_ativa and executando_p2:
            is_active = True
        
        if is_active and len(sequences[perfil_key]) > 0:
            for step in sequences[perfil_key]:
                # If stopped mid-sequence, break out
                if perfil_key == "perfil_1" and not executando_p1: break
                if perfil_key == "perfil_2" and not executando_p2: break
                
                pos = step.get("pos")
                delay = float(step.get("delay", 1.0))
                
                if pos and len(pos) == 2:
                    pyautogui.moveTo(pos[0], pos[1], duration=duration)
                    pyautogui.click(button='left')
                    
                # Interruptible sleep
                start_t = time.time()
                while time.time() - start_t < delay:
                    if perfil_key == "perfil_1" and not executando_p1: break
                    if perfil_key == "perfil_2" and not executando_p2: break
                    time.sleep(0.1)
        else:
            time.sleep(0.1)

# Start execution threads
threading.Thread(target=executar_sequencia, args=("perfil_1",), daemon=True).start()
threading.Thread(target=executar_sequencia, args=("perfil_2",), daemon=True).start()

def monitorar_teclas():
    global executando_p1, executando_p2
    while True:
        if thread_p1_ativa and keyboard.is_pressed('down'):
            executando_p1 = not executando_p1
            time.sleep(0.5)
            
        if thread_p2_ativa and keyboard.is_pressed('up'):
            executando_p2 = not executando_p2
            time.sleep(0.5)
            
        time.sleep(0.1)

threading.Thread(target=monitorar_teclas, daemon=True).start()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Macro de Sequência Avançada")
        self.root.geometry("540x650")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)
        
        # --- Modern Dark Theme Colors (Discord Inspired) ---
        self.color_bg = "#36393f"
        self.color_bg_secondary = "#2f3136"
        self.color_text = "#dcddde"
        self.color_text_title = "#ffffff"
        self.color_btn_primary = "#5865f2"
        self.color_btn_danger = "#ed4245"
        self.color_btn_success = "#3ba55d"
        self.color_btn_warning = "#fee75c"
        self.color_btn_secondary = "#4f545c"
        self.color_border = "#202225"
        
        self.root.configure(bg=self.color_bg)
        
        carregar_config()
        
        self.frame_main = tk.Frame(root, bg=self.color_bg)
        self.frame_perfil = tk.Frame(root, bg=self.color_bg)
        
        self.perfil_atual = None
        self.step_widgets = [] # Keeps track of dynamic rows
        
        self.setup_main()
        self.setup_perfil_ui()
        
        self.show_frame(self.frame_main)
        self.atualizar_status()

    def create_button(self, parent, text, bg, fg, command, width=None, font=("Segoe UI", 10, "bold")):
        btn = tk.Button(parent, text=text, font=font, bg=bg, fg=fg, relief="flat", 
                        cursor="hand2", command=command, activebackground=bg, activeforeground=fg)
        if width:
            btn.config(width=width)
        return btn

    def setup_main(self):
        lbl = tk.Label(self.frame_main, text="Selecione o Macro", font=("Segoe UI", 20, "bold"), bg=self.color_bg, fg=self.color_text_title)
        lbl.pack(pady=(60, 30))
        
        btn_p1 = self.create_button(self.frame_main, "📞 Configurar Perfil 1\n(Atalho: Seta Baixo)", self.color_btn_primary, "white", command=lambda: self.abrir_perfil("perfil_1"), width=35)
        btn_p1.config(height=3)
        btn_p1.pack(pady=10)
        
        btn_p2 = self.create_button(self.frame_main, "📺 Configurar Perfil 2\n(Atalho: Seta Cima)", "#eb459e", "white", command=lambda: self.abrir_perfil("perfil_2"), width=35) # Pinkish for P2
        btn_p2.config(height=3)
        btn_p2.pack(pady=10)

    def setup_perfil_ui(self):
        self.header_frame = tk.Frame(self.frame_perfil, bg=self.color_bg_secondary, pady=10)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)
        
        self.lbl_titulo_perfil = tk.Label(self.header_frame, text="Perfil", font=("Segoe UI", 16, "bold"), bg=self.color_bg_secondary, fg=self.color_text_title)
        self.lbl_titulo_perfil.pack()
        
        # Area rolável para os passos
        self.canvas_frame = tk.Frame(self.frame_perfil, bg=self.color_bg)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Scrollbar com estilo
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Vertical.TScrollbar", background=self.color_bg_secondary, troughcolor=self.color_bg, bordercolor=self.color_bg, arrowcolor=self.color_text)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg=self.color_bg, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.color_bg)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Botões inferiores
        btn_frame = tk.Frame(self.frame_perfil, bg=self.color_bg, pady=15)
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        btn_add = self.create_button(btn_frame, "➕ Adicionar Nova Ação", self.color_btn_success, "white", self.add_step_ui)
        btn_add.config(pady=8, padx=20)
        btn_add.pack(pady=5)
        
        self.lbl_status = tk.Label(btn_frame, text="STATUS: PARADO", font=("Segoe UI", 12, "bold"), bg=self.color_bg, fg=self.color_btn_danger)
        self.lbl_status.pack(pady=5)
        
        btn_voltar = self.create_button(btn_frame, "⬅ Voltar e Salvar", self.color_btn_secondary, "white", self.voltar_main)
        btn_voltar.config(pady=5, padx=20)
        btn_voltar.pack(pady=5)

    def add_step_ui(self, step_data=None):
        if step_data is None:
            # Novo passo default
            idx = len(sequences[self.perfil_atual])
            step_data = {"pos": [0,0], "delay": 2.0, "name": f"Ação {idx+1}"}
            sequences[self.perfil_atual].append(step_data)
            
        idx = sequences[self.perfil_atual].index(step_data)
        
        step_name = step_data.get("name", "")
        if not step_name:
            step_name = f"Ação {idx+1}"
        
        row_frame = tk.Frame(self.scrollable_frame, bg=self.color_bg_secondary, bd=0, padx=10, pady=10)
        row_frame.pack(fill=tk.X, pady=6, padx=5)
        
        # Coluna da Esquerda (Nome + Posição)
        col1 = tk.Frame(row_frame, bg=self.color_bg_secondary)
        col1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        name_var = tk.StringVar(value=step_name)
        entry_name = tk.Entry(col1, textvariable=name_var, font=("Segoe UI", 11, "bold"), width=18, bg=self.color_bg, fg=self.color_text_title, relief="flat", insertbackground=self.color_text_title)
        entry_name.pack(anchor="w", pady=(0, 5))
        
        def update_name(*args, s=step_data, nv=name_var):
            s["name"] = nv.get()
        name_var.trace("w", update_name)
        
        pos_var = tk.StringVar(value=f"X: {step_data['pos'][0]}   Y: {step_data['pos'][1]}")
        lbl_pos = tk.Label(col1, textvariable=pos_var, bg=self.color_bg_secondary, fg=self.color_text, font=("Segoe UI", 9))
        lbl_pos.pack(anchor="w")
        
        # Coluna do Meio (Botão Gravar + Delay)
        col2 = tk.Frame(row_frame, bg=self.color_bg_secondary)
        col2.pack(side=tk.LEFT, padx=10)
        
        btn_gravar = self.create_button(col2, "🎯 Gravar", self.color_btn_primary, "white", lambda s=step_data, pv=pos_var: self.gravar_posicao_step(s, pv))
        btn_gravar.config(font=("Segoe UI", 9, "bold"), padx=10)
        btn_gravar.pack(pady=(0, 5))
        
        delay_frame = tk.Frame(col2, bg=self.color_bg_secondary)
        delay_frame.pack()
        
        tk.Label(delay_frame, text="Espera(s):", bg=self.color_bg_secondary, fg=self.color_text, font=("Segoe UI", 9)).pack(side=tk.LEFT)
        delay_var = tk.StringVar(value=str(step_data['delay']))
        entry_delay = tk.Entry(delay_frame, textvariable=delay_var, width=5, bg=self.color_bg, fg=self.color_text_title, relief="flat", font=("Segoe UI", 9), justify="center", insertbackground=self.color_text_title)
        entry_delay.pack(side=tk.LEFT, padx=5)
        
        def update_delay(*args, s=step_data, dv=delay_var):
            try:
                val = float(dv.get().replace(',','.'))
                s["delay"] = val
            except ValueError:
                pass
        delay_var.trace("w", update_delay)
        
        # Coluna da Direita (Remover)
        col3 = tk.Frame(row_frame, bg=self.color_bg_secondary)
        col3.pack(side=tk.RIGHT)
        
        btn_remove = self.create_button(col3, "✖", self.color_btn_danger, "white", lambda s=step_data, rf=row_frame: self.remove_step(s, rf))
        btn_remove.config(font=("Segoe UI", 12))
        btn_remove.pack()
        
        self.step_widgets.append(row_frame)

    def gravar_posicao_step(self, step_data, pos_var):
        pos_var.set("Gravando em 4s...")
        def capturar():
            time.sleep(4)
            pos = pyautogui.position()
            step_data["pos"] = [pos.x, pos.y]
            self.root.after(0, lambda: pos_var.set(f"X: {pos.x}   Y: {pos.y}"))
            salvar_config()
        threading.Thread(target=capturar, daemon=True).start()

    def remove_step(self, step_data, row_frame):
        if step_data in sequences[self.perfil_atual]:
            sequences[self.perfil_atual].remove(step_data)
        row_frame.destroy()
        salvar_config()
        self.recarregar_lista()

    def recarregar_lista(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.step_widgets.clear()
        
        for step in sequences[self.perfil_atual]:
            self.add_step_ui(step)

    def show_frame(self, frame):
        self.frame_main.pack_forget()
        self.frame_perfil.pack_forget()
        frame.pack(fill=tk.BOTH, expand=True)

    def abrir_perfil(self, perfil_id):
        global thread_p1_ativa, thread_p2_ativa, executando_p1, executando_p2
        self.perfil_atual = perfil_id
        
        if perfil_id == "perfil_1":
            self.lbl_titulo_perfil.config(text="Perfil 1 (Seta p/ Baixo)")
            thread_p1_ativa = True
            thread_p2_ativa = False
            executando_p1 = False
            executando_p2 = False
        else:
            self.lbl_titulo_perfil.config(text="Perfil 2 (Seta p/ Cima)")
            thread_p2_ativa = True
            thread_p1_ativa = False
            executando_p1 = False
            executando_p2 = False
            
        self.recarregar_lista()
        self.show_frame(self.frame_perfil)

    def voltar_main(self):
        global thread_p1_ativa, thread_p2_ativa, executando_p1, executando_p2
        salvar_config()
        thread_p1_ativa = False
        thread_p2_ativa = False
        executando_p1 = False
        executando_p2 = False
        self.show_frame(self.frame_main)

    def atualizar_status(self):
        if self.perfil_atual == "perfil_1":
            if executando_p1:
                self.lbl_status.config(text="● EM EXECUÇÃO", fg=self.color_btn_success)
            else:
                self.lbl_status.config(text="■ PARADO", fg=self.color_btn_danger)
        elif self.perfil_atual == "perfil_2":
            if executando_p2:
                self.lbl_status.config(text="● EM EXECUÇÃO", fg=self.color_btn_success)
            else:
                self.lbl_status.config(text="■ PARADO", fg=self.color_btn_danger)
                
        self.root.after(200, self.atualizar_status)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
