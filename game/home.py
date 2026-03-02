# home.py – Pantalla de inicio DuckHunt (Flet 0.81+)
import flet as ft
import subprocess
import sys
import os

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
MAIN_PATH = os.path.join(BASE_DIR, "main.py")

# ─── Colores ──────────────────────────────────────────────────────────────────
BG      = "#0d1b2a"
CARD    = "#132338"
ACCENT  = "#f5a623"
GREEN   = "#27ae60"
RED     = "#c0392b"
WHITE   = "#ecf0f1"
MUTED   = "#95a5a6"
GREY    = "#bdc3c7"


def ctrl_row(icon: str, label: str, description: str) -> ft.Row:
    return ft.Row(
        [
            ft.Text(icon,        size=16),
            ft.Text(label,       size=13, weight=ft.FontWeight.BOLD, color=WHITE, width=85),
            ft.Text(description, size=12, color=GREY),
        ],
        spacing=10,
    )


def main(page: ft.Page):
    page.title            = "Tec Hunt – Inicio"
    page.window.width     = 600
    page.window.height    = 530
    page.window.resizable = False
    page.bgcolor          = BG
    page.padding          = 0

    status_text = ft.Text("", color=MUTED, size=13, italic=True)

    # ── Callbacks ─────────────────────────────────────────────────────────────
    def start_game(e):
        status_text.value = "⏳ Iniciando juego…"
        page.update()
        try:
            subprocess.Popen([sys.executable, MAIN_PATH], cwd=BASE_DIR)
            status_text.value = "✅ ¡Juego iniciado! Buena caza."
        except Exception as ex:
            status_text.value = f"❌ Error: {ex}"
        page.update()

    def exit_app(e):
        page.window.close()

    # ── Encabezado ────────────────────────────────────────────────────────────
    # SOLUCIÓN 1: Usar raw string o forward slashes para la ruta
    header = ft.Column(
    [
        # Fila para las 3 imágenes horizontales
        ft.Row(
            [
                ft.Image(
                    src=r"C:\Users\zarat\OneDrive\Desktop\DuckHunt\img\Aragon.png",
                    width=80,
                    height=80,
                    fit="contain",
                ),
                ft.Image(
                    src=r"C:\Users\zarat\OneDrive\Desktop\DuckHunt\img\Elda.png",
                    width=80,
                    height=80,
                    fit="contain",
                ),
                ft.Image(
                    src=r"C:\Users\zarat\OneDrive\Desktop\DuckHunt\img\Nancy.png",
                    width=80,
                    height=80,
                    fit="contain",
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centrar horizontalmente
            spacing=20,  # Espacio entre imágenes
        ),
        
        # Espacio opcional entre imágenes y texto
        ft.Container(height=10),
        
        # Textos
        ft.Text(
            "TEC HUNT",
            size=40,
            weight=ft.FontWeight.BOLD,
            color=ACCENT,
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Text(
            "Apunta con el dedo índice  ·  Dobla el pulgar para disparar",
            size=13,
            color=MUTED,
            text_align=ft.TextAlign.CENTER,
        ),
    ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=6,
    )

    # ── Tarjeta de controles ──────────────────────────────────────────────────
    controls_card = ft.Container(
        content=ft.Column(
            [
                ft.Text("🎮 Controles", size=15, weight=ft.FontWeight.BOLD, color=ACCENT),
                ft.Divider(color=ACCENT, height=1),
                ctrl_row("☝",  "Mira",      "Mueve el dedo índice"),
                ctrl_row("👍", "Disparo",   "Dobla el pulgar (ángulo < 0°)"),
                ctrl_row("🔄", "Reiniciar", "Presiona R en pantalla de Game Over"),
                ctrl_row("🚪", "Salir",     "Presiona Q en cualquier momento"),
            ],
            spacing=8,
        ),
        bgcolor=CARD,
        border_radius=14,
        padding=20,
    )

    # ── Botón Iniciar ─────────────────────────────────────────────────────────
    btn_play = ft.Button(
        content=ft.Row(
            [ft.Icon(ft.Icons.PLAY_ARROW, color=WHITE, size=18),
             ft.Text("Iniciar Partida", color=WHITE, size=14, weight=ft.FontWeight.BOLD)],
            spacing=8,
            tight=True,
        ),
        on_click=start_game,
        bgcolor=GREEN,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        width=210,
        height=50,
    )

    # ── Botón Salir ───────────────────────────────────────────────────────────
    btn_exit = ft.Container(
        content=ft.Text("Salir", color=RED, size=14, weight=ft.FontWeight.BOLD),
        width=140,
        height=50,
        border=ft.Border.all(2, RED),
        border_radius=10,
        alignment=ft.Alignment(0, 0),
        on_click=exit_app,
        ink=True,
    )

    # ── Footer ────────────────────────────────────────────────────────────────
    footer = ft.Text(
        "Duck Hunt © 2026  |  MediaPipe · Pygame · OpenCV · Flet",
        size=11,
        color=MUTED,
        text_align=ft.TextAlign.CENTER,
    )

    # ── Layout principal ──────────────────────────────────────────────────────
    page.add(
        ft.Container(
            bgcolor=BG,
            expand=True,
            padding=ft.Padding(left=40, top=0, right=40, bottom=0),
            content=ft.Column(
                [
                    ft.Container(height=30),
                    header,
                    ft.Container(height=20),
                    controls_card,
                    ft.Container(height=22),
                    ft.Row(
                        [btn_play, ft.Container(width=14), btn_exit],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(height=10),
                    ft.Row([status_text], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Container(height=16),
                    ft.Row([footer], alignment=ft.MainAxisAlignment.CENTER),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
        )
    )


if __name__ == "__main__":
    ft.app(target=main, assets_dir="img")  # Importante: Especificar assets_dir