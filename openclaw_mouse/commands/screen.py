"""Screen control commands."""
import typer
import pyautogui
from typing import Optional
import os

app = typer.Typer(help="Screen and screenshot commands")


@app.command()
def screenshot(
    filename: str = typer.Argument(..., help="Output filename"),
    region: Optional[str] = typer.Option(None, "--region", "-r", help="Region as 'x,y,width,height'"),
):
    """Take a screenshot."""
    if region:
        parts = [int(x) for x in region.split(",")]
        if len(parts) == 4:
            x, y, width, height = parts
            img = pyautogui.screenshot(region=(x, y, width, height))
        else:
            typer.echo("Error: Region must be in format 'x,y,width,height'")
            raise typer.Exit(1)
    else:
        img = pyautogui.screenshot()
    
    img.save(filename)
    typer.echo(f"Screenshot saved to {filename}")


@app.command()
def size():
    """Get screen size."""
    width, height = pyautogui.size()
    typer.echo(f"Screen size: {width}x{height}")


@app.command()
def pixel(
    x: int = typer.Argument(..., help="X coordinate"),
    y: int = typer.Argument(..., help="Y coordinate"),
):
    """Get pixel color at coordinates."""
    color = pyautogui.pixel(x, y)
    typer.echo(f"Pixel at ({x}, {y}): RGB{color}")


@app.command("on-screen")
def on_screen(
    x: int = typer.Argument(..., help="X coordinate"),
    y: int = typer.Argument(..., help="Y coordinate"),
):
    """Check if coordinates are on screen."""
    result = pyautogui.onScreen(x, y)
    typer.echo(f"Coordinates ({x}, {y}) are {'on' if result else 'off'} screen")
