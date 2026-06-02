# scanput
Lightweight Windows Keyboard &amp; Mouse input library using hardware scan codes.

Unlike existing libraries like `pyautogui` that use virtual key presses, `scanput` uses hardware scan codes making them indistinguishable* from physical hardware keypresses to most applications.

While the `AutoHotKey` Python library does offer hardware scan code inputs, the library requires having `AutoHotKey` installed, pointing to the file path to the .exe, and then spawns a new `AutoHotKey.exe` subprocess *every time* you perform any action. 

`scanput` is designed to be lightweight and has zero third-party required dependencies.

## Usage
A more detailed guide can be found in `demo.py`.

### Key Presses
All button pressing & mouse clicking functions require both a press and a release. Pressing a key without releasing it will result in the key being held down indefinately. 
It is recommended to add a short timing delay between presses. For example:
```python
HOLD = 0.08
key_down("k")
time.sleep(HOLD)
key_up("k")
```
The above example presses the `k` key and holds it for 0.08 seconds before releasing.

For a list of key aliases, run the following line:
```python
print(list(KEY_ALIASES.keys()))
```
Additionally, `key_down()` and `key_up()` accept either a key name string or a raw Windows Virtual Key code as an integer, allowing direct specification of any VK code not covered by the named aliases. The Windows Virtual Key code is converted to a hardware scan code before input is performed. A full list of Windows VK integers can be found at the following link: 

[https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes](https://learn.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes)

### Mouse Clicks
Similarly, mouse clicks also take a press & release approach:
```python
HOLD = 0.08
print("Left click.")
left_down()
time.sleep(HOLD)
left_up()

print("Right click.")
right_down()
time.sleep(HOLD)
right_up()
```

### Mouse Movement
There are only two mouse movement functions: `get_cursor_position()` and `set_cursor_position(x,y)`. The following snippet obtains the current mouse position, and offsets it by an `(x,y)` value of `(300,150)` pixels:
```python
x, y = get_cursor_position()
print(f"Current mouse position: ({x}, {y})")

dest_x, dest_y = x + 300, y - 150
print(f"Teleporting mouse to ({dest_x}, {dest_y})")
set_cursor_position(dest_x, dest_y)
```
Please note that the Y axis for monitor pixel coordinates starts with `0` being the top of the screen, rather than the bottom. That means the coordinate `(0,0)` is the top-left monitor pixel. While unintuitive, it is consistent with how monitor pixel coordinates have always worked starting with early CRTs. 

### Toggle Key States
The `get_toggle_key_state()` function can be used to let your script know the current state of the `capslock`, `numlock`, and `scrolllock` keys:
```python
get_toggle_key_state("capslock")   # 1 or 0
get_toggle_key_state("numlock")    # 1 or 0
get_toggle_key_state("scrolllock") # 1 or 0
get_toggle_key_state(0x14)         # same as capslock by VK int
```
Be aware that this function is only meaningful for toggle keys. Passing modifier keys like `shift` or `alt` will always return `0`.

And that's really all there is to it. 

You can press buttons. And you can release buttons. You can move the mouse. And you can find out where the mouse is. You can click mice. And you can release mouse clicks. 
The world is your oyster. Crack it open and slurp out its innards.
