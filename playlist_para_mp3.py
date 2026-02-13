import os
import re
import sys
import shutil
from yt_dlp import YoutubeDL

def sanitize_filename(name):
    """Remove caracteres inválidos para nomes de arquivos."""
    return re.sub(r'[\\/*?:"<>|]', "", name)

def check_ffmpeg():
    """Verifica se o FFmpeg está instalado, pois é necessário para a conversão."""
    if shutil.which("ffmpeg") is None:
        print("-" * 50)
        print("⚠️  ERRO: FFmpeg não encontrado!")
        print("O FFmpeg é obrigatório para converter vídeos em MP3.")
        print("Por favor, instale o FFmpeg e adicione-o ao PATH do seu sistema.")
        print("-" * 50)
        return False
    return True

def download_playlist_as_mp3(playlist_url):
    """Baixa todos os vídeos de uma playlist e converte para MP3."""
    
    if not check_ffmpeg():
        return

    print(f"🔍 Analisando playlist: {playlist_url}")

    # 1. Obter informações da playlist primeiro para criar a pasta
    ydl_opts_info = {
        'extract_flat': True,
        'quiet': True,
        'nocheckcertificate': True,
    }

    try:
        with YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            if not info:
                print("❌ Não foi possível obter informações da playlist.")
                return
            
            playlist_title = info.get('title', 'Musicas_Youtube')
            entries = info.get('entries', [])
            total_videos = len(entries)
    except Exception as e:
        print(f"❌ Erro ao acessar playlist: {e}")
        return

    # Criar pasta de destino
    folder_name = sanitize_filename(playlist_title)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    print(f"📂 Pasta de destino: '{folder_name}'")
    print(f"🎵 Total de vídeos encontrados: {total_videos}")
    print("-" * 50)

    # 2. Configurações para download e conversão
    # Usamos '%(playlist_index)s' para manter a ordem da playlist nos arquivos
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{folder_name}/%(playlist_index)s - %(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', # Qualidade padrão (192kbps)
        }],
        'quiet': False, # Mostrar progresso
        'no_warnings': True,
        'ignoreerrors': True, # Pular vídeos com erro (privados/deletados)
        'nocheckcertificate': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])
    except Exception as e:
        print(f"❌ Ocorreu um erro durante o download: {e}")

    print("-" * 50)
    print(f"🏁 Processo concluído!")
    print(f"📂 Seus arquivos MP3 estão em: {os.path.abspath(folder_name)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Insira o link da Playlist do YouTube: ").strip()
    
    if url:
        download_playlist_as_mp3(url)
    else:
        print("❌ Nenhuma URL fornecida.")
