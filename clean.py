#!/usr/bin/env python3
"""Script para limpar pastas de playlists baixadas."""

import os
import shutil

def clean():
    """Remove pastas de playlists, mantendo .git e src."""
    
    excluded_dirs = {'.git', 'src', 'assets', '.vscode', '.idea', 'dist', 'build', '__pycache__', 'images'}
    
    print("[*] Limpando pastas de playlists...")
    
    removed_count = 0
    for item in os.listdir('.'):
        if os.path.isdir(item) and item not in excluded_dirs:
            try:
                shutil.rmtree(item)
                print(f"    Removido: {item}")
                removed_count += 1
            except Exception as e:
                print(f"    Erro ao remover {item}: {e}")
    
    if removed_count == 0:
        print("[!] Nenhuma pasta para limpar.")
    else:
        print(f"[✓] Limpeza concluída! ({removed_count} pasta(s) removida(s))")

if __name__ == "__main__":
    clean()
