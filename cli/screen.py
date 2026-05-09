"""Screen control CLI commands."""
import typer
from typing import Optional

from core.automation.engine import get_engine

app = typer.Typer(help="Screen and screenshot commands")
engine = get_engine()


@app.command()
def screenshot(
    filename: str = typer.Argument(..., help="Output filename"),
    region: Optional[str] = typer.Option(None, "--region", "-r", help="Region as 'x,y,width,height'"),
):
    """Take a screenshot."""
    if region:
        parts = [int(x) for x in region.split(",")]
        if len(parts) == 4:
            img = engine.backend.take_screenshot(tuple(parts))
        else:
            typer.echo("Error: Region must be in format 'x,y,width,height'", err=True)
            raise typer.Exit(1)
    else:
        img = engine.backend.take_screenshot()
    
    img.save(filename)
    typer.echo(f"Screenshot saved to {filename}")


@app.command()
def size():
    """Get screen size."""
    size = engine.backend.get_screen_size()
    typer.echo(f"Screen size: {size.width}x{size.height}")


@app.command()
def pixel(
    x: int = typer.Argument(..., help="X coordinate"),
    y: int = typer.Argument(..., help="Y coordinate"),
):
    """Get pixel color at coordinates."""
    import pyautogui
    color = pyautogui.pixel(x, y)
    typer.echo(f"Pixel at ({x}, {y}): RGB{color}")
