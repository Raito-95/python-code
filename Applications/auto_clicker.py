import threading
from pynput import mouse, keyboard
from datetime import datetime
from threading import Lock

class MouseKeyboardControl:
    def __init__(self):
        self.mouse_controller = mouse.Controller()
        self.keyboard_controller = keyboard.Controller()
        self.stop_clicking = threading.Event()
        self.lock = Lock()
        self.clicking_active = False

    def print_event_time(self, event_description):
        print(f"{event_description} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def click_mouse(self):
        while not self.stop_clicking.is_set():
            with self.lock:
                self.mouse_controller.click(mouse.Button.left)
                self.print_event_time("Mouse clicked")
            self.stop_clicking.wait(0.1)

    def on_press(self, key):
        if hasattr(key, 'char') and key.char is not None:
            if key.char == 'z' and not self.clicking_active:
                self.stop_clicking.clear()
                self.clicking_active = True
                threading.Thread(target=self.click_mouse).start()
                self.keyboard_controller.press(keyboard.Key.ctrl)
                self.print_event_time("Ctrl pressed and mouse clicking started")
            elif key.char == '\x18' and self.clicking_active:
                self.stop_clicking.set()
                self.clicking_active = False
                self.keyboard_controller.release(keyboard.Key.ctrl)
                self.print_event_time("Ctrl released and mouse clicking stopped")
            elif key.char == 'q':
                self.stop_clicking.set()
                if self.clicking_active:
                    self.keyboard_controller.release(keyboard.Key.ctrl)
                self.clicking_active = False
                self.print_event_time("Exiting program")
                return False

    def on_release(self, key):
        self.print_event_time(f"Key released: {key}")

    def start_listening(self):
        try:
            with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
                listener.join()
        except Exception as e:
            self.print_event_time(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    controller = MouseKeyboardControl()
    controller.start_listening()
