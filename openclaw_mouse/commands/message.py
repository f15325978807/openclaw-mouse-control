"""Message dialog commands."""
import typer
from typing import Optional
import platform

app = typer.Typer(help="Message dialog commands")


@app.command()
def alert(
    text: str = typer.Argument(..., help="Alert text"),
    title: Optional[str] = typer.Option("Alert", "--title", "-t", help="Dialog title"),
):
    """Show an alert dialog."""
    system = platform.system()
    if system == "Windows":
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, text, title, 0)
    elif system == "Darwin":  # macOS
        import subprocess
        script = f'display dialog "{text}" with title "{title}" buttons {{"OK"}} default button "OK"'
        subprocess.run(["osascript", "-e", script])
    else:  # Linux
        import subprocess
        subprocess.run(["zenity", "--info", "--title", title, "--text", text])
    typer.echo("Alert shown")


@app.command()
def confirm(
    text: str = typer.Argument(..., help="Confirmation text"),
    title: Optional[str] = typer.Option("Confirm", "--title", "-t", help="Dialog title"),
):
    """Show a confirmation dialog."""
    system = platform.system()
    result = False
    if system == "Windows":
        import ctypes
        response = ctypes.windll.user32.MessageBoxW(0, text, title, 1)
        result = (response == 1)  # IDOK = 1
    elif system == "Darwin":
        import subprocess
        script = f'display dialog "{text}" with title "{title}" buttons {{"Cancel", "OK"}} default button "OK"'
        try:
            subprocess.run(["osascript", "-e", script], check=True)
            result = True
        except subprocess.CalledProcessError:
            result = False
    else:
        import subprocess
        try:
            subprocess.run(["zenity", "--question", "--title", title, "--text", text], check=True)
            result = True
        except subprocess.CalledProcessError:
            result = False
    
    typer.echo(f"User selected: {'OK' if result else 'Cancel'}")
    return result


@app.command()
def prompt(
    text: str = typer.Argument(..., help="Prompt text"),
    title: Optional[str] = typer.Option("Input", "--title", "-t", help="Dialog title"),
):
    """Show an input prompt dialog."""
    system = platform.system()
    result = ""
    if system == "Windows":
        import ctypes
        from ctypes import wintypes
        # Simple input using Windows API would be complex, using console instead
        result = input(f"{text}: ")
    elif system == "Darwin":
        import subprocess
        script = f'display dialog "{text}" with title "{title}" default answer ""'
        try:
            output = subprocess.check_output(["osascript", "-e", script], text=True)
            result = output.strip().split(":")[-1].strip()
        except subprocess.CalledProcessError:
            result = ""
    else:
        import subprocess
        try:
            result = subprocess.check_output(["zenity", "--entry", "--title", title, "--text", text], text=True).strip()
        except subprocess.CalledProcessError:
            result = ""
    
    typer.echo(f"User input: {result}")
    return result
