import tkinter as tk
import queue


class ResourceMonitorGUI:
    def __init__(self, stop_event=None):
        self.stop_event = stop_event

        self.root = tk.Tk()
        self.root.title("Monitor de Recursos - Alarmes")
        self.root.geometry("600x400")

        # Área de texto (onde aparecem os alertas)
        self.text_area = tk.Text(
            self.root,
            state='disabled',
            bg='black',
            fg='red',
            font=('Consolas', 10)
        )
        self.text_area.pack(expand=True, fill='both', padx=10, pady=10)

        # Botão de parar para o encerramento gracioso)
        self.stop_button = tk.Button(
            self.root,
            text="Parar Sistema",
            command=self.close,
            bg="gray",
            fg="white",
            width=28,  
            height=8    
        )
        self.stop_button.pack(pady=5)

        # Fila interna para mensagens vindas dos consumidores
        self.message_queue = queue.Queue()

        # Quando clicas no X da janela
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        # Loop de atualização da GUI
        self.root.after(100, self._process_messages)

    def add_alert(self, message):
        """Chamado pelos consumidores para adicionar alertas"""
        self.message_queue.put(message)

    def _process_messages(self):
        """Atualiza a interface com novos alertas"""
        while not self.message_queue.empty():
            msg = self.message_queue.get()

            self.text_area.config(state='normal')
            self.text_area.insert(tk.END, f"[ALERTA] {msg}\n")
            self.text_area.see(tk.END)
            self.text_area.config(state='disabled')

        self.root.after(100, self._process_messages)

    def close(self):
        """Encerramento gracioso"""
        if self.stop_event is not None:
            self.stop_event.set()

        self.root.destroy()

    def start(self):
        """Arranca a GUI (bloqueante)"""
        self.root.mainloop()