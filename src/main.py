import flet as ft
from yt_dlp import YoutubeDL
import requests
from PIL import Image
from io import BytesIO
import os

def main(page: ft.Page):
    # Configuración de la página
    page.title = "Descargador de Videos"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    # Elementos de la UI
    url_input = ft.TextField(label="Enlace del video", width=300)
    output_text = ft.Text(size=12)
    thumbnail_image = ft.Image(width=150, height=150)
    progress_bar = ft.ProgressBar(width=300, value=0)
    download_path_text = ft.Text(size=12)  # Mostrar la ruta del archivo descargado

    # Botón de descarga
    download_button = ft.ElevatedButton("Descargar", disabled=True, width=150)

    def buscar_video(e):
        url = url_input.value
        if not url:
            output_text.value = "Por favor, ingresa un enlace válido."
            page.update()
            return

        try:
            # Configuración de yt-dlp
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "format": "best",  # Mejor calidad disponible
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                thumbnail_url = info.get("thumbnail", "")

                if thumbnail_url:
                    response = requests.get(thumbnail_url)
                    img = Image.open(BytesIO(response.content))
                    img.save("thumbnail.jpg")
                    thumbnail_image.src = "thumbnail.jpg"
                    thumbnail_image.update()

                    output_text.value = f"Video encontrado: {info['title']}"
                    download_button.disabled = False
                else:
                    output_text.value = "No se pudo cargar el thumbnail."
        except Exception as e:
            output_text.value = f"Error: {str(e)}"
            thumbnail_image.src = ""
            download_button.disabled = True

        page.update()

    def descargar_video(e):
        url = url_input.value
        if not url:
            output_text.value = "Por favor, ingresa un enlace válido."
            page.update()
            return

        # Cambiar color y texto del botón al iniciar la descarga
        download_button.text = "Descargando..."
        download_button.bgcolor = ft.colors.LIGHT_BLUE
        page.update()

        try:   
            if not os.path.exists("/storage/emulated/0/DCIM/DownFlet"):
                os.makedirs("/storage/emulated/0/DCIM/DownFlet")
            ydl_opts = {
                #"outtmpl": "videos/%(title)s.%(ext)s",  # Carpeta de salida(pc)
                #"outtmpl": "/storage/emulated/0/Download/%(title)s.%(ext)s", #op1
                "outtmpl": "/storage/emulated/0/DCIM/DownFlet/%(title)s.%(ext)s", #op2
                "format": "best",  # Mejor calidad disponible
                "progress_hooks": [hook_progreso],  # Progreso
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                download_path_text.value = f"Archivo guardado en: videos/{info['title']}.{info['ext']}"
                page.update()

            output_text.value = "¡Descarga completada!"
        except Exception as e:
            output_text.value = f"Error al descargar: {str(e)}"
            download_path_text.value = ""

        # Restaurar el botón al estado inicial
        download_button.text = "Descargar"
        download_button.bgcolor = ft.colors.BLUE
        page.update()

    def hook_progreso(d):
        if d["status"] == "downloading":
            progreso = d.get("downloaded_bytes", 0) / d.get("total_bytes", 1)
            progress_bar.value = progreso
            page.update()
        elif d["status"] == "finished":
            progress_bar.value = 1
            page.update()

    # Botón para buscar el video
    search_button = ft.ElevatedButton("Buscar Video", on_click=buscar_video, width=150)

    # Botón de descarga
    download_button.on_click = descargar_video

    # Agregar elementos a la página
    page.add(
        url_input,
        search_button,
        thumbnail_image,
        download_button,
        progress_bar,
        output_text,
        download_path_text,  # Añadir la ruta del archivo al final
    )

# Ejecutar la aplicación
ft.app(target=main)
