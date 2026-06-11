from __future__ import annotations

import ctypes
import ctypes.wintypes

ctypes.windll.user32.SetProcessDPIAware()

__all__ = [
    "KEY_ALIASES",
    "get_cursor_position",
    "get_screen_resolution",
    "get_toggle_key_state",
    "key_down",
    "key_up",
    "left_down",
    "left_up",
    "right_down",
    "right_up",
    "set_cursor_position",
]

_ULONG_PTR = ctypes.c_ulonglong if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_ulong

_INPUT_MOUSE = 0
_INPUT_KEYBOARD = 1

_KEYEVENTF_KEYUP = 0x0002
_KEYEVENTF_SCANCODE = 0x0008
_KEYEVENTF_EXTENDEDKEY = 0x0001

_MAPVK_VK_TO_VSC_EX = 4

_MOUSEEVENTF_LEFTDOWN = 0x0002
_MOUSEEVENTF_LEFTUP = 0x0004
_MOUSEEVENTF_RIGHTDOWN = 0x0008
_MOUSEEVENTF_RIGHTUP = 0x0010

KEY_ALIASES: dict[str, int] = {
    "backspace": 0x08,
    "tab": 0x09,
    "enter": 0x0D,
    "return": 0x0D,
    "shift": 0x10,
    "ctrl": 0x11,
    "control": 0x11,
    "alt": 0x12,
    "pause": 0x13,
    "capslock": 0x14,
    "caps_lock": 0x14,
    "esc": 0x1B,
    "escape": 0x1B,
    "space": 0x20,
    " ": 0x20,
    "pageup": 0x21,
    "page_up": 0x21,
    "pagedown": 0x22,
    "page_down": 0x22,
    "end": 0x23,
    "home": 0x24,
    "left": 0x25,
    "up": 0x26,
    "right": 0x27,
    "down": 0x28,
    "insert": 0x2D,
    "delete": 0x2E,
    "del": 0x2E,
    "lwin": 0x5B,
    "rwin": 0x5C,
    "numlock": 0x90,
    "num_lock": 0x90,
    "scrolllock": 0x91,
    "scroll_lock": 0x91,
    "lshift": 0xA0,
    "rshift": 0xA1,
    "lctrl": 0xA2,
    "rctrl": 0xA3,
    "lcontrol": 0xA2,
    "rcontrol": 0xA3,
    "lalt": 0xA4,
    "ralt": 0xA5,
}

_EXTENDED_KEYS: set[int] = {
    0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28,
    0x2D, 0x2E, 0x5B, 0x5C, 0xA3, 0xA5,
}

# VkKeyScanW high-byte modifier bits -> VK codes to hold while sending the key.
_MODIFIER_VKS: dict[int, int] = {
    0x01: 0x10,  # Shift
    0x02: 0x11,  # Ctrl
    0x04: 0x12,  # Alt (VK_MENU)
}


class _MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.wintypes.LONG),
        ("dy", ctypes.wintypes.LONG),
        ("mouseData", ctypes.wintypes.DWORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", _ULONG_PTR),
    ]


class _KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.wintypes.WORD),
        ("wScan", ctypes.wintypes.WORD),
        ("dwFlags", ctypes.wintypes.DWORD),
        ("time", ctypes.wintypes.DWORD),
        ("dwExtraInfo", _ULONG_PTR),
    ]


class _HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.wintypes.DWORD),
        ("wParamL", ctypes.wintypes.WORD),
        ("wParamH", ctypes.wintypes.WORD),
    ]


class _INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", _MOUSEINPUT),
        ("ki", _KEYBDINPUT),
        ("hi", _HARDWAREINPUT),
    ]


class _INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.wintypes.DWORD),
        ("union", _INPUT_UNION),
    ]


_SendInput = ctypes.windll.user32.SendInput
_SendInput.argtypes = (ctypes.wintypes.UINT, ctypes.POINTER(_INPUT), ctypes.c_int)
_SendInput.restype = ctypes.wintypes.UINT

_MapVirtualKeyW = ctypes.windll.user32.MapVirtualKeyW
_MapVirtualKeyW.argtypes = (ctypes.wintypes.UINT, ctypes.wintypes.UINT)
_MapVirtualKeyW.restype = ctypes.wintypes.UINT

_VkKeyScanW = ctypes.windll.user32.VkKeyScanW
_VkKeyScanW.argtypes = (ctypes.wintypes.WCHAR,)
_VkKeyScanW.restype = ctypes.c_short

_GetKeyState = ctypes.windll.user32.GetKeyState
_GetKeyState.argtypes = (ctypes.c_int,)
_GetKeyState.restype = ctypes.c_short

_GetAsyncKeyState = ctypes.windll.user32.GetAsyncKeyState
_GetAsyncKeyState.argtypes = (ctypes.c_int,)
_GetAsyncKeyState.restype = ctypes.c_short

# VKs currently held down via key_down() (including auto-pressed modifiers).
_held_vks: set[int] = set()
# Main VK -> modifier VKs that key_down() auto-pressed for it, to be released on key_up().
_auto_mods: dict[int, list[int]] = {}


def _is_held(vk: int) -> bool:
    """True if vk is currently held, either by us or physically on the keyboard."""
    if vk in _held_vks:
        return True
    return bool(_GetAsyncKeyState(vk) & 0x8000)


def _send_input(input_event: _INPUT) -> None:
    sent = _SendInput(1, ctypes.byref(input_event), ctypes.sizeof(_INPUT))
    if sent != 1:
        raise ctypes.WinError()


def _mouse_event(flags: int) -> None:
    _send_input(_INPUT(
        type=_INPUT_MOUSE,
        union=_INPUT_UNION(mi=_MOUSEINPUT(
            dx=0, dy=0, mouseData=0,
            dwFlags=flags, time=0, dwExtraInfo=0,
        )),
    ))


def _vk_from_key(key: str | int) -> tuple[int, list[int]]:
    """Returns (vk_code, [required_modifier_vks])."""
    if isinstance(key, int): # If VK int supplied, just return it.
        return key, []

    # Edge cases where .strip() breaks.
    if key == " ":
        return KEY_ALIASES['space'], []
    if key == '\n':
        return KEY_ALIASES['enter'], []
    if key == '\t':
        return KEY_ALIASES['tab'], []
    if key == '\b':
        return KEY_ALIASES['backspace'], []

    normalized_key = key.strip().lower() 
    if normalized_key in KEY_ALIASES:
        return KEY_ALIASES[normalized_key], []

    if normalized_key.startswith("f") and normalized_key[1:].isdigit():
        function_key = int(normalized_key[1:])
        if 1 <= function_key <= 24:
            return 0x70 + function_key - 1, []

    if len(normalized_key) == 1:
        if normalized_key.isalnum():
            return ord(normalized_key.upper()), []

        scan_result = _VkKeyScanW(normalized_key)
        if scan_result != -1:
            vk = scan_result & 0xFF
            mod_byte = (scan_result >> 8) & 0xFF
            mods = [vk_mod for bit, vk_mod in _MODIFIER_VKS.items() if mod_byte & bit]
            return vk, mods

    raise ValueError(f"Unsupported key for SendInput: {key!r}")


def _send_key_event(vk: int, is_key_up: bool = False) -> None:
    scan_code = _MapVirtualKeyW(vk, _MAPVK_VK_TO_VSC_EX)
    if scan_code == 0:
        raise ValueError(f"MapVirtualKeyW returned 0 for VK 0x{vk:02X}")
    flags = _KEYEVENTF_SCANCODE
    if vk in _EXTENDED_KEYS:
        flags |= _KEYEVENTF_EXTENDEDKEY
    if is_key_up:
        flags |= _KEYEVENTF_KEYUP

    _send_input(_INPUT(
        type=_INPUT_KEYBOARD,
        union=_INPUT_UNION(ki=_KEYBDINPUT(
            wVk=0, wScan=scan_code,
            dwFlags=flags, time=0, dwExtraInfo=0,
        )),
    ))


def set_cursor_position(x: int, y: int) -> None:
    """Moves the cursor to the given screen coordinates."""
    ctypes.windll.user32.SetCursorPos(int(x), int(y))


def get_screen_resolution() -> tuple[int, int]:
    """Returns the primary screen resolution as (width, height)."""
    width = ctypes.windll.user32.GetSystemMetrics(0)
    height = ctypes.windll.user32.GetSystemMetrics(1)
    return width, height


def get_cursor_position() -> tuple[int, int]:
    """Returns the current cursor position as (x, y)."""
    pos = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pos))
    return pos.x, pos.y


def get_toggle_key_state(key: str | int) -> int:
    """Returns 1 if the toggle key is on, 0 if off. Works for capslock, numlock, scrolllock."""
    vk, _ = _vk_from_key(key)
    return int(_GetKeyState(vk) & 0x0001)


def left_down() -> None:
    """Presses and holds the left mouse button."""
    _mouse_event(_MOUSEEVENTF_LEFTDOWN)


def left_up() -> None:
    """Releases the left mouse button."""
    _mouse_event(_MOUSEEVENTF_LEFTUP)


def right_down() -> None:
    """Presses and holds the right mouse button."""
    _mouse_event(_MOUSEEVENTF_RIGHTDOWN)


def right_up() -> None:
    """Releases the right mouse button."""
    _mouse_event(_MOUSEEVENTF_RIGHTUP)


def key_down(key: str | int) -> None:
    """Presses and holds key, auto-pressing any required modifiers (e.g. Shift for '!') that aren't already held."""
    vk, mods = _vk_from_key(key)
    pressed_mods = []
    for mod_vk in mods:
        if not _is_held(mod_vk):
            _send_key_event(mod_vk)
            _held_vks.add(mod_vk)
            pressed_mods.append(mod_vk)
    _send_key_event(vk)
    _held_vks.add(vk)
    if pressed_mods:
        _auto_mods.setdefault(vk, []).extend(pressed_mods)


def key_up(key: str | int) -> None:
    """Releases key, and releases any modifiers that key_down() auto-pressed for it."""
    vk, _mods = _vk_from_key(key)
    _send_key_event(vk, is_key_up=True)
    _held_vks.discard(vk)
    for mod_vk in reversed(_auto_mods.pop(vk, [])):
        _send_key_event(mod_vk, is_key_up=True)
        _held_vks.discard(mod_vk)
