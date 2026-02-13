#!/usr/bin/env python3
"""
Script auxiliar para compilar o projeto YouTube Downloader para executável.
Uso: python src/build.py [--with-ffmpeg] [--optimized]
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_executable(with_ffmpeg=False, optimized=False):
    """Cria um executável a partir do script GUI."""
    
    print("=" * 70)
    print("YouTube Downloader - Build Executável")
    print("=" * 70)
    
    # Obter diretório de trabalho
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    src_dir = script_dir
    gui_file = os.path.join(src_dir, "youtube_mp3_gui.py")
    images_dir = os.path.join(src_dir, "images")
    
    # Verificar arquivos necessários
    if not os.path.exists(gui_file):
        print(f"\n[❌] Erro: arquivo '{gui_file}' não encontrado!")
        return False
    
    if not os.path.exists(images_dir):
        print(f"[⚠️ ] Aviso: pasta '{images_dir}' não encontrada!")
    
    # Validar estrutura
    print(f"\n[*] Estrutura do projeto:")
    print(f"    Diretório base: {project_root}")
    print(f"    Src: {src_dir}")
    print(f"    Imagens: {images_dir}")
    
    # Verificar e baixar/preparar FFmpeg se necessário
    if with_ffmpeg:
        ffmpeg_bin = os.path.join(src_dir, "ffmpeg", "bin", "ffmpeg.exe")
        if not os.path.exists(ffmpeg_bin):
            print("\n[*] Preparando FFmpeg...")
            try:
                ffmpeg_manager = os.path.join(src_dir, "ffmpeg_manager.py")
                subprocess.run([sys.executable, ffmpeg_manager], check=True)
            except Exception as e:
                print(f"[⚠️ ] Aviso ao preparar FFmpeg: {e}")
                print("     O FFmpeg não será incluído no build.")
                with_ffmpeg = False
    
    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller
    except ImportError:
        print("\n[!] PyInstaller não está instalado.")
        print("[*] Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # Limpar builds anteriores
    for folder in ["build", "dist"]:
        folder_path = os.path.join(project_root, folder)
        if os.path.exists(folder_path):
            print(f"\n[*] Removendo {folder} anterior...")
            shutil.rmtree(folder_path)
    
    spec_file = os.path.join(project_root, "youtube_mp3_gui.spec")
    if os.path.exists(spec_file):
        os.remove(spec_file)
    
    # Construir comando PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", "YouTube MP3 Downloader",
        "--distpath", os.path.join(project_root, "dist"),
        "--buildpath", os.path.join(project_root, "build"),
        "--windowed",
        "--onefile",
    ]
    
    # Adicionar dados (imagens)
    if os.path.exists(images_dir):
        cmd.append(f"--add-data={images_dir}{os.pathsep}src/images")
    
    # Adicionar FFmpeg se selecionado
    if with_ffmpeg:
        ffmpeg_dir = os.path.join(src_dir, "ffmpeg")
        if os.path.exists(ffmpeg_dir):
            print(f"\n[*] Incluindo FFmpeg no build...")
            cmd.append(f"--add-data={ffmpeg_dir}{os.pathsep}ffmpeg")
    
    # Modo otimizado (reduz tamanho)
    if optimized:
        print("\n[*] Usando modo otimizado (reduz tamanho do executável)...")
        cmd.remove("--onefile")
        cmd.append("--onedir")
        cmd.extend([
            "--collect-submodules=yt_dlp",
            "--collect-submodules=customtkinter",
        ])
    
    cmd.append(gui_file)
    
    print(f"\n[*] Buildando...\n")
    
    try:
        result = subprocess.run(cmd, check=True, cwd=project_root)
        
        print("\n" + "=" * 70)
        print("✅ SUCESSO! Executável criado com sucesso!")
        print("=" * 70)
        
        if optimized:
            exe_dir = os.path.join(project_root, "dist", "YouTube MP3 Downloader")
            print(f"\n📦 Pasta: {exe_dir}")
            print(f"   Execute: {os.path.join(exe_dir, 'YouTube MP3 Downloader.exe')}")
        else:
            exe_path = os.path.join(project_root, "dist", "YouTube MP3 Downloader.exe")
            if os.path.exists(exe_path):
                size_mb = os.path.getsize(exe_path) / (1024 * 1024)
                print(f"\n📦 Arquivo: {exe_path}")
                print(f"📊 Tamanho: {size_mb:.2f} MB")
        
        print("\n✨ Você pode distribuir este executável para outros usuários!")
        if not with_ffmpeg:
            print("⚠️  Certifique-se de que o FFmpeg está instalado no computador de destino")
        else:
            print("✅ FFmpeg foi incluído no build!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao compilar: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        return False


if __name__ == "__main__":
    with_ffmpeg = "--with-ffmpeg" in sys.argv or "-f" in sys.argv
    optimized = "--optimized" in sys.argv or "-o" in sys.argv
    
    print("\nOpções detectadas:")
    print(f"  Incluir FFmpeg: {with_ffmpeg}")
    print(f"  Modo otimizado: {optimized}")
    print()
    
    success = build_executable(with_ffmpeg=with_ffmpeg, optimized=optimized)
    sys.exit(0 if success else 1)
