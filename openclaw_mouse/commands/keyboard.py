"""Keyboard control commands."""
import typer
import pyautogui
from typing import Optional

app = typer.Typer(help="Keyboard control commands")


@app.command()
def write(
    text: str = typer.Argument(..., help="Text to type"),
    interval: float = typer.Option(0.01, "--interval", "-i", help="Interval between keys in seconds"),
):
    """Type text."""
    pyautogui.write(text, interval=interval)
    typer.echo(f"Typed: {text}")


@app.command()
def press(
    key: str = typer.Argument(..., help="Key to press"),
    presses: int = typer.Option(1, "--presses", "-p", help="Number of times to press"),
    interval: float = typer.Option(0.1, "--interval", "-i", help="Interval between presses"),
):
    """Press a key."""
    pyautogui.press(key, presses=presses, interval=interval)
    typer.echo(f"Pressed '{key}' {presses} time(s)")


@app.command()
def hotkey(
    keys: str = typer.Argument(..., help="Comma-separated keys (e.g., 'ctrl,c')"),
):
    """Execute hotkey combination."""
    key_list = [k.strip() for k in keys.split(",")]
    pyautogui.hotkey(*key_list)
    typer.echo(f"Executed hotkey: {' + '.join(key_list)}")


@app.command()
def keydown(
    key: str = typer.Argument(..., help="Key to hold down"),
):
    """Hold down a key."""
    pyautogui.keyDown(key)
    typer.echo(f"Holding down '{key}'")


@app.command()
def keyup(
    key: str = typer.Argument(..., help="Key to release"),
):
    """Release a key."""
    pyautogui.keyUp(key)
    typer.echo(f"Released '{key}'")
