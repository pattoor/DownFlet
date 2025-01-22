import flet as ft
from yt_dlp import YoutubeDL
import requests

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
    output_dir = "/storage/emulated/0/Download/Downflet-videos" #android
    #output_dir = "videos/%(title)s.%(ext)s" #pc

    # Campo de entrada
    url_input = ft.TextField(
        label="Enlace del video",
        width=300,
        border_color=ft.colors.WHITE,
        focused_border_color=ft.colors.WHITE,
    )

    # Variable para almacenar el enlace del video
    url_video = {"link": ""}

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

    # Función para buscar el video
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
                    url_video["link"] = url  # Guardar el enlace en la variable
                    url_input.value = ""  # Limpiar el campo de entrada
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

    # Función para descargar el video
    def descargar_video(e):
        url = url_video["link"]  # Usar el enlace guardado
        if not url:
            output_text.value = "Por favor, busca un video antes de descargarlo."
            page.update()
            return

        # Cambiar color y texto del botón al iniciar la descarga
        download_button.text = "Descargando..."
        download_button.bgcolor = ft.colors.LIGHT_BLUE
        page.update()

        try:
            ydl_opts = {
                #"outtmpl": "videos/%(title)s.%(ext)s",  # Carpeta de salida(pc)
                #"outtmpl": "/storage/emulated/0/Download/%(title)s.%(ext)s", #op1
                "outtmpl": f"{output_dir}/%(title)s.%(ext)s", #op2              
                "format": "best",  # Mejor calidad disponible
                "progress_hooks": [hook_progreso],  # Progreso
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                download_path_text.value = f"Archivo guardado en: {output_dir}/{info['title']}.{info['ext']}"
                output_text.value = "¡Descarga completada!"
                page.update()

              # Forzar indexación en Media Store -> (android)
                import os
                os.system(f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///storage/emulated/0/Download/Downflet-videos/{info['title']}.{info['ext']}")

        except Exception as e:
            output_text.value = f"Error al descargar: {str(e)}"
            download_path_text.value = ""

        # Restaurar el botón al estado inicial
        download_button.text = "Descargar"
        download_button.bgcolor = ft.colors.BLUE
        page.update()

    # Actualizar progreso de la descarga
    def hook_progreso(d):
        if d["status"] == "downloading":
            progreso = d.get("downloaded_bytes", 0) / d.get("total_bytes", 1)
            progress_bar.value = progreso
            page.update()
        elif d["status"] == "finished":
            progress_bar.value = 1
            page.update()

    # Configurar acciones de los botones
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
