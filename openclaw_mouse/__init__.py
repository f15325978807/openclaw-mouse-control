"""OpenClaw Mouse Control - CLI for mouse automation."""
import typer
from openclaw_mouse.commands import mouse, keyboard, screen, message, app

app_cli = typer.Typer(
    name="openclaw-mouse",
    help="Control your mouse with automation for OpenClaw",
    no_args_is_help=True,
)

# Register sub-applications
app_cli.add_typer(mouse.app, name="mouse")
app_cli.add_typer(keyboard.app, name="keyboard")
app_cli.add_typer(screen.app, name="screen")
app_cli.add_typer(message.app, name="message")
app_cli.add_typer(app.app, name="app")


@app_cli.command()
def version():
    """Show version information."""
    typer.echo("openclaw-mouse v1.0.0")
