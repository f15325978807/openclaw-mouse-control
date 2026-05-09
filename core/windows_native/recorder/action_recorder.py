"""Action recorder for capturing user interactions."""
import logging
import time
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class ActionType(Enum):
    """Types of recordable actions."""
    MOUSE_CLICK = "mouse_click"
    MOUSE_MOVE = "mouse_move"
    MOUSE_SCROLL = "mouse_scroll"
    KEY_PRESS = "key_press"
    KEY_HOTKEY = "key_hotkey"
    WINDOW_FOCUS = "window_focus"
    WINDOW_OPEN = "window_open"
    ELEMENT_CLICK = "element_click"
    ELEMENT_TYPE = "element_type"
    DELAY = "delay"


@dataclass
class RecordedAction:
    """Single recorded action."""
    action_type: ActionType
    timestamp: float
    data: Dict[str, Any]
    duration: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "action_type": self.action_type.value,
            "timestamp": self.timestamp,
            "data": self.data,
            "duration": self.duration
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecordedAction":
        """Create from dictionary."""
        return cls(
            action_type=ActionType(data["action_type"]),
            timestamp=data["timestamp"],
            data=data["data"],
            duration=data.get("duration", 0.0)
        )


class ActionRecorder:
    """Records user actions for playback."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._actions: List[RecordedAction] = []
        self._is_recording = False
        self._start_time: float = 0.0
        self._last_action_time: float = 0.0

    def start(self) -> None:
        """Start recording."""
        self._actions = []
        self._is_recording = True
        self._start_time = time.time()
        self._last_action_time = self._start_time
        self.logger.info("Recording started")

    def stop(self) -> List[RecordedAction]:
        """Stop recording and return actions."""
        self._is_recording = False
        self.logger.info(f"Recording stopped. {len(self._actions)} actions recorded")
        return self._actions.copy()

    def is_recording(self) -> bool:
        """Check if currently recording."""
        return self._is_recording

    def _add_action(self, action_type: ActionType, data: Dict[str, Any]) -> None:
        """Add action to recording."""
        if not self._is_recording:
            return

        current_time = time.time()
        duration = current_time - self._last_action_time

        action = RecordedAction(
            action_type=action_type,
            timestamp=current_time - self._start_time,
            data=data,
            duration=duration
        )
        self._actions.append(action)
        self._last_action_time = current_time

    def record_mouse_click(self, x: int, y: int, button: str = "left") -> None:
        """Record mouse click."""
        self._add_action(ActionType.MOUSE_CLICK, {
            "x": x,
            "y": y,
            "button": button
        })

    def record_mouse_move(self, x: int, y: int) -> None:
        """Record mouse move."""
        self._add_action(ActionType.MOUSE_MOVE, {
            "x": x,
            "y": y
        })

    def record_mouse_scroll(self, clicks: int, x: int, y: int) -> None:
        """Record mouse scroll."""
        self._add_action(ActionType.MOUSE_SCROLL, {
            "clicks": clicks,
            "x": x,
            "y": y
        })

    def record_key_press(self, key: str) -> None:
        """Record key press."""
        self._add_action(ActionType.KEY_PRESS, {
            "key": key
        })

    def record_hotkey(self, keys: List[str]) -> None:
        """Record hotkey."""
        self._add_action(ActionType.KEY_HOTKEY, {
            "keys": keys
        })

    def record_window_focus(self, window_title: str) -> None:
        """Record window focus."""
        self._add_action(ActionType.WINDOW_FOCUS, {
            "window_title": window_title
        })

    def record_element_click(self, element_name: str, element_role: str) -> None:
        """Record element click."""
        self._add_action(ActionType.ELEMENT_CLICK, {
            "element_name": element_name,
            "element_role": element_role
        })

    def record_element_type(self, element_name: str, text: str) -> None:
        """Record element text input."""
        self._add_action(ActionType.ELEMENT_TYPE, {
            "element_name": element_name,
            "text": text
        })

    def record_delay(self, seconds: float) -> None:
        """Record explicit delay."""
        self._add_action(ActionType.DELAY, {
            "seconds": seconds
        })

    def export_json(self, filepath: str) -> None:
        """Export actions to JSON file."""
        data = {
            "version": "1.0",
            "total_actions": len(self._actions),
            "actions": [action.to_dict() for action in self._actions]
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        self.logger.info(f"Actions exported to {filepath}")

    def export_workflow(self, filepath: str) -> None:
        """Export as YAML workflow."""
        try:
            import yaml
            workflow = {"workflow": []}
            for action in self._actions:
                step = self._action_to_workflow_step(action)
                if step:
                    workflow["workflow"].append(step)

            with open(filepath, "w", encoding="utf-8") as f:
                yaml.dump(workflow, f, default_flow_style=False, allow_unicode=True)
            self.logger.info(f"Workflow exported to {filepath}")
        except ImportError:
            self.logger.error("PyYAML required for workflow export")

    def _action_to_workflow_step(self, action: RecordedAction) -> Optional[Dict[str, Any]]:
        """Convert action to workflow step."""
        if action.action_type == ActionType.MOUSE_CLICK:
            return {"click": f"({action.data['x']}, {action.data['y']})"}
        elif action.action_type == ActionType.ELEMENT_CLICK:
            return {"click": action.data["element_name"]}
        elif action.action_type == ActionType.ELEMENT_TYPE:
            return {"type": action.data["text"], "into": action.data["element_name"]}
        elif action.action_type == ActionType.WINDOW_FOCUS:
            return {"focus": action.data["window_title"]}
        elif action.action_type == ActionType.KEY_PRESS:
            return {"press": action.data["key"]}
        elif action.action_type == ActionType.DELAY:
            return {"delay": action.data["seconds"]}
        return None

    def clear(self) -> None:
        """Clear recorded actions."""
        self._actions = []
        self.logger.debug("Recording cleared")
