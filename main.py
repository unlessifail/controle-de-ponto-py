import customtkinter as ctk
import tkinter as tk
from datetime import datetime, timedelta
import json
import os
from tkinter import messagebox

class ControlePonto:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("1440x50")
        self.root.overrideredirect(True)  # Remove a barra de título
        self.root.attributes('-alpha', 0.7)  # Define transparência
        self.root.attributes('-topmost', True)  # Sempre no topo
        
        # Posiciona a janela acima da barra de tarefas
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        taskbar_height = 40  # Altura aproximada da barra de tarefas
        y_position = screen_height - taskbar_height - 50
        self.root.geometry(f"1440x50+{(screen_width-1440)//2}+{y_position}")

        # Variáveis de controle
        self.status = "Fora de Serviço"
        self.inicio_status = datetime.now()
        self.pausas_disponiveis = 2
        self.logs = []
        self.tempo_total = {}
        
        self.criar_interface()
        self.atualizar_contador()
        
        # Carregar logs se existirem
        self.carregar_logs()

    def criar_interface(self):
        # Frame principal
        frame = ctk.CTkFrame(self.root)
        frame.pack(fill=tk.X, expand=True, padx=5, pady=5)

        # Label de status
        self.status_label = ctk.CTkLabel(frame, text=f"Status: {self.status}")
        self.status_label.pack(side=tk.LEFT, padx=5)

        # Label do contador
        self.contador_label = ctk.CTkLabel(frame, text="00:00:00")
        self.contador_label.pack(side=tk.RIGHT, padx=5)

        # Botões
        self.btn_entrada = ctk.CTkButton(frame, text="Entrada", command=self.registrar_entrada)
        self.btn_entrada.pack(side=tk.LEFT, padx=2)

        self.btn_pausa = ctk.CTkButton(frame, text="Pausa I", command=self.registrar_pausa, state="disabled")
        self.btn_pausa.pack(side=tk.LEFT, padx=2)

        self.btn_almoco = ctk.CTkButton(frame, text="Almoço", command=self.registrar_almoco, state="disabled")
        self.btn_almoco.pack(side=tk.LEFT, padx=2)

        self.btn_feedback = ctk.CTkButton(frame, text="Feedback", command=self.registrar_feedback, state="disabled")
        self.btn_feedback.pack(side=tk.LEFT, padx=2)

        self.btn_reuniao = ctk.CTkButton(frame, text="Reunião", command=self.registrar_reuniao, state="disabled")
        self.btn_reuniao.pack(side=tk.LEFT, padx=2)

        self.btn_indisponivel = ctk.CTkButton(frame, text="Indisponível", command=self.registrar_indisponivel, state="disabled")
        self.btn_indisponivel.pack(side=tk.LEFT, padx=2)

        self.btn_logs = ctk.CTkButton(frame, text="Logs", command=self.exibir_logs)
        self.btn_logs.pack(side=tk.LEFT, padx=2)

    def atualizar_contador(self):
        tempo_decorrido = datetime.now() - self.inicio_status
        horas = tempo_decorrido.seconds // 3600
        minutos = (tempo_decorrido.seconds % 3600) // 60
        segundos = tempo_decorrido.seconds % 60
        self.contador_label.configure(text=f"{horas:02d}:{minutos:02d}:{segundos:02d}")
        
        # Verificar alertas
        if self.status == "Almoçando" and tempo_decorrido.seconds >= 58 * 60:
            self.mostrar_alerta_almoco()
        elif self.status.startswith("Pausa") and tempo_decorrido.seconds >= 9 * 60:
            self.mostrar_alerta_pausa()
            
        self.root.after(1000, self.atualizar_contador)

    def registrar_log(self, novo_status):
        tempo_decorrido = datetime.now() - self.inicio_status
        
        # Atualizar tempo total no status anterior
        if self.status not in self.tempo_total:
            self.tempo_total[self.status] = timedelta()
        self.tempo_total[self.status] += tempo_decorrido
        
        log = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status_anterior": self.status,
            "novo_status": novo_status,
            "duracao": str(tempo_decorrido).split('.')[0]
        }
        self.logs.append(log)
        self.salvar_logs()

    def registrar_entrada(self):
        if self.status == "Fora de Serviço":
            self.registrar_log("Em função")
            self.status = "Em função"
            self.inicio_status = datetime.now()
            self.status_label.configure(text=f"Status: {self.status}")
            self.btn_entrada.configure(text="Saída")
            self.habilitar_botoes()
            self.pausas_disponiveis = 2
            self.btn_pausa.configure(text="Pausa I")
        elif self.status == "Em função":
            self.registrar_log("Fora de Serviço")
            self.status = "Fora de Serviço"
            self.inicio_status = datetime.now()
            self.status_label.configure(text=f"Status: {self.status}")
            self.btn_entrada.configure(text="Entrada")
            self.desabilitar_botoes()
            self.btn_almoco.configure(state="disabled")
            self.btn_pausa.configure(text="Pausa I")

    def registrar_pausa(self):
        if self.status == "Em função":
            if self.pausas_disponiveis > 0:
                pausa_texto = "Pausa I" if self.pausas_disponiveis == 2 else "Pausa II"
                self.registrar_log(pausa_texto)
                self.status = pausa_texto
                self.inicio_status = datetime.now()
                self.status_label.configure(text=f"Status: {self.status}")
                self.btn_pausa.configure(text="Despausar")
                self.desabilitar_botoes(exceto="pausa")
        elif self.status.startswith("Pausa"):
            self.registrar_log("Em função")
            self.status = "Em função"
            self.inicio_status = datetime.now()
            self.status_label.configure(text=f"Status: {self.status}")
            self.pausas_disponiveis -= 1
            if self.pausas_disponiveis > 0:
                self.btn_pausa.configure(text="Pausa II")
            else:
                self.btn_pausa.configure(state="disabled")
            self.habilitar_botoes()

    def registrar_almoco(self):
        if self.status == "Em função":
            self.registrar_log("Almoçando")
            self.status = "Almoçando"
            self.inicio_status = datetime.now()
            self.status_label.configure(text=f"Status: {self.status}")
            self.btn_almoco.configure(text="Retornar")
            self.desabilitar_botoes(exceto="almoco")
        elif self.status == "Almoçando":
            self.retornar_almoco()

    def registrar_feedback(self):
        if self.status == "Em função":
            self.registrar_log("Em feedback")
            self.status = "Em feedback"
            self.inicio_status = datetime.now()
            self.status_label.configure(text=f"Status: {self.status}")
            self.btn_feedback.configure(text="Retornar")
            self.desabilitar_botoes(exceto="feedback")
        elif self.status == "Em feedback":
            self.retornar_feedback()

    def registrar_reuniao(self):
        if self.status == "Em função":
            self.registrar_log("Em reunião")
            self.status = "Em reunião"
            self.inicio_status = datetime.now()
            self.status_label.configure(text=f"Status: {self.status}")
            self.btn_reuniao.configure(text="Retornar")
            self.desabilitar_botoes(exceto="reuniao")
        elif self.status == "Em reunião":
            self.retornar_reuniao()

    def registrar_indisponivel(self):
        if self.status == "Em função":
            self.registrar_log("Indisponível")
            self.status = "Indisponível"
            self.inicio_status = datetime.now()
            self.status_label.configure(text=f"Status: {self.status}")
            self.btn_indisponivel.configure(text="Disponível")
            self.desabilitar_botoes(exceto="indisponivel")
        elif self.status == "Indisponível":
            self.retornar_disponivel()

    def retornar_almoco(self):
        self.registrar_log("Em função")
        self.status = "Em função"
        self.inicio_status = datetime.now()
        self.status_label.configure(text=f"Status: {self.status}")
        self.btn_almoco.configure(text="Almoço", state="disabled")
        self.habilitar_botoes()

    def retornar_feedback(self):
        self.registrar_log("Em função")
        self.status = "Em função"
        self.inicio_status = datetime.now()
        self.status_label.configure(text=f"Status: {self.status}")
        self.btn_feedback.configure(text="Feedback")
        self.habilitar_botoes()

    def retornar_reuniao(self):
        self.registrar_log("Em função")
        self.status = "Em função"
        self.inicio_status = datetime.now()
        self.status_label.configure(text=f"Status: {self.status}")
        self.btn_reuniao.configure(text="Reunião")
        self.habilitar_botoes()

    def retornar_disponivel(self):
        self.registrar_log("Em função")
        self.status = "Em função"
        self.inicio_status = datetime.now()
        self.status_label.configure(text=f"Status: {self.status}")
        self.btn_indisponivel.configure(text="Indisponível")
        self.habilitar_botoes()

    def habilitar_botoes(self):
        for btn in [self.btn_pausa, self.btn_almoco, self.btn_feedback, 
                   self.btn_reuniao, self.btn_indisponivel]:
            btn.configure(state="normal")

    def desabilitar_botoes(self, exceto=None):
        botoes = {
            "pausa": self.btn_pausa,
            "almoco": self.btn_almoco,
            "feedback": self.btn_feedback,
            "reuniao": self.btn_reuniao,
            "indisponivel": self.btn_indisponivel
        }
        
        for nome, btn in botoes.items():
            if nome != exceto:
                btn.configure(state="disabled")

    def mostrar_alerta_almoco(self):
        if messagebox.showwarning("Alerta de Atraso", "Seu horário de almoço está excedendo o limite!",
                                type=messagebox.OK) == "ok":
            self.retornar_almoco()

    def mostrar_alerta_pausa(self):
        if messagebox.showwarning("Alerta de Atraso", "Sua pausa está excedendo o limite!",
                                type=messagebox.OK) == "ok":
            self.registrar_pausa()

    def exibir_logs(self):
        janela_logs = ctk.CTkToplevel(self.root)
        janela_logs.title("Logs de Atividade")
        janela_logs.geometry("600x400")
        
        texto_logs = ctk.CTkTextbox(janela_logs)
        texto_logs.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Calcular porcentagens
        tempo_total = sum((v.total_seconds() for v in self.tempo_total.values()), 0)
        
        texto_logs.insert("1.0", "=== RESUMO ===\n\n")
        for status, tempo in self.tempo_total.items():
            porcentagem = (tempo.total_seconds() / tempo_total * 100) if tempo_total > 0 else 0
            texto_logs.insert("end", f"{status}: {str(tempo).split('.')[0]} ({porcentagem:.1f}%)\n")
        
        texto_logs.insert("end", "\n=== LOGS DETALHADOS ===\n\n")
        for log in self.logs:
            texto_logs.insert("end", f"[{log['timestamp']}] {log['status_anterior']} -> {log['novo_status']} (Duração: {log['duracao']})\n")
        
        def exportar_logs():
            with open("logs_ponto.txt", "w", encoding="utf-8") as f:
                f.write(texto_logs.get("1.0", tk.END))
            messagebox.showinfo("Sucesso", "Logs exportados para logs_ponto.txt")
        
        btn_exportar = ctk.CTkButton(janela_logs, text="Exportar Logs", command=exportar_logs)
        btn_exportar.pack(pady=10)

    def salvar_logs(self):
        dados = {
            "logs": self.logs,
            "tempo_total": {k: str(v) for k, v in self.tempo_total.items()}
        }
        with open("logs_ponto.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

    def carregar_logs(self):
        try:
            with open("logs_ponto.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                self.logs = dados["logs"]
                self.tempo_total = {}
                for k, v in dados["tempo_total"].items():
                    # Remove os microssegundos se existirem
                    tempo_partes = v.split('.')
                    tempo_str = tempo_partes[0]  # Pega apenas a parte antes do ponto
                    # Divide em horas, minutos e segundos
                    h, m, s = map(int, tempo_str.split(':'))
                    self.tempo_total[k] = timedelta(hours=h, minutes=m, seconds=s)
        except FileNotFoundError:
            pass

    def executar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ControlePonto()
    app.executar() 