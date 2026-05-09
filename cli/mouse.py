"""Mouse control CLI commands."""
import typer
from typing import Optional

from core.automation.engine import get_engine

app = typer.Typer(help="Mouse control commands")
engine = get_engine()


@app.command()
def move(
    x: int = typer.Argument(..., help="Target X coordinate"),
    y: int = typer.Argument(..., help="Target Y coordinate"),
    duration: float = typer.Option(0.2, "--duration", "-d", help="Movement duration in seconds"),
):
    """Move mouse to coordinates."""
    engine.backend.set_mouse_position(x, y, duration=duration)
    typer.echo(f"Mouse moved to ({x}, {y})")


@app.command()
def click(
    x: Optional[int] = typer.Argument(None, help="X coordinate (optional)"),
    y: Optional[int] = typer.Argument(None, help="Y coordinate (optional)"),
    button: str = typer.Option("left", "--button", "-b", help="Mouse button: left, right, middle"),
    clicks: int = typer.Option(1, "--clicks", "-c", help="Number of clicks"),
):
    """Click at current position or specific coordinates."""
    engine.backend.mouse_click(x, y, button=button, clicks=clicks)
    if x is not None and y is not None:
        typer.echo(f"Clicked {button} button {clicks} time(s) at ({x}, {y})")
    else:
        typer.echo(f"Clicked {button} button {clicks} time(s) at current position")


@app.command("double-click")
def double_click(
    x: Optional[int] = typer.Argument(None, help="X coordinate (optional)"),
    y: Optional[int] = typer.Argument(None, help="Y coordinate (optional)"),
):
    """Double-click at current position or specific coordinates."""
    engine.backend.mouse_click(x, y, clicks=2)
    if x is not None and y is not None:
        typer.echo(f"Double-clicked at ({x}, {y})")
    else:
        typer.echo("Double-clicked at current position")


@app.command("right-click")
def right_click(
    x: Optional[int] = typer.Argument(None, help="X coordinate (optional)"),
    y: Optional[int] = typer.Argument(None, help="Y coordinate (optional)"),
):
    """Right-click at current position or specific coordinates."""
    engine.backend.mouse_click(x, y, button="right")
    if x is not None and y is not None:
        typer.echo(f"Right-clicked at ({x}, {y})")
    else:
        typer.echo("Right-clicked at current position")


@app.command()
def drag(
    x: int = typer.Argument(..., help="Target X coordinate"),
    y: int = typer.Argument(..., help="Target Y coordinate"),
    duration: float = typer.Option(0.5, "--duration", "-d", help="Drag duration in seconds"),
    button: str = typer.Option("left", "--button", "-b", help="Mouse button to drag with"),
):
    """Drag mouse to coordinates."""
    engine.backend.mouse_drag(x, y, duration=duration, button=button)
    typer.echo(f"Dragged to ({x}, {y}) with {button} button")


@app.command()
def scroll(
    clicks: int = typer.Argument(..., help="Scroll amount (positive=up, negative=down)"),
    x: Optional[int] = typer.Argument(None, help="X coordinate (optional)"),
    y: Optional[int] = typer.Argument(None, help="Y coordinate (optional)"),
):
    """Scroll at current position or specific coordinates."""
    engine.backend.mouse_scroll(clicks, x, y)
    if x is not None and y is not None:
        typer.echo(f"Scrolled {clicks} clicks at ({x}, {y})")
    else:
        typer.echo(f"Scrolled {clicks} clicks at current position")


@app.command()
def position():
    """Get current mouse position."""
    pos = engine.backend.get_mouse_position()
    typer.echo(f"Mouse position: ({pos.x}, {pos.y})")
