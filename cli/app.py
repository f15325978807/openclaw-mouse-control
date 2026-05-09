"""Application control CLI commands."""
import typer
from typing import Optional, List

from core.automation.engine import get_engine

app = typer.Typer(help="Application control commands")
engine = get_engine()


@app.command()
def open(
    name: str = typer.Argument(..., help="Application name"),
    args: Optional[List[str]] = typer.Option(None, "--arg", help="Additional arguments"),
):
    """Open an application."""
    if engine.backend.open_application(name, args):
        typer.echo(f"Opened {name}")
    else:
        typer.echo(f"Failed to open {name}", err=True)
        raise typer.Exit(1)


@app.command()
def focus(
    name: str = typer.Argument(..., help="Window title or application name"),
):
    """Focus on a window."""
    window = engine.backend.find_window(name)
    if window:
        if engine.backend.focus_window(window):
            typer.echo(f"Focused on {window.title}")
        else:
            typer.echo(f"Failed to focus on {name}", err=True)
            raise typer.Exit(1)
    else:
        typer.echo(f"Window '{name}' not found", err=True)
        raise typer.Exit(1)


@app.command()
def list():
    """List all visible windows."""
    windows = engine.backend.get_visible_windows()
    if windows:
        typer.echo("Visible windows:")
        for i, window in enumerate(windows, 1):
            typer.echo(f"  {i}. {window.title}")
    else:
        typer.echo("No visible windows found")
