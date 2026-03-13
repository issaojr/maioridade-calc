"""
Gera o executável de distribuição do Maioridade Calc.
Uso: python build.py [--onedir]
  --onedir  Gera uma pasta em vez de arquivo único (mais compatível)
"""
import os
import sys
import subprocess
import argparse

_HERE = os.path.dirname(os.path.abspath(__file__))
_ICO = os.path.join(_HERE, "assets", "icon.ico")
_PNG = os.path.join(_HERE, "assets", "icon.png")
_FLET = os.path.join(_HERE, ".venv", "Scripts", "flet.exe")

from constants import APP_NAME, APP_VERSION


def gerar_ico():
    if os.path.exists(_ICO):
        print(f"Ícone já existe: {_ICO}")
        return True
    if not os.path.exists(_PNG):
        print("Aviso: assets/icon.png não encontrado — buildando sem ícone.")
        return False
    result = subprocess.run([sys.executable, "make_icon.py"])
    return result.returncode == 0 and os.path.exists(_ICO)


def main():
    parser = argparse.ArgumentParser(description="Build do Maioridade Calc")
    parser.add_argument(
        "--onedir", action="store_true",
        help="Gera pasta em vez de arquivo único (recomendado para ambientes corporativos)"
    )
    args = parser.parse_args()

    tem_ico = gerar_ico()

    cmd = [
        _FLET, "pack", "main.py",
        "--name", "MaioridadeCalc",
        "--product-name", APP_NAME,
        "--product-version", APP_VERSION,
        "--file-version", APP_VERSION + ".0",
        "-y",
    ]

    if tem_ico:
        cmd += ["--icon", _ICO]

    if args.onedir:
        cmd.append("-D")

    mode = "pasta (--onedir)" if args.onedir else "arquivo único"
    print(f"\nGerando build: {mode}")
    print(f"Versão: {APP_VERSION}")
    print(f"Comando: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, cwd=_HERE)

    if result.returncode == 0:
        dist = os.path.join(_HERE, "dist")
        print(f"\nBuild concluído! Arquivos em: {dist}")
    else:
        print("\nErro durante o build.")
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()
