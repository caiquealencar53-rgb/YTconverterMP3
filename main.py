import os
from flask import Flask, render_template, request, send_file
import yt_dlp




app = Flask(__name__)

# Pasta temporária onde o áudio será salvo antes do envio
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form.get("url")
        
        if not video_url:
            return "Por favor, insira uma URL válida."
    # Configurações do yt-dlp para baixar apenas o áudio em MP3
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extrai as informações e faz o download
                info = ydl.extract_info(video_url, download=True)
                # Descobre o nome do arquivo final gerado
                filename = ydl.prepare_filename(info)
                mp3_filename = os.path.splitext(filename)[0] + ".mp3"
                
        

            # Envia o arquivo de áudio gerado para o usuário
            response = send_file(mp3_filename, as_attachment=True)
            
            # Opcional: deletar o arquivo do seu servidor após o envio para não encher o disco
            # (Pode requerer uma lógica de cleanup posterior)
            
            return response

        except Exception as e:
            return f"Ocorreu um erro ao processar o vídeo: {str(e)}", 500

    return render_template("index.html")
if __name__ == '__main__':
    app.run(debug=True)


