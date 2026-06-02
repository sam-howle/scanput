import time
from scanput import (
    key_down, key_up,
    left_down, left_up,
    right_down, right_up,
    get_cursor_position, set_cursor_position,
)

HOLD = 0.08
BETWEEN = 0.12

print("Focus a text field. Starting in 5 seconds...")
time.sleep(5)

alphabet = "abcdefghijklmnopqrstuvwxyz"
specials = ["space", "enter", "!", "@", "#", "$", "%", "tab", "1", "2", "3"]

print ("typing the alphabet.")
for char in alphabet:
    key_down(char)
    time.sleep(HOLD)
    key_up(char)
    time.sleep(BETWEEN)

key_down("shift")
print("Typing the alphabet while holding shift.")
for char in alphabet:
    key_down(char)
    time.sleep(HOLD)
    key_up(char)
    time.sleep(BETWEEN)
key_up("shift")
time.sleep(BETWEEN)

print("Typing special characters.")
for key in specials:
    key_down(key)
    time.sleep(HOLD)
    key_up(key)
    time.sleep(BETWEEN)

x, y = get_cursor_position()
print(f"Current mouse position: ({x}, {y})")

dest_x, dest_y = x + 300, y - 150
print(f"Teleporting mouse to ({dest_x}, {dest_y})")
set_cursor_position(dest_x, dest_y)
time.sleep(BETWEEN)

print("Left click.")
left_down()
time.sleep(HOLD)
left_up()
time.sleep(BETWEEN)

print("Right click.")
right_down()
time.sleep(HOLD)
right_up()
time.sleep(BETWEEN)

print("Testing complete.")
