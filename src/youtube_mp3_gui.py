import os
import re
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from yt_dlp import YoutubeDL
from PIL import Image

# Configurações de aparência do CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def get_resource_path(filename):
    """Obtém o caminho correto para recursos (funciona em dev e executável)."""
    if getattr(tk, '_MEIPASS', False):
        # Executável PyInstaller
        return os.path.join(tk._MEIPASS, 'src', 'images', filename)
    else:
        # Desenvolvimento
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, 'images', filename)

def check_ffmpeg():
    """Verifica se o FFmpeg está instalado."""
    if shutil.which("ffmpeg") is not None:
        return True
    
    # Tentar pasta local (para build com FFmpeg incluído)
    local_ffmpeg = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'bin', 'ffmpeg.exe')
    if os.path.exists(local_ffmpeg):
        return True
    
    return False

class YoutubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube MP3 Downloader")
        self.geometry("650x550")

        # Verificar FFmpeg no início
        if not check_ffmpeg():
            messagebox.showwarning(
                "FFmpeg Não Encontrado",
                "O FFmpeg não está instalado ou não foi encontrado no PATH.\n\n"
                "Por favor, instale o FFmpeg de:\n"
                "https://ffmpeg.org/download.html\n\n"
                "Após instalar, adicione o FFmpeg ao PATH do sistema."
            )

        # Layout Principal
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        # Logo e Título
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        logo_frame.grid_columnconfigure(1, weight=1)

        try:
            logo_path = get_resource_path("logo.png")
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                logo_img.thumbnail((60, 60), Image.Resampling.LANCZOS)
                logo_photo = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(60, 60))
                logo_label = ctk.CTkLabel(logo_frame, image=logo_photo, text="")
                logo_label.image = logo_photo  # Manter referência
                logo_label.grid(row=0, column=0, padx=(0, 15))
        except Exception as e:
            print(f"Aviso: Não foi possível carregar a logo: {e}")

        self.label_title = ctk.CTkLabel(logo_frame, text="YouTube\nPlaylist para MP3", font=ctk.CTkFont(size=18, weight="bold"))
        self.label_title.grid(row=0, column=1, sticky="w")

        # Campo de URL
        self.url_entry = ctk.CTkEntry(self, placeholder_text="Cole o link da playlist ou vídeo aqui...", width=500)
        self.url_entry.grid(row=1, column=0, padx=20, pady=10)

        # Seleção de Pasta
        self.folder_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.folder_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.folder_frame.grid_columnconfigure(0, weight=1)

        self.folder_path = tk.StringVar(value=os.path.expanduser("~/Downloads"))
        self.folder_entry = ctk.CTkEntry(self.folder_frame, textvariable=self.folder_path, state="readonly")
        self.folder_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.folder_button = ctk.CTkButton(self.folder_frame, text="Escolher Pasta", command=self.browse_folder, width=120)
        self.folder_button.grid(row=0, column=1)

        # Botão de Download
        self.download_button = ctk.CTkButton(self, text="Iniciar Download", command=self.start_download_thread, font=ctk.CTkFont(weight="bold"))
        self.download_button.grid(row=3, column=0, padx=20, pady=20)

        # Área de Log/Status
        self.status_text = ctk.CTkTextbox(self, height=150)
        self.status_text.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.status_text.insert("0.0", "Pronto para começar...\n")
        self.status_text.configure(state="disabled")

        # Barra de Progresso (Indeterminada para simplificar)
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.progress_bar.set(0)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def log(self, message):
        self.status_text.configure(state="normal")
        self.status_text.insert("end", f"> {message}\n")
        self.status_text.see("end")
        self.status_text.configure(state="disabled")

    def sanitize_filename(self, name):
        return re.sub(r'[\\/*?:"<>|]', "", name)

    def start_download_thread(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Aviso", "Por favor, insira uma URL válida.")
            return

        self.download_button.configure(state="disabled")
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        
        # Rodar em uma thread separada para não travar a interface
        thread = threading.Thread(target=self.download_process, args=(url,))
        thread.daemon = True
        thread.start()

    def download_process(self, url):
        output_dir = self.folder_path.get()
        
        # Logger customizado para o yt-dlp
        class MyLogger:
            def __init__(self, app):
                self.app = app
            def debug(self, msg):
                if msg.startswith('[download]'):
                    pass # Evitar poluir muito o log com progresso de bytes
                else:
                    self.app.after(0, lambda: self.app.log(msg))
            def warning(self, msg):
                self.app.after(0, lambda: self.app.log(f"AVISO: {msg}"))
            def error(self, msg):
                self.app.after(0, lambda: self.app.log(f"ERRO: {msg}"))

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output_dir}/%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': MyLogger(self),
            'nocheckcertificate': True,
            'ignoreerrors': True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                self.after(0, lambda: self.log("Iniciando análise e download..."))
                ydl.download([url])
            self.after(0, lambda: self.log("🏁 Processo concluído com sucesso!"))
            self.after(0, lambda: messagebox.showinfo("Sucesso", "Download concluído!"))
        except Exception as e:
            self.after(0, lambda: self.log(f"ERRO FATAL: {str(e)}"))
            self.after(0, lambda: messagebox.showerror("Erro", f"Ocorreu um erro: {e}"))
        finally:
            self.after(0, self.reset_ui)

    def reset_ui(self):
        self.download_button.configure(state="normal")
        self.progress_bar.stop()
        self.progress_bar.set(0)

if __name__ == "__main__":
    app = YoutubeDownloaderApp()
    app.mainloop()
