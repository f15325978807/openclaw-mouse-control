"""Keyboard control CLI commands."""
import typer
from typing import Optional

from core.automation.engine import get_engine

app = typer.Typer(help="Keyboard control commands")
engine = get_engine()


@app.command()
def write(
    text: str = typer.Argument(..., help="Text to type"),
    interval: float = typer.Option(0.01, "--interval", "-i", help="Interval between keys in seconds"),
):
    """Type text."""
    import pyautogui
    pyautogui.write(text, interval=interval)
    typer.echo(f"Typed: {text}")


@app.command()
def press(
    key: str = typer.Argument(..., help="Key to press"),
    presses: int = typer.Option(1, "--presses", "-p", help="Number of times to press"),
    interval: float = typer.Option(0.1, "--interval", "-i", help="Interval between presses"),
):
    """Press a key."""
    import pyautogui
    pyautogui.press(key, presses=presses, interval=interval)
    typer.echo(f"Pressed '{key}' {presses} time(s)")


@app.command()
def hotkey(
    keys: str = typer.Argument(..., help="Comma-separated keys (e.g., 'ctrl,c')"),
):
    """Execute hotkey combination."""
    import pyautogui
    key_list = [k.strip() for k in keys.split(",")]
    pyautogui.hotkey(*key_list)
    typer.echo(f"Executed hotkey: {' + '.join(key_list)}")
