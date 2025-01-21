import flet as ft
from yt_dlp import YoutubeDL
import requests
from PIL import Image
from io import BytesIO
import os

def main(page: ft.Page):
    # Configuración de la página
    page.title = "DownFlet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Elementos de la UI
    title_app = ft.Text("DOWNFLET - Descargador de videos", size="30", color="white")
    output_text = ft.Text(size=12)
    thumbnail_image = ft.Image(width=150, height=150)
    progress_bar = ft.ProgressBar(width=300, value=0)
    download_path_text = ft.Text(size=12)
    output_dir = "/storage/emulated/0/Download/Downflet-videos"

    # Campo de entrada con borde blanco
    url_input = ft.TextField(
        label="Enlace del video",
        width=300,
        border_color=ft.Colors.WHITE,  # Cambiar el borde a blanco
        focused_border_color=ft.Colors.WHITE,  # Mantener el borde blanco al enfocarse
    )

    # Botón de búsqueda
    search_button = ft.ElevatedButton(
        "Buscar Video",
        on_click=lambda e: buscar_video(e),
        width=150,
    )

    # Botón de descarga
    download_button = ft.ElevatedButton("Descargar", disabled=True, width=150)

    def buscar_video(e):
        url = url_input.value
        if not url:
            output_text.value = "Por favor, ingresa un enlace válido."
            thumbnail_image.src = None  # Limpia la imagen si no hay un enlace válido
            thumbnail_image.update()
            page.update()
            return

        try:
            # Configuración de yt-dlp
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "format": "best",
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                thumbnail_url = info.get("thumbnail", "")

                if thumbnail_url:
                    response = requests.get(thumbnail_url)
                    if response.status_code == 200:  # Verifica que el thumbnail se descargue correctamente
                        # Convertir la imagen a base64 para evitar guardar archivos locales
                        img_data = BytesIO(response.content).getvalue()
                        thumbnail_image.src_base64 = ft.base64_encode(img_data)
                        thumbnail_image.update()

                        # Limpia el campo de entrada
                        url_input.value = ""
                        url_input.update()

                        output_text.value = f"Video encontrado: {info['title']}"
                        download_button.disabled = False
                    else:
                        output_text.value = "No se pudo cargar el thumbnail."
                        thumbnail_image.src = None
                        thumbnail_image.update()
                else:
                    output_text.value = "No se encontró un thumbnail para este video."
                    thumbnail_image.src = None
                    thumbnail_image.update()

        except Exception as e:
            output_text.value = f"Error: {str(e)}"
            thumbnail_image.src = None
            thumbnail_image.update()
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
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            ydl_opts = {
                "outtmpl": f"{output_dir}/%(title)s.%(ext)s",
                "format": "best",
                "progress_hooks": [hook_progreso],
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                download_path_text.value = f"Archivo guardado en: {output_dir}/{info['title']}.{info['ext']}"
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

    # Botón de descarga
    download_button.on_click = descargar_video

    # Agregar elementos a la página
    page.add(
        title_app,
        url_input,
        search_button,
        thumbnail_image,
        download_button,
        progress_bar,
        output_text,
        download_path_text,
    )

# Ejecutar la aplicación
ft.app(target=main)
