# YouTube Downloader - Playlist para MP3

Um script Python para baixar playlists completas do YouTube e converter automaticamente todos os vídeos para MP3.

**Disponível em 2 versões:**
- 🔧 **CLI** (Command Line Interface) - `src/playlist_para_mp3.py`
- 🎨 **GUI** (Interface Gráfica) - `src/youtube_mp3_gui.py` 💙 **Recomendada**

## 🎯 Funcionalidades

- ✅ Download de playlists inteiras do YouTube
- ✅ Conversão automática para MP3 (192kbps)
- ✅ Organização em pastas nomeadas pela playlist
- ✅ Preservação da ordem dos vídeos da playlist
- ✅ Sanitização de nomes de arquivos
- ✅ Tratamento de erros (pula vídeos privados/deletados)
- ✅ Feedback visual com emojis e progresso

## 📋 Pré-requisitos

### Para uso via Python
- Python 3.6+
- FFmpeg instalado e adicionado ao PATH do sistema
- Dependências em `requirements.txt`

### Para usar Executável
- **SEM FFmpeg incluído:** Windows 10+ | FFmpeg instalado no sistema
- **COM FFmpeg incluído:** Windows 10+ | Nenhuma dependência externa

## 🚀 Instalação

### Opção 1: Usar Python (Desenvolvimento)

1. **Clone o repositório:**
```bash
git clone https://github.com/FlaviaMarcella/Youtube-Downloader.git
cd Youtube-Downloader
```

2. **Instale as dependências Python:**
```bash
make install
# ou: pip install -r requirements.txt
```

3. **Instale o FFmpeg:**
   - **Windows:** Baixe em [ffmpeg.org](https://ffmpeg.org/download.html) ou use `choco install ffmpeg`
   - **Linux/Ubuntu:** `sudo apt-get install ffmpeg`
   - **macOS:** `brew install ffmpeg`

### Opção 2: Usar Executável (Recomendado para Usuários)

1. **Clone ou baixe o repositório**
2. **Execute:** `make build-with-ffmpeg`
3. **Distribute:** `dist/YouTube MP3 Downloader.exe`

O executável funcionará em qualquer Windows 10+ sem necessidade de instalar Python ou FFmpeg!

## 💻 Uso

### Versão GUI (Interface Gráfica) - Recomendada para Iniciantes

```bash
python src/youtube_mp3_gui.py
```

Ou via Makefile:
```bash
make gui
```

A interface gráfica oferece:
- ✅ Logo do projeto para identificação
- ✅ Campo de entrada amigável para URL
- ✅ Seleção de pasta de destino
- ✅ Log detalhado do progresso
- ✅ Barra de progresso
- ✅ Feedback visual com mensagens

### Versão CLI (Linha de Comando)

#### Opção 1: Linha de Comando Direta
```bash
python src/playlist_para_mp3.py "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
```

#### Opção 2: Usar Makefile
```bash
make download URL="https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
```

#### Opção 3: Input Interativo
```bash
python src/playlist_para_mp3.py
# Digite a URL da playlist quando solicitado
```

## 🔨 Compilar para Executável (.exe)

Para criar um executável standalone que não requer Python instalado:

### Opção 1: Via Makefile (Simples)

**Sem FFmpeg** (requer FFmpeg instalado no sistema de destino):
```bash
make build
```

**Com FFmpeg Incluído** (recomendado - FFmpeg será automaticamente baixado e incluído):
```bash
make build-with-ffmpeg
```

### Opção 2: Via Script Python (Avançado)

```bash
# Modo padrão (sem FFmpeg)
python src/build.py

# Com FFmpeg incluído
python src/build.py --with-ffmpeg

# Modo otimizado (reduz tamanho, cria pasta)
python src/build.py --optimized
```

### Opção 3: Comando Direto PyInstaller

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "YouTube MP3 Downloader" --add-data "src/images:src/images" src/youtube_mp3_gui.py
```

---

## ℹ️ Informações sobre o Build

### Executável Sem FFmpeg
- 📦 Tamanho: ~140-160 MB
- ⚠️ Requer FFmpeg instalado no sistema de destino
- ✅ Rápido de gerar

### Executável Com FFmpeg
- 📦 Tamanho: ~350-400 MB (inclui FFmpeg)
- ✅ Funciona fora da caixa, sem dependências externas
- ✨ Melhor para distribuição (recomendado!)
- 🔄 Primeira execução baixa/extrai FFmpeg (~200 MB)

---

## 📋 Arquivo Gerado

O executável será criado em:
- **Modo padrão:** `dist/YouTube MP3 Downloader.exe`
- **Modo otimizado:** `dist/YouTube MP3 Downloader/YouTube MP3 Downloader.exe`

## 📁 Estrutura

```
Youtube-Downloader/
├── src/
│   ├── youtube_mp3_gui.py       # Interface gráfica (GUI)
│   ├── playlist_para_mp3.py     # Script CLI para download
│   ├── ffmpeg_manager.py        # Gerenciador de FFmpeg
│   ├── build.py                 # Script para criar executável
│   └── images/
│       ├── logo.png             # Logo do projeto
│       └── ...
├── README.md                     # Este arquivo
├── .gitignore                    # Configuração de exclusões do Git
├── Makefile                      # Automação de tarefas
└── requirements.txt              # Dependências Python
```

## 📊 Saída

Os arquivos MP3 baixados serão salvos em uma pasta com o nome da playlist clonada e organizados com o seguinte padrão:

```
Playlist_Name/
├── 01 - Video Title.mp3
├── 02 - Another Video.mp3
└── 03 - More Videos.mp3
```

## ⚙️ Comandos Makefile

```bash
make help            # Mostra ajuda
make install         # Instala dependências
make gui             # Abre a interface gráfica
make download URL=   # Baixa playlist via CLI (requer URL=...)
make build           # Cria executável sem FFmpeg
make build-with-ffmpeg  # Cria executável com FFmpeg incluído
make clean           # Remove pastas de playlists baixadas
```

**Exemplos:**
```bash
make gui
make build-with-ffmpeg
make download URL="https://www.youtube.com/playlist?list=PLxxxxxx"
```

## 🔧 Configuração Disponível

No script `playlist_para_mp3.py`, você pode ajustar:
- **Qualidade de áudio:** altere `'preferredquality': '192'` (padrão 192kbps)
- **Formato:** modifique `'preferredcodec': 'mp3'` para outro formato

## ⚠️ Aviso Legal

- Respeite os direitos autorais
- Use apenas para fins pessoais
- Verifique a política de uso do YouTube

## 🐛 Solução de Problemas

### FFmpeg não encontrado
- Certifique-se de que o FFmpeg está instalado
- Adicione ao PATH do seu sistema

### Erro de certificado SSL
- O script já trata isso com a opção `'nocheckcertificate': True`

### Alguns vídeos falharam
- É normal que vídeos privados ou deletados causem erros
- O script continua nos vídeos válidos

## 📄 Licença

Este projeto está disponível sob a licença MIT.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

---

**Desenvolvido com ❤️**
