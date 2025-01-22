import flet as ft
from yt_dlp import YoutubeDL
import requests
from PIL import Image
from io import BytesIO
import os

def main(page: ft.Page):
    # Configuración inicial de la página
    page.title = "DownFlet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Elementos de la UI
    title_app = ft.Text("DOWNFLET - Descargador de videos", size="30", color="white")
    output_text = ft.Text(size=12)
    progress_bar = ft.ProgressBar(width=300, value=0)
    download_path_text = ft.Text(size=12)
    output_dir = "/storage/emulated/0/Download/Downflet-videos"

    # Campo de entrada
    url_input = ft.TextField(
        label="Enlace del video",
        width=300,
        border_color=ft.colors.WHITE,
        focused_border_color=ft.colors.WHITE,
    )

    # Imagen del thumbnail (oculta inicialmente)
    thumbnail_image = ft.Image(
        width=150,
        height=150,
        visible=False,  # Oculto al inicio
    )

    # Botón de búsqueda
    search_button = ft.ElevatedButton(
        "Buscar Video",
        on_click=lambda e: buscar_video(e),
        width=150
    )

    # Botón de descarga
    download_button = ft.ElevatedButton("Descargar", disabled=True, width=150)

    def buscar_video(e):
        url = url_input.value
        if not url:
            output_text.value = "Por favor, ingresa un enlace válido."
            thumbnail_image.visible = False  # Mantener oculto si no hay enlace válido
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
                    thumbnail_image.src = thumbnail_url
                    thumbnail_image.visible = True  # Mostrar el thumbnail
                    thumbnail_image.update()
                    url_input.value = ""
                    url_input.update()
                    output_text.value = f"Video encontrado: {info['title']}"
                    download_button.disabled = False
                else:
                    output_text.value = "No se encontró un thumbnail para este video."
                    thumbnail_image.visible = False
                    thumbnail_image.update()

        except Exception as e:
            output_text.value = f"Error: {str(e)}"
            thumbnail_image.visible = False
            thumbnail_image.update()
            download_button.disabled = True

        page.update()

    # Agregar elementos a la página
    page.add(
        title_app,
        url_input,
        search_button,
        thumbnail_image,  # Imagen se mantiene invisible hasta buscar
        download_button,
        progress_bar,
        output_text,
        download_path_text,
    )

# Ejecutar la aplicación
ft.app(target=main)
