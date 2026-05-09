"""Action player for replaying recorded actions."""
import logging
import time
from typing import List, Optional

from .action_recorder import RecordedAction, ActionType
from ..services.element_service import ElementService
from ..services.input_service import InputService
from ..services.window_service import WindowService

logger = logging.getLogger(__name__)


class ActionPlayer:
    """Plays back recorded actions."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._element_service = ElementService()
        self._input_service = InputService()
        self._window_service = WindowService()
        self._is_playing = False
        self._current_index = 0
        self._actions: List[RecordedAction] = []

    def load_actions(self, actions: List[RecordedAction]) -> None:
        """Load actions for playback."""
        self._actions = actions
        self._current_index = 0
        self.logger.info(f"Loaded {len(actions)} actions")

    def load_json(self, filepath: str) -> None:
        """Load actions from JSON file."""
        import json
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._actions = [RecordedAction.from_dict(a) for a in data["actions"]]
        self._current_index = 0
        self.logger.info(f"Loaded {len(self._actions)} actions from {filepath}")

    def play(self, speed: float = 1.0) -> None:
        """Play all actions."""
        if not self._actions:
            self.logger.warning("No actions to play")
            return

        self._is_playing = True
        self.logger.info(f"Starting playback at {speed}x speed")

        for i, action in enumerate(self._actions):
            if not self._is_playing:
                break

            self._current_index = i
            self._execute_action(action)

            # Wait between actions (scaled by speed)
            if i < len(self._actions) - 1:
                delay = action.duration / speed
                if delay > 0:
                    time.sleep(delay)

        self._is_playing = False
        self.logger.info("Playback completed")

    def stop(self) -> None:
        """Stop playback."""
        self._is_playing = False
        self.logger.info("Playback stopped")

    def step(self) -> bool:
        """Execute single step. Returns True if more steps available."""
        if self._current_index >= len(self._actions):
            return False

        action = self._actions[self._current_index]
        self._execute_action(action)
        self._current_index += 1
        return self._current_index < len(self._actions)

    def _execute_action(self, action: RecordedAction) -> None:
        """Execute single action."""
        try:
            if action.action_type == ActionType.MOUSE_CLICK:
                self._input_service.click(
                    action.data["x"],
                    action.data["y"],
                    action.data.get("button", "left")
                )
            elif action.action_type == ActionType.MOUSE_MOVE:
                self._input_service.move_to(
                    action.data["x"],
                    action.data["y"]
                )
            elif action.action_type == ActionType.MOUSE_SCROLL:
                self._input_service.scroll(
                    action.data["clicks"],
                    action.data["x"],
                    action.data["y"]
                )
            elif action.action_type == ActionType.KEY_PRESS:
                self._input_service.press_key(action.data["key"])
            elif action.action_type == ActionType.KEY_HOTKEY:
                self._input_service.hotkey(*action.data["keys"])
            elif action.action_type == ActionType.WINDOW_FOCUS:
                window = self._window_service.find_window(action.data["window_title"])
                if window:
                    self._window_service.focus_window(window)
            elif action.action_type == ActionType.ELEMENT_CLICK:
                element = self._element_service.find_element(name=action.data["element_name"])
                if element:
                    self._element_service.click_element(element)
            elif action.action_type == ActionType.ELEMENT_TYPE:
                element = self._element_service.find_element(name=action.data["element_name"])
                if element:
                    self._element_service.type_into_element(element, action.data["text"])
            elif action.action_type == ActionType.DELAY:
                time.sleep(action.data["seconds"])

            self.logger.debug(f"Executed: {action.action_type.value}")
        except Exception as e:
            self.logger.error(f"Failed to execute action {action.action_type.value}: {e}")

    def is_playing(self) -> bool:
        """Check if currently playing."""
        return self._is_playing
