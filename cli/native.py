"""Windows Native Automation CLI commands."""
import typer
from typing import Optional

from core.windows_native.services.element_service import ElementService
from core.windows_native.services.window_service import WindowService
from core.windows_native.services.input_service import InputService
from core.windows_native.services.screenshot_service import ScreenshotService
from core.windows_native.recorder.action_recorder import ActionRecorder
from core.windows_native.recorder.action_player import ActionPlayer
from core.windows_native.vision.screen_parser import ScreenParser
from core.windows_native.models.element import ElementRole

app = typer.Typer(help="Windows Native Automation commands")

_element_service = ElementService()
_window_service = WindowService()
_input_service = InputService()
_screenshot_service = ScreenshotService()
_recorder = ActionRecorder()
_player = ActionPlayer()
_parser = ScreenParser()


@app.command()
def find_window(title: str, partial: bool = typer.Option(True, "--partial/--exact")):
    """Find window by title."""
    window = _window_service.find_window(title, partial)
    if window:
        typer.echo(f"Found window: {window.name} ({window.bounds})")
    else:
        typer.echo("Window not found", err=True)
        raise typer.Exit(1)


@app.command()
def find_element(name: Optional[str] = typer.Option(None),
                 role: Optional[str] = typer.Option(None),
                 automation_id: Optional[str] = typer.Option(None)):
    """Find UI element by properties."""
    role_enum = None
    if role:
        try:
            role_enum = ElementRole(role)
        except ValueError:
            typer.echo(f"Invalid role: {role}", err=True)
            raise typer.Exit(1)

    element = _element_service.find_element(
        name=name,
        role=role_enum,
        automation_id=automation_id
    )
    if element:
        typer.echo(f"Found element: {element.name} ({element.role.value}) at {element.bounds}")
    else:
        typer.echo("Element not found", err=True)
        raise typer.Exit(1)


@app.command()
def click_element(name: str):
    """Click element by name."""
    element = _element_service.find_element(name=name)
    if element:
        if _element_service.click_element(element):
            typer.echo(f"Clicked element: {element.name}")
        else:
            typer.echo("Failed to click element", err=True)
            raise typer.Exit(1)
    else:
        typer.echo("Element not found", err=True)
        raise typer.Exit(1)


@app.command()
def type_into(name: str, text: str):
    """Type text into element."""
    element = _element_service.find_element(name=name)
    if element:
        if _element_service.type_into_element(element, text):
            typer.echo(f"Typed '{text}' into {element.name}")
        else:
            typer.echo("Failed to type", err=True)
            raise typer.Exit(1)
    else:
        typer.echo("Element not found", err=True)
        raise typer.Exit(1)


@app.command()
def dump_tree():
    """Dump current window UI tree."""
    tree = _element_service.dump_tree()
    typer.echo(tree)


@app.command()
def parse_screen():
    """Parse screen and list all elements."""
    elements = _parser.parse_screen()
    typer.echo(f"Found {len(elements)} elements:")
    for i, elem in enumerate(elements[:20], 1):  # Limit to 20
        typer.echo(f"  {i}. {elem.role.value}: {elem.name} ({elem.bounds})")


@app.command()
def screenshot(filename: str = "screenshot.png"):
    """Take screenshot using MSS."""
    img = _screenshot_service.capture()
    img.save(filename)
    typer.echo(f"Screenshot saved to {filename}")


@app.command()
def record_start():
    """Start recording actions."""
    _recorder.start()
    typer.echo("Recording started")


@app.command()
def record_stop(export: Optional[str] = typer.Option(None, "--export")):
    """Stop recording and optionally export."""
    actions = _recorder.stop()
    typer.echo(f"Recorded {len(actions)} actions")
    if export:
        _recorder.export_json(export)
        typer.echo(f"Exported to {export}")


@app.command()
def playback(file: str, speed: float = typer.Option(1.0, "--speed")):
    """Playback recorded actions."""
    _player.load_json(file)
    _player.play(speed=speed)
    typer.echo("Playback completed")
