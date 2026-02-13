.PHONY: help install gui download clean build build-with-ffmpeg

help:
	@echo.
	@echo YouTube Downloader - Playlist para MP3
	@echo ========================================
	@echo.
	@echo Comandos disponíveis:
	@echo   make help                 - Mostra esta mensagem
	@echo   make install              - Instala dependências Python
	@echo   make gui                  - Abre a interface gráfica
	@echo   make download URL=...     - Baixa playlist via CLI
	@echo   make build                - Cria executável (.exe)
	@echo   make build-with-ffmpeg    - Cria executável com FFmpeg incluído
	@echo   make clean                - Remove pastas de playlists baixadas
	@echo.
	@echo Exemplos:
	@echo   make gui
	@echo   make build
	@echo   make build-with-ffmpeg
	@echo   make download URL="https://www.youtube.com/playlist?list=PLxxxxxx"
	@echo.

install:
	@echo [*] Instalando dependências...
	pip install -r requirements.txt
	@echo [✓] Instalação concluída!

gui:
	@echo [*] Abrindo interface gráfica...
	python src/youtube_mp3_gui.py

download:
	@if "$(URL)" == "" (echo [!] Erro: Use URL="sua_url_aqui" & exit /b 1)
	@echo [*] Iniciando download...
	python src/playlist_para_mp3.py "$(URL)"

clean:
	@echo [*] Limpando pastas de playlists...
	@for /d %%D in (*) do (if /i not "%%D"==".git" rmdir /s /q "%%D" 2>nul)
	@echo [✓] Limpeza concluída!

build:
	@echo [*] Buildando executável...
	python src/build.py
	@echo [✓] Executável criado em: dist/YouTube MP3 Downloader.exe

build-with-ffmpeg:
	@echo [*] Buildando executável com FFmpeg...
	python src/build.py --with-ffmpeg
	@echo [✓] Executável criado com FFmpeg incluído!
