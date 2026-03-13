import subprocess
import asyncio
import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_DIALOG_SCRIPT = os.path.join(_HERE, "dialog_window.py")


async def _abrir_async(dialog_type: str, page):
    if getattr(sys, "frozen", False):
        cmd = [sys.executable, dialog_type]
    else:
        cmd = [sys.executable, _DIALOG_SCRIPT, dialog_type]

    flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

    page.disabled = True
    page.update()

    proc = await asyncio.create_subprocess_exec(*cmd, creationflags=flags)
    await proc.wait()

    page.disabled = False
    page.window.focused = True
    page.update()


def mostrar_sobre(page=None, e=None):
    if page is not None:
        async def _run():
            await _abrir_async("sobre", page)
        page.run_task(_run)


def mostrar_licenca(page=None, e=None):
    if page is not None:
        async def _run():
            await _abrir_async("licenca", page)
        page.run_task(_run)
