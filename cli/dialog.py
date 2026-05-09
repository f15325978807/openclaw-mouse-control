"""Dialog CLI commands."""
import typer
from typing import Optional

from core.automation.engine import get_engine

app = typer.Typer(help="Message dialog commands")
engine = get_engine()


@app.command()
def alert(
    text: str = typer.Argument(..., help="Alert text"),
    title: Optional[str] = typer.Option("Alert", "--title", "-t", help="Dialog title"),
):
    """Show an alert dialog."""
    engine.backend.show_alert(text, title)
    typer.echo("Alert shown")


@app.command()
def confirm(
    text: str = typer.Argument(..., help="Confirmation text"),
    title: Optional[str] = typer.Option("Confirm", "--title", "-t", help="Dialog title"),
):
    """Show a confirmation dialog."""
    result = engine.backend.show_confirm(text, title)
    typer.echo(f"User selected: {'OK' if result else 'Cancel'}")
    return result


@app.command()
def prompt(
    text: str = typer.Argument(..., help="Prompt text"),
    title: Optional[str] = typer.Option("Input", "--title", "-t", help="Dialog title"),
):
    """Show an input prompt dialog."""
    result = engine.backend.show_prompt(text, title)
    typer.echo(f"User input: {result}")
    return result
