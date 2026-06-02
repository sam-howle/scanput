import time
from scanput import (
    key_down, key_up,
    left_down, left_up,
    right_down, right_up,
    get_cursor_position, set_cursor_position,
)

KEY_HOLD_TIME = 0.08
BETWEEN_KEYPRESS_DELAY = 0.12

print("Focus a text field. Starting in 5 seconds...")
time.sleep(5)

alphabet = "abcdefghijklmnopqrstuvwxyz"
specials = ["space", "enter", "!", "@", "#", "$", "%", "tab", "1", "2", "3"]

print ("typing the alphabet.")
for char in alphabet:
    key_down(char)
    time.sleep(KEY_HOLD_TIME)
    key_up(char)
    time.sleep(BETWEEN_KEYPRESS_DELAY)

key_down("shift")
print("Typing the alphabet while KEY_HOLD_TIMEing shift.")
for char in alphabet:
    key_down(char)
    time.sleep(KEY_HOLD_TIME)
    key_up(char)
    time.sleep(BETWEEN_KEYPRESS_DELAY)
key_up("shift")
time.sleep(BETWEEN_KEYPRESS_DELAY)

print("Typing special characters.")
for key in specials:
    key_down(key)
    time.sleep(KEY_HOLD_TIME)
    key_up(key)
    time.sleep(BETWEEN_KEYPRESS_DELAY)

# New line for next section
key_down('enter')
time.sleep(KEY_HOLD_TIME)
key_up('enter')
time.sleep(BETWEEN_KEYPRESS_DELAY)

print("Typing keys by VK integers.")
print("For a full list, see https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes")

# Example VK integer inputs. Useful for OEM/punctuation keys where the
# scan code is more reliable than assuming keyboard layout.
# Full reference: https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
example_vk_ints = [
    (0xBC, "comma (,)"),
    (0xBE, "period (.)"),
    (0xBF, "forward slash (/)"),
    (0xBD, "minus/hyphen (-)"),
    (0xBB, "equals (=)"),
    (0xBA, "semicolon (;)"),
    (0xDB, "open bracket ([)"),
    (0xDD, "close bracket (])"),
    (0xDC, "backslash (\\)"),
    (0xDE, "apostrophe (')"),
    (0xC0, "backtick (`)"),
]
print("Typing a few sample inputs by VK integer codes.")
for vk, label in example_vk_ints:
    print(f"  0x{vk:02X} -> {label}")
    key_down(vk)
    time.sleep(KEY_HOLD_TIME)
    key_up(vk)
    time.sleep(BETWEEN_KEYPRESS_DELAY)

x, y = get_cursor_position()
print(f"Current mouse position: ({x}, {y})")

dest_x, dest_y = x + 300, y - 150
print(f"Teleporting mouse to ({dest_x}, {dest_y})")
set_cursor_position(dest_x, dest_y)
time.sleep(BETWEEN_KEYPRESS_DELAY)

print("Left click.")
left_down()
time.sleep(KEY_HOLD_TIME)
left_up()
time.sleep(BETWEEN_KEYPRESS_DELAY)

print("Right click.")
right_down()
time.sleep(KEY_HOLD_TIME)
right_up()
time.sleep(BETWEEN_KEYPRESS_DELAY)

print("Testing complete.")
