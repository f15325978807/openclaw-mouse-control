"""Application control commands."""
import typer
import subprocess
import platform
from typing import Optional, List

app = typer.Typer(help="Application control commands")


@app.command()
def open(
    name: str = typer.Argument(..., help="Application name"),
    args: Optional[List[str]] = typer.Option(None, "--arg", help="Additional arguments"),
):
    """Open an application."""
    system = platform.system()
    try:
        if system == "Windows":
            if args:
                subprocess.Popen([name] + args, shell=True)
            else:
                subprocess.Popen([name], shell=True)
        elif system == "Darwin":  # macOS
            cmd = ["open", "-a", name]
            if args:
                cmd.extend(args)
            subprocess.Popen(cmd)
        else:  # Linux
            cmd = [name]
            if args:
                cmd.extend(args)
            subprocess.Popen(cmd)
        typer.echo(f"Opened {name}")
    except Exception as e:
        typer.echo(f"Error opening {name}: {e}")


@app.command()
def focus(
    name: str = typer.Argument(..., help="Window title or application name"),
):
    """Focus on a window."""
    system = platform.system()
    try:
        if system == "Windows":
            import ctypes
            from ctypes import wintypes
            
            def window_enum_callback(hwnd, extra):
                if ctypes.windll.user32.IsWindowVisible(hwnd):
                    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                    if length > 0:
                        buffer = ctypes.create_unicode_buffer(length + 1)
                        ctypes.windll.user32.GetWindowTextW(hwnd, buffer, length + 1)
                        if name.lower() in buffer.value.lower():
                            ctypes.windll.user32.SetForegroundWindow(hwnd)
                            return False
                return True
            
            enum_windows_proc = ctypes.WINFUNCTYPE(
                wintypes.BOOL,
                wintypes.HWND,
                wintypes.LPARAM
            )
            ctypes.windll.user32.EnumWindows(enum_windows_proc(window_enum_callback), 0)
            
        elif system == "Darwin":
            script = f'tell application "{name}" to activate'
            subprocess.run(["osascript", "-e", script])
        else:
            # Linux - try using wmctrl
            subprocess.run(["wmctrl", "-a", name])
        typer.echo(f"Focused on {name}")
    except Exception as e:
        typer.echo(f"Error focusing on {name}: {e}")


@app.command()
def list():
    """List all visible windows."""
    system = platform.system()
    windows = []
    try:
        if system == "Windows":
            import ctypes
            from ctypes import wintypes
            
            def window_enum_callback(hwnd, extra):
                if ctypes.windll.user32.IsWindowVisible(hwnd):
                    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                    if length > 0:
                        buffer = ctypes.create_unicode_buffer(length + 1)
                        ctypes.windll.user32.GetWindowTextW(hwnd, buffer, length + 1)
                        if buffer.value.strip():
                            windows.append(buffer.value)
                return True
            
            enum_windows_proc = ctypes.WINFUNCTYPE(
                wintypes.BOOL,
                wintypes.HWND,
                wintypes.LPARAM
            )
            ctypes.windll.user32.EnumWindows(enum_windows_proc(window_enum_callback), 0)
            
        elif system == "Darwin":
            script = 'tell application "System Events" to get name of every application process whose visible is true'
            output = subprocess.check_output(["osascript", "-e", script], text=True)
            windows = [w.strip() for w in output.split(",") if w.strip()]
        else:
            # Linux
            output = subprocess.check_output(["wmctrl", "-l"], text=True)
            for line in output.strip().split("\n"):
                parts = line.split(None, 3)
                if len(parts) >= 4:
                    windows.append(parts[3])
        
        if windows:
            typer.echo("Visible windows:")
            for i, window in enumerate(windows, 1):
                typer.echo(f"  {i}. {window}")
        else:
            typer.echo("No visible windows found")
    except Exception as e:
        typer.echo(f"Error listing windows: {e}")
