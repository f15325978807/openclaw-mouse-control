"""Window event hook for monitoring window changes."""
import logging
import ctypes
from ctypes import wintypes
from typing import Callable, Optional
import threading

logger = logging.getLogger(__name__)

# WinEvent constants
EVENT_SYSTEM_FOREGROUND = 0x0003
EVENT_OBJECT_CREATE = 0x8000
EVENT_OBJECT_DESTROY = 0x8001
EVENT_OBJECT_SHOW = 0x8002
EVENT_OBJECT_HIDE = 0x8003
EVENT_OBJECT_FOCUS = 0x8005
WINEVENT_OUTOFCONTEXT = 0x0000


class WindowHook:
    """Hook for window events."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._hook = None
        self._callbacks: list = []
        self._is_running = False
        self._thread: Optional[threading.Thread] = None
        self._user32 = ctypes.windll.user32
        self._ole32 = ctypes.windll.ole32

        # Define callback type
        self.WINEVENTPROC = ctypes.WINFUNCTYPE(
            None,
            wintypes.HANDLE,
            wintypes.DWORD,
            wintypes.HWND,
            wintypes.LONG,
            wintypes.LONG,
            wintypes.DWORD,
            wintypes.DWORD
        )

    def register_callback(self, callback: Callable[[str, int, str], None]) -> None:
        """Register event callback.
        
        Args:
            callback: Function(event_type, hwnd, window_title)
        """
        self._callbacks.append(callback)

    def _event_callback(self, hWinEventHook, event, hwnd, idObject, idChild,
                        dwEventThread, dwmsEventTime):
        """Internal event handler."""
        try:
            # Get window title
            length = self._user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buffer = ctypes.create_unicode_buffer(length + 1)
                self._user32.GetWindowTextW(hwnd, buffer, length + 1)
                title = buffer.value
            else:
                title = ""

            # Map event to type
            event_map = {
                EVENT_SYSTEM_FOREGROUND: "foreground",
                EVENT_OBJECT_CREATE: "create",
                EVENT_OBJECT_DESTROY: "destroy",
                EVENT_OBJECT_SHOW: "show",
                EVENT_OBJECT_HIDE: "hide",
                EVENT_OBJECT_FOCUS: "focus",
            }
            event_type = event_map.get(event, f"unknown_{event}")

            # Notify callbacks
            for callback in self._callbacks:
                try:
                    callback(event_type, hwnd, title)
                except Exception as e:
                    self.logger.error(f"Callback error: {e}")
        except Exception as e:
            self.logger.error(f"Event handling error: {e}")

    def start(self) -> bool:
        """Start window hook."""
        if self._is_running:
            return True

        try:
            self._ole32.CoInitialize(None)
            callback = self.WINEVENTPROC(self._event_callback)

            # Set hook for foreground window changes
            self._hook = self._user32.SetWinEventHook(
                EVENT_SYSTEM_FOREGROUND,
                EVENT_OBJECT_FOCUS,
                0,
                callback,
                0,
                0,
                WINEVENT_OUTOFCONTEXT
            )

            if self._hook:
                self._is_running = True
                self.logger.info("Window hook started")
                return True
            else:
                self.logger.error("Failed to set hook")
                return False
        except Exception as e:
            self.logger.error(f"Failed to start hook: {e}")
            return False

    def stop(self) -> None:
        """Stop window hook."""
        if self._hook:
            self._user32.UnhookWinEvent(self._hook)
            self._hook = None
        self._is_running = False
        self._ole32.CoUninitialize()
        self.logger.info("Window hook stopped")

    def is_running(self) -> bool:
        """Check if hook is running."""
        return self._is_running
