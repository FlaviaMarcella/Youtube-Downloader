#!/usr/bin/env python3
"""
Gerenciador de FFmpeg para YouTube Downloader.
Baixa e extrai FFmpeg automaticamente se não estiver instalado.
"""

import os
import sys
import shutil
import urllib.request
import zipfile
from pathlib import Path

FFMPEG_DOWNLOAD_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
FFMPEG_DIR = os.path.join(os.path.dirname(__file__), "ffmpeg")
FFMPEG_BIN = os.path.join(FFMPEG_DIR, "bin", "ffmpeg.exe")


def is_ffmpeg_installed():
    """Verifica se FFmpeg está instalado no PATH."""
    return shutil.which("ffmpeg") is not None


def is_ffmpeg_local():
    """Verifica se existe FFmpeg local no projeto."""
    return os.path.exists(FFMPEG_BIN)


def download_ffmpeg():
    """Baixa FFmpeg da fonte pública."""
    print("[*] Baixando FFmpeg...")
    print(f"    URL: {FFMPEG_DOWNLOAD_URL}")
    
    zip_path = os.path.join(FFMPEG_DIR, "ffmpeg.zip")
    
    try:
        # Criar diretório se não existir
        os.makedirs(FFMPEG_DIR, exist_ok=True)
        
        # Baixar arquivo
        urllib.request.urlretrieve(FFMPEG_DOWNLOAD_URL, zip_path)
        print("[✓] Download concluído!")
        
        # Extrair
        print("[*] Extraindo FFmpeg...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(FFMPEG_DIR)
        print("[✓] Extração concluída!")
        
        # Reorganizar estrutura (FFmpeg coloca em pasta aninhada)
        for root, dirs, files in os.walk(FFMPEG_DIR):
            for file in files:
                if file in ["ffmpeg.exe", "ffprobe.exe"]:
                    src = os.path.join(root, file)
                    bin_dir = os.path.join(FFMPEG_DIR, "bin")
                    os.makedirs(bin_dir, exist_ok=True)
                    dst = os.path.join(bin_dir, file)
                    shutil.move(src, dst)
                    print(f"[✓] Movido {file}")
        
        # Limpar estrutura desnecessária
        for item in os.listdir(FFMPEG_DIR):
            item_path = os.path.join(FFMPEG_DIR, item)
            if item != "bin" and os.path.isdir(item_path):
                shutil.rmtree(item_path)
        
        # Remover zip
        if os.path.exists(zip_path):
            os.remove(zip_path)
        
        print("[✓] FFmpeg instalado com sucesso!")
        return True
        
    except Exception as e:
        print(f"[❌] Erro ao baixar FFmpeg: {e}")
        return False


def ensure_ffmpeg():
    """Garante que FFmpeg está disponível."""
    # Verificar FFmpeg no PATH
    if is_ffmpeg_installed():
        print("[✓] FFmpeg encontrado no PATH")
        return True
    
    # Verificar FFmpeg local
    if is_ffmpeg_local():
        print("[✓] FFmpeg local encontrado")
        # Adicionar ao PATH
        bin_dir = os.path.join(FFMPEG_DIR, "bin")
        os.environ['PATH'] = bin_dir + os.pathsep + os.environ.get('PATH', '')
        return True
    
    # Oferecer download
    print("\n[!] FFmpeg não encontrado!")
    print("[*] Você pode:")
    print("    1. Baixá-lo automaticamente (requer internet)")
    print("    2. Instalar manualmente de https://ffmpeg.org/download.html")
    
    return False


if __name__ == "__main__":
    if not is_ffmpeg_installed() and not is_ffmpeg_local():
        print("YouTube Downloader - Gerenciador de FFmpeg\n")
        response = input("Deseja baixar FFmpeg automaticamente? (s/n): ").lower()
        if response == 's':
            if download_ffmpeg():
                sys.exit(0)
            else:
                sys.exit(1)
        else:
            sys.exit(1)
    else:
        ensure_ffmpeg()
        print("FFmpeg está disponível!")
