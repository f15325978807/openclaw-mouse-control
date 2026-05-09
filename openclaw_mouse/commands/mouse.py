"""Mouse control commands."""
import typer
import pyautogui
from typing import Optional

app = typer.Typer(help="Mouse control commands")


@app.command()
def move(
    x: int = typer.Argument(..., help="Target X coordinate"),
    y: int = typer.Argument(..., help="Target Y coordinate"),
    duration: float = typer.Option(0.2, "--duration", "-d", help="Movement duration in seconds"),
):
    """Move mouse to coordinates."""
    pyautogui.moveTo(x, y, duration=duration)
    typer.echo(f"Mouse moved to ({x}, {y})")


@app.command()
def click(
    x: Optional[int] = typer.Argument(None, help="X coordinate (optional)"),
    y: Optional[int] = typer.Argument(None, help="Y coordinate (optional)"),
    button: str = typer.Option("left", "--button", "-b", help="Mouse button: left, right, middle"),
    clicks: int = typer.Option(1, "--clicks", "-c", help="Number of clicks"),
):
    """Click at current position or specific coordinates."""
    if x is not None and y is not None:
        pyautogui.click(x, y, button=button, clicks=clicks)
        typer.echo(f"Clicked {button} button {clicks} time(s) at ({x}, {y})")
    else:
        pyautogui.click(button=button, clicks=clicks)
        typer.echo(f"Clicked {button} button {clicks} time(s) at current position")


@app.command("double-click")
def double_click(
    x: Optional[int] = typer.Argument(None, help="X coordinate (optional)"),
    y: Optional[int] = typer.Argument(None, help="Y coordinate (optional)"),
):
    """Double-click at current position or specific coordinates."""
    if x is not None and y is not None:
        pyautogui.doubleClick(x, y)
        typer.echo(f"Double-clicked at ({x}, {y})")
    else:
        pyautogui.doubleClick()
        typer.echo("Double-clicked at current position")


@app.command("right-click")
def right_click(
    x: Optional[int] = typer.Argument(None, help="X coordinate (optional)"),
    y: Optional[int] = typer.Argument(None, help="Y coordinate (optional)"),
):
    """Right-click at current position or specific coordinates."""
    if x is not None and y is not None:
        pyautogui.rightClick(x, y)
        typer.echo(f"Right-clicked at ({x}, {y})")
    else:
        pyautogui.rightClick()
        typer.echo("Right-clicked at current position")


@app.command("middle-click")
def middle_click(
    x: Optional[int] = typer.Argument(None, help="X coordinate (optional)"),
    y: Optional[int] = typer.Argument(None, help="Y coordinate (optional)"),
):
    """Middle-click at current position or specific coordinates."""
    if x is not None and y is not None:
        pyautogui.middleClick(x, y)
        typer.echo(f"Middle-clicked at ({x}, {y})")
    else:
        pyautogui.middleClick()
        typer.echo("Middle-clicked at current position")


@app.command()
def drag(
    x: int = typer.Argument(..., help="Target X coordinate"),
    y: int = typer.Argument(..., help="Target Y coordinate"),
    duration: float = typer.Option(0.5, "--duration", "-d", help="Drag duration in seconds"),
    button: str = typer.Option("left", "--button", "-b", help="Mouse button to drag with"),
):
    """Drag mouse to coordinates."""
    pyautogui.dragTo(x, y, duration=duration, button=button)
    typer.echo(f"Dragged to ({x}, {y}) with {button} button")


@app.command()
def scroll(
    clicks: int = typer.Argument(..., help="Scroll amount (positive=up, negative=down)"),
    x: Optional[int] = typer.Argument(None, help="X coordinate (optional)"),
    y: Optional[int] = typer.Argument(None, help="Y coordinate (optional)"),
):
    """Scroll at current position or specific coordinates."""
    if x is not None and y is not None:
        pyautogui.scroll(clicks, x, y)
        typer.echo(f"Scrolled {clicks} clicks at ({x}, {y})")
    else:
        pyautogui.scroll(clicks)
        typer.echo(f"Scrolled {clicks} clicks at current position")


@app.command()
def position():
    """Get current mouse position."""
    x, y = pyautogui.position()
    typer.echo(f"Mouse position: ({x}, {y})")
