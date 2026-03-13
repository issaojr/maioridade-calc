"""
Janela filha independente (subprocess).
Uso: python dialog_window.py [sobre|licenca]
"""
import os
import sys
import flet as ft
from constants import (
    APP_NAME, APP_VERSION, APP_AUTHOR, APP_EMAIL,
    APP_REPO, APP_LICENSE_TYPE, LICENSE_TEXT,
)

_BG = "#2c2d30"
_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icon.ico")


def _setup(page: ft.Page, titulo: str, width: int, height: int):
    page.title = titulo
    page.window.width = width
    page.window.height = height
    page.window.resizable = False
    page.window.maximizable = False
    page.window.always_on_top = True
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = _BG
    page.padding = 20
    if os.path.exists(_ICON):
        page.window.icon = _ICON
    page.run_task(page.window.center)


def main_sobre(page: ft.Page):
    _setup(page, f"Sobre – {APP_NAME}", 400, 500)

    page.add(
        ft.Column(
            expand=True,
            controls=[
                ft.Text(
                    APP_NAME,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Text(
                    f"Versão {APP_VERSION}",
                    size=13,
                    color=ft.Colors.GREY_400,
                ),
                ft.Divider(height=16),
                ft.Text("Autor", size=12, color=ft.Colors.GREY_400),
                ft.Text(APP_AUTHOR, size=14, color=ft.Colors.WHITE),
                ft.Text(APP_EMAIL, size=12, color=ft.Colors.BLUE_200),
                ft.Divider(height=16),
                ft.Text("Repositório", size=12, color=ft.Colors.GREY_400),
                ft.TextButton(
                    "github.com/issaojr/maioridade-calc",
                    url=APP_REPO,
                    style=ft.ButtonStyle(color=ft.Colors.BLUE_200),
                ),
                ft.Divider(height=16),
                ft.Text(
                    f"Licença: {APP_LICENSE_TYPE}",
                    size=12,
                    color=ft.Colors.GREY_400,
                ),
                ft.Container(expand=True),
                ft.Row(
                    [
                        ft.Button(
                            "Fechar",
                            on_click=lambda _: page.run_task(page.window.close),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                bgcolor=ft.Colors.BLUE_GREY_700,
                                color=ft.Colors.WHITE,
                            ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=4,
        )
    )


def main_licenca(page: ft.Page):
    _setup(page, f"Licença {APP_LICENSE_TYPE} – {APP_NAME}", 600, 600)

    page.add(
        ft.Column(
            expand=True,
            controls=[
                ft.Text(
                    f"Licença {APP_LICENSE_TYPE}",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Divider(height=10),
                ft.Container(
                    expand=True,
                    content=ft.TextField(
                        value=LICENSE_TEXT,
                        multiline=True,
                        read_only=True,
                        text_size=11,
                        color=ft.Colors.GREY_300,
                        bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.WHITE),
                        border_color=ft.Colors.with_opacity(0.2, ft.Colors.WHITE),
                        border_radius=6,
                        expand=True,
                    ),
                ),
                ft.Divider(height=10),
                ft.Row(
                    [
                        ft.Button(
                            "Fechar",
                            on_click=lambda _: page.run_task(page.window.close),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                                bgcolor=ft.Colors.BLUE_GREY_700,
                                color=ft.Colors.WHITE,
                            ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=4,
        )
    )


if __name__ == "__main__":
    dialog_type = sys.argv[1] if len(sys.argv) > 1 else "sobre"
    if dialog_type == "licenca":
        ft.run(main_licenca)
    else:
        ft.run(main_sobre)
