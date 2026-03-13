"""
Converte assets/icon.png em assets/icon.ico com múltiplos tamanhos embutidos.
Uso: python make_icon.py
"""
import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_PNG = os.path.join(_HERE, "assets", "icon.png")
_ICO = os.path.join(_HERE, "assets", "icon.ico")

SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]


def main():
    try:
        from PIL import Image
    except ImportError:
        print("Pillow não encontrado. Instale com:")
        print("  .venv\\Scripts\\pip.exe install Pillow")
        sys.exit(1)

    if not os.path.exists(_PNG):
        print(f"Arquivo não encontrado: {_PNG}")
        print("Coloque o arquivo icon.png na pasta assets/ e tente novamente.")
        sys.exit(1)

    img = Image.open(_PNG).convert("RGBA")
    img.save(_ICO, format="ICO", sizes=SIZES)
    print(f"Ícone gerado com sucesso: {_ICO}")
    print(f"Tamanhos embutidos: {[s[0] for s in SIZES]} px")


if __name__ == "__main__":
    main()
