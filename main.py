import os
import json
import flet as ft
from logic import calcular_maioridade, calcular_idade_completa, DataFuturaError
from constants import APP_NAME
from dialogs import mostrar_sobre, mostrar_licenca

_POS_FILE = os.path.join(os.path.expanduser("~"), ".maioridade_calc_pos.json")


def _carregar_pos():
    try:
        with open(_POS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return None


def _salvar_pos(left, top):
    try:
        with open(_POS_FILE, "w") as f:
            json.dump({"left": left, "top": top}, f)
    except Exception:
        pass

_ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icon.ico")


def main(page: ft.Page):
    # --- Configurações de Janela ---
    page.title = "Maioridade Calc"
    page.window.width = 300
    page.window.height = 340
    page.window.always_on_top = True
    page.window.resizable = False
    page.window.title_bar_hidden = True
    if os.path.exists(_ICON):
        page.window.icon = _ICON

    # Estilo do Widget
    page.theme_mode = ft.ThemeMode.DARK
    page.window.bgcolor = ft.Colors.TRANSPARENT
    page.bgcolor = ft.Colors.with_opacity(0.9, "#202124")
    page.padding = ft.Padding.only(left=20, right=20, top=4, bottom=20)

    # Posição da janela: centro na primeira vez, última posição nas seguintes
    pos = _carregar_pos()
    if pos:
        page.window.left = pos["left"]
        page.window.top = pos["top"]
    else:
        page.run_task(page.window.center)

    # --- Fechar salvando posição ---
    async def _fechar(_=None):
        _salvar_pos(page.window.left, page.window.top)
        await page.window.close()

    # Estado compartilhado
    state = {"calculado": False}

    # --- Auto-slash no campo de data ---
    def on_date_change(e):
        raw = "".join(c for c in txt_input.value if c.isdigit())
        if len(raw) > 8:
            raw = raw[:8]
        if len(raw) <= 2:
            formatted = raw
        elif len(raw) <= 4:
            formatted = raw[:2] + "/" + raw[2:]
        else:
            formatted = raw[:2] + "/" + raw[2:4] + "/" + raw[4:]
        # Se o usuário editar o campo após um cálculo, reseta automaticamente
        if state["calculado"]:
            _resetar_estado()
        if txt_input.value != formatted:
            txt_input.value = formatted
        txt_input.update()

    # --- Componentes de UI ---
    txt_input = ft.TextField(
        label="Data Nascimento:",
        hint_text="DD/MM/AAAA",
        border_radius=10,
        text_size=16,
        expand=True,
        on_change=on_date_change,
        on_submit=lambda _: processar_calculo(None),
    )

    lbl_maior_titulo = ft.Text(
        "Maioridade em:", size=14, color=ft.Colors.BLUE_200, visible=False
    )
    lbl_maior_data = ft.Text(
        "", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_200, visible=False
    )
    lbl_idade_titulo = ft.Text(
        "Idade Hoje:", size=14, color=ft.Colors.BLUE_200, visible=False
    )
    lbl_idade_valor = ft.Text(
        "", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_200, visible=False
    )

    resultados = [
        lbl_maior_titulo, lbl_maior_data,
        lbl_idade_titulo, lbl_idade_valor,
    ]

    # --- Helpers de formatação ---
    def _fmt(valor, singular, plural):
        return f"{valor} {singular if valor == 1 else plural}"

    def _resetar_estado():
        state["calculado"] = False
        btn_ok.visible = True
        btn_limpar.visible = False

    # --- Ação do Botão Ok ---
    def processar_calculo(e):
        try:
            anos, meses, dias = calcular_idade_completa(txt_input.value)
            data_maior = calcular_maioridade(txt_input.value)

            # Formata omitindo componentes zerados (meses e dias)
            partes = []
            if anos > 0:
                partes.append(_fmt(anos, "ano", "anos"))
            if meses > 0:
                partes.append(_fmt(meses, "mês", "meses"))
            if dias > 0:
                partes.append(_fmt(dias, "dia", "dias"))
            if not partes:  # nasceu hoje
                partes.append("0 dias")

            lbl_maior_data.value = data_maior
            lbl_idade_valor.value = "  ".join(partes)
            for lbl in resultados:
                lbl.visible = True
            txt_input.error_text = None

            # Muda botão para Limpar
            state["calculado"] = True
            btn_ok.visible = False
            btn_limpar.visible = True
        except DataFuturaError:
            data_maior = calcular_maioridade(txt_input.value)
            lbl_maior_data.value = data_maior
            lbl_idade_valor.value = "Ainda não nasceu 👶"
            for lbl in resultados:
                lbl.visible = True
            txt_input.error_text = None
            state["calculado"] = True
            btn_ok.visible = False
            btn_limpar.visible = True
        except ValueError:
            for lbl in resultados:
                lbl.visible = False
            txt_input.error_text = "Data inválida"
        page.update()

    def limpar(e):
        txt_input.value = ""
        txt_input.error_text = None
        for lbl in resultados:
            lbl.visible = False
        _resetar_estado()
        page.update()

    btn_ok = ft.Button(
        "Ok",
        on_click=processar_calculo,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            bgcolor=ft.Colors.GREEN_300,
            color=ft.Colors.BLACK,
            padding=ft.Padding(bottom=20, top=20, left=12, right=12),
        ),
    )

    btn_limpar = ft.Button(
        "Limpar",
        on_click=limpar,
        visible=False,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            bgcolor=ft.Colors.ORANGE_300,
            color=ft.Colors.BLACK,
            padding=ft.Padding(bottom=20, top=20, left=12, right=12),
        ),
    )

    # --- Barra superior customizada (arrastável) ---
    menu_popup = ft.PopupMenuButton(
        icon=ft.Icons.MENU,
        icon_color=ft.Colors.GREY_400,
        tooltip="Menu",
        items=[
            ft.PopupMenuItem(
                content="Sobre",
                icon=ft.Icons.INFO_OUTLINE,
                on_click=lambda e: mostrar_sobre(page),
            ),
            ft.PopupMenuItem(
                content="Licença",
                icon=ft.Icons.GAVEL,
                on_click=lambda e: mostrar_licenca(page),
            ),
            ft.PopupMenuItem(),  # divisor
            ft.PopupMenuItem(
                content="Fechar",
                icon=ft.Icons.CLOSE,
                on_click=lambda e: page.run_task(_fechar),
            ),
        ],
    )

    top_bar = ft.WindowDragArea(
        ft.Row(
            [
                menu_popup,
                ft.Container(expand=True),  # espaço arrastável
                ft.IconButton(
                    ft.Icons.MINIMIZE,
                    icon_size=18,
                    on_click=lambda _: setattr(page.window, "minimized", True),
                    icon_color=ft.Colors.GREY_400,
                    tooltip="Minimizar",
                    padding=0,
                ),
                ft.IconButton(
                    ft.Icons.CLOSE,
                    icon_size=18,
                    on_click=lambda _: page.run_task(_fechar),
                    icon_color=ft.Colors.GREY_400,
                    tooltip="Fechar",
                    padding=0,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=0,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
    )

    # --- Montagem do Layout ---
    page.add(
        ft.Column(
            controls=[
                top_bar,
                ft.Row(
                    [txt_input, btn_ok, btn_limpar],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                ft.Column(
                    controls=[
                        lbl_maior_titulo,
                        lbl_maior_data,
                        ft.Divider(height=8, color=ft.Colors.TRANSPARENT),
                        lbl_idade_titulo,
                        lbl_idade_valor,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=2,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        )
    )


if __name__ == "__main__":
    import sys
    # Quando o executável é chamado com um argumento de diálogo (ex: MaioridadeCalc.exe sobre),
    # abre a janela de diálogo correspondente em vez do app principal.
    if len(sys.argv) > 1 and sys.argv[1] in ("sobre", "licenca"):
        from dialog_window import main_sobre, main_licenca
        _target = main_sobre if sys.argv[1] == "sobre" else main_licenca
        ft.run(_target)
    else:
        ft.run(main)