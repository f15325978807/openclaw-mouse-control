"""OpenClaw Mouse Control - Production-grade desktop automation framework."""
import typer
from typing import Optional

from cli.mouse import app as mouse_app
from cli.keyboard import app as keyboard_app
from cli.screen import app as screen_app
from cli.dialog import app as dialog_app
from cli.app import app as app_app
from core.utils.logger import setup_logging
from core.config.settings import init_config

app = typer.Typer(
    name="openclaw-mouse",
    help="OpenClaw Mouse Control - Production-grade desktop automation",
    no_args_is_help=True,
)

# Register sub-applications
app.add_typer(mouse_app, name="mouse")
app.add_typer(keyboard_app, name="keyboard")
app.add_typer(screen_app, name="screen")
app.add_typer(dialog_app, name="dialog")
app.add_typer(app_app, name="app")


@app.callback()
def main(
    config: Optional[str] = typer.Option(None, "--config", "-c", help="Path to config file"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging"),
):
    """OpenClaw Mouse Control CLI."""
    # Initialize configuration
    if config:
        from pathlib import Path
        init_config(Path(config))
    
    # Setup logging
    level = "DEBUG" if verbose else None
    setup_logging(level=level)


@app.command()
def version():
    """Show version information."""
    typer.echo("openclaw-mouse v1.0.0")


if __name__ == "__main__":
    app()
