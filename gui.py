import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import asyncio
import json
import os
# Importamos la nueva función orquestadora de compatibilidad
from src.main import run_matchmaker_pipeline

class TikTokScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Scraper Pro - AI Matchmaker")
        self.root.geometry("650x650")
        self.root.configure(padx=20, pady=20)

        # Panel de entrada
        tk.Label(root, text="Tu Username (ej. @tu_usuario):", font=("Arial", 12, "bold")).pack(anchor="w")
        self.entry_user1 = tk.Entry(root, font=("Arial", 14))
        self.entry_user1.pack(fill="x", pady=(5, 10))

        tk.Label(root, text="Username de tu Crush/Objetivo (ej. @crush):", font=("Arial", 12, "bold")).pack(anchor="w")
        self.entry_user2 = tk.Entry(root, font=("Arial", 14))
        self.entry_user2.pack(fill="x", pady=(5, 15))

        self.btn_run = tk.Button(root, text="▶ Analizar Compatibilidad", bg="#FF4B4B", fg="white", font=("Arial", 12, "bold"), command=self.start_scraping)
        self.btn_run.pack(fill="x", ipady=5)

        # Panel de visualización de datos
        tk.Label(root, text="Resultados:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(20, 5))
        self.result_box = scrolledtext.ScrolledText(root, font=("Consolas", 10), bg="#1e1e1e", fg="#d4d4d4", wrap=tk.WORD)
        self.result_box.pack(fill="both", expand=True)

    def start_scraping(self):
        user1 = self.entry_user1.get().strip()
        user2 = self.entry_user2.get().strip()
        
        if not user1 or not user2:
            messagebox.showwarning("Advertencia", "Por favor ingresa ambos usuarios.")
            return

        # Bloquear botón y limpiar pantalla
        self.btn_run.config(state=tk.DISABLED, text="⏳ Analizando Perfiles...")
        self.result_box.delete(1.0, tk.END)
        self.insert_text(f"Iniciando proceso para {user1} y {user2}...\n(El navegador invisible se está ejecutando de fondo)\n\n")

        # Ejecutar en un hilo separado para no congelar la interfaz
        threading.Thread(target=self.run_async_task, args=(user1, user2), daemon=True).start()

    def run_async_task(self, user1, user2):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            # Ejecutamos el nuevo orquestador de parejas
            report_path = loop.run_until_complete(run_matchmaker_pipeline(user1, user2))

            if report_path and os.path.exists(report_path):
                self.display_json_data(report_path)
            else:
                self.insert_text("[ERROR] No se pudo generar el reporte JSON.\n")
        except Exception as e:
            self.insert_text(f"\n[ERROR CRÍTICO] {e}\n")
        finally:
            # Restaurar botón al terminar
            self.root.after(0, lambda: self.btn_run.config(state=tk.NORMAL, text="▶ Analizar Compatibilidad"))

    def display_json_data(self, filepath):
        """Lee el JSON de compatibilidad y lo muestra estructurado en la interfaz."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        res = "="*50 + "\n"
        res += " 💘 REPORTE DE COMPATIBILIDAD Y ESTRATEGIA\n"
        res += "="*50 + "\n\n"

        # Función auxiliar para formatear cada perfil
        def format_profile(profile_data, title):
            if not profile_data:
                return f" [!] Datos no encontrados para {title}\n\n"
                
            p_res = f" 👤 {title}: {profile_data.get('username', 'N/A')}\n"
            p_res += f" 👥 Seguidores: {profile_data.get('followers')} | 👣 Siguiendo: {profile_data.get('following')}\n"
            
            big_five = profile_data.get("big_five_analysis", {})
            p_res += f" 🧠 Big Five ({big_five.get('status', 'Error')}):\n"
            
            if big_five.get("status") == "Completado":
                for trait, score in big_five.get("scores", {}).items():
                    p_res += f"    - {trait}: {score}\n"
            else:
                p_res += f"    - Motivo: {big_five.get('reason', 'Sin datos suficientes')}\n"
            return p_res + "\n"

        # Mostrar perfil 1 y 2
        res += format_profile(data.get("user1_profile", {}), "USUARIO 1 (Tú)")
        res += format_profile(data.get("user2_profile", {}), "USUARIO 2 (Objetivo)")

        # Mostrar la estrategia de conquista
        res += "="*50 + "\n"
        res += f"{data.get('strategy', 'No se pudo generar la estrategia.')}\n"
        res += "="*50 + "\n"

        self.insert_text(res)

    def insert_text(self, text):
        """Inserta texto de forma segura desde el hilo secundario al principal."""
        self.root.after(0, self._append, text)

    def _append(self, text):
        self.result_box.insert(tk.END, text)
        self.result_box.see(tk.END)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = TikTokScraperGUI(ventana)
    ventana.mainloop()