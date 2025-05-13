import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import threading
import time
from pynput import keyboard as kb
from pynput.keyboard import Key, Controller

class AutoTyper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Auto Typer Software")
        self.root.geometry("600x700")
        
        # Variables
        self.is_typing = False
        self.is_paused = False
        self.keyboard_controller = Controller()
        self.current_hotkeys = set()
        self.typing_speed = tk.DoubleVar(value=1.0)
        
        # Special characters mapping (using actual keyboard keys)
        self.special_chars = {
            '{': [Key.shift, '['],  # Left curly brace
            '}': [Key.shift, ']'],  # Right curly brace
            '(': [Key.shift, '9'],
            ')': [Key.shift, '0'],
            '!': [Key.shift, '1'],
            '@': [Key.shift, '2'],
            '#': [Key.shift, '3'],
            '$': [Key.shift, '4'],
            '%': [Key.shift, '5'],
            '^': [Key.shift, '6'],
            '&': [Key.shift, '7'],
            '*': [Key.shift, '8'],
            '_': [Key.shift, '-'],
            '+': [Key.shift, '='],
            ':': [Key.shift, ';'],
            '"': [Key.shift, "'"],
            '<': [Key.shift, ','],
            '>': [Key.shift, '.'],
            '?': [Key.shift, '/'],
            '|': [Key.shift, '\\'],
            '~': [Key.shift, '`'],
            '[': ['['],
            ']': [']'],
            '\\': ['\\'],
            '/': ['/'],
            '\'': ['\''],
            '-': ['-'],
            '=': ['='],
            '.': ['.'],
            ',': [','],
            ';': [';']
        }
        
        self.create_gui()
        
    def create_gui(self):
        # Main Frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Text Area
        text_frame = ttk.LabelFrame(main_frame, text="Enter Text to Auto-Type:", padding="5")
        text_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.text_area = tk.Text(text_frame, height=10, width=50, wrap=tk.NONE)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        x_scrollbar = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self.text_area.xview)
        self.text_area.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Typing Speed
        speed_frame = ttk.LabelFrame(main_frame, text="Typing Speed", padding="5")
        speed_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(speed_frame, text="Letters per second:").pack(side=tk.LEFT, padx=5)
        speed_spinner = ttk.Spinbox(
            speed_frame,
            from_=0.1,
            to=10.0,
            increment=0.1,
            textvariable=self.typing_speed,
            width=10
        )
        speed_spinner.pack(side=tk.LEFT, padx=5)
        
        # Control Buttons
        self.create_hotkey_button("Start", "ctrl+alt+q", self.start_typing)
        self.create_hotkey_button("Stop", "ctrl+alt+w", self.stop_typing)
        self.create_hotkey_button("Pause", "ctrl+alt+p", self.pause_typing)
        self.create_hotkey_button("Resume", "ctrl+alt+e", self.resume_typing)
        
        # Countdown Label
        self.countdown_label = ttk.Label(main_frame, text="", font=('Arial', 12, 'bold'))
        self.countdown_label.pack(pady=10)
        
        # Status Label
        self.status_label = ttk.Label(main_frame, text="Ready", font=('Arial', 10))
        self.status_label.pack(pady=5)
        
        # Footer
        footer = ttk.Label(self.root, text="Made by Faizanur Rahman", foreground="black", font=('Poppins',10,'bold'))
        footer.pack(side=tk.BOTTOM, pady=10)

    def create_hotkey_button(self, name, default_hotkey, command):
        frame = ttk.LabelFrame(self.root, text=f"{name} Configuration", padding="5")
        frame.pack(pady=5, padx=10, fill=tk.X)
        
        button = ttk.Button(frame, text=name, command=command)
        button.pack(side=tk.LEFT, padx=5)
        
        hotkey_var = tk.StringVar(value=default_hotkey)
        hotkey_entry = ttk.Entry(frame, textvariable=hotkey_var, width=15)
        hotkey_entry.pack(side=tk.LEFT, padx=5)
        
        def set_hotkey():
            try:
                old_hotkey = hotkey_var.get()
                if old_hotkey in self.current_hotkeys:
                    keyboard.remove_hotkey(old_hotkey)
                    self.current_hotkeys.remove(old_hotkey)
                
                hotkey_var.set("Press hotkey...")
                frame.update()
                
                new_hotkey = keyboard.read_hotkey()
                if new_hotkey not in self.current_hotkeys:
                    hotkey_var.set(new_hotkey)
                    keyboard.add_hotkey(new_hotkey, command)
                    self.current_hotkeys.add(new_hotkey)
                else:
                    messagebox.showerror("Error", "This hotkey is already in use!")
                    hotkey_var.set(old_hotkey)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to set hotkey: {str(e)}")
                hotkey_var.set(default_hotkey)
        
        ttk.Button(frame, text="Set Hotkey", command=set_hotkey).pack(side=tk.LEFT, padx=5)
        
        try:
            keyboard.add_hotkey(default_hotkey, command)
            self.current_hotkeys.add(default_hotkey)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set default hotkey: {str(e)}")

    def countdown(self, callback):
        for i in range(5, 0, -1):
            self.countdown_label.config(text=f"Starting in {i} seconds...")
            self.root.update()
            time.sleep(1)
        self.countdown_label.config(text="")
        callback()

    def prepare_text(self):
        text = self.text_area.get("1.0", tk.END)
        lines = text.splitlines(True)
        prepared_text = []
        
        for line in lines:
            # Convert tabs to single tab space
            line = line.replace('\t', ' ' * 4)
            line = ' ' * (len(line) - len(line.lstrip(' '))) + line.lstrip(' ')
            prepared_text.append(line)
        
        return ''.join(prepared_text)

    def type_special_char(self, char):
        try:
            if char in self.special_chars:
                keys = self.special_chars[char]
                if len(keys) == 2:  # If it needs shift
                    with self.keyboard_controller.pressed(keys[0]):
                        self.keyboard_controller.press(keys[1])
                        self.keyboard_controller.release(keys[1])
                else:  # Single key
                    self.keyboard_controller.press(keys[0])
                    self.keyboard_controller.release(keys[0])
            elif char.isupper():
                with self.keyboard_controller.pressed(Key.shift):
                    self.keyboard_controller.press(char.lower())
                    self.keyboard_controller.release(char.lower())
            else:
                self.keyboard_controller.press(char)
                self.keyboard_controller.release(char)
            
            # Small delay after each character to ensure proper typing
            time.sleep(0.01)
            
        except Exception as e:
            print(f"Error typing character '{char}': {str(e)}")

    def type_text(self):
        try:
            text = self.prepare_text()
            base_delay = 1.0 / self.typing_speed.get()
            
            for char in text:
                if not self.is_typing:
                    break
                while self.is_paused:
                    time.sleep(0.1)
                    continue
                
                if char == '\n':
                    self.keyboard_controller.press(Key.enter)
                    self.keyboard_controller.release(Key.enter)
                elif char == '\t':
                    self.keyboard_controller.press(Key.tab)
                    self.keyboard_controller.release(Key.tab)
                elif char == ' ':
                    self.keyboard_controller.press(Key.space)
                    self.keyboard_controller.release(Key.space)
                else:
                    self.type_special_char(char)
                
                time.sleep(base_delay)
            
            self.status_label.config(text="Typing finished!")
        except Exception as e:
            messagebox.showerror("Error", f"Typing error: {str(e)}")
        finally:
            self.is_typing = False
            self.is_paused = False

    def start_typing(self):
        if not self.is_typing and self.text_area.get("1.0", tk.END).strip():
            self.is_typing = True
            self.is_paused = False
            self.status_label.config(text="Preparing to type...")
            threading.Thread(target=lambda: self.countdown(
                lambda: threading.Thread(target=self.type_text, daemon=True).start()
            ), daemon=True).start()
        else:
            messagebox.showwarning("Warning", "Please enter text to type!")

    def stop_typing(self):
        self.is_typing = False
        self.is_paused = False
        self.status_label.config(text="Typing stopped!")
        self.countdown_label.config(text="")

    def pause_typing(self):
        if self.is_typing:
            self.is_paused = True
            self.status_label.config(text="Typing paused!")

    def resume_typing(self):
        if self.is_typing and self.is_paused:
            self.status_label.config(text="Preparing to resume...")
            threading.Thread(target=lambda: self.countdown(
                lambda: setattr(self, 'is_paused', False)
            ), daemon=True).start()

    def run(self):
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Application error: {str(e)}")

if __name__ == "__main__":
    auto_typer = AutoTyper()
    auto_typer.run()