# 🖋️ Auto Typer Software

A powerful and customizable desktop automation tool that auto-types user-defined text with hotkey-based control. Built using Python and `tkinter`, this tool is designed to assist developers, testers, and power users in automating repetitive typing tasks.

---

## 💡 Features

- 🎯 **Custom Hotkeys**: Start, Stop, Pause, and Resume auto-typing with configurable global hotkeys.
- 📝 **Text Area**: Enter or paste any block of text to be auto-typed.
- ⚡ **Typing Speed Control**: Adjust the speed in letters per second (from 0.1 to 10).
- ⏳ **Countdown Timer**: Delay before auto-typing begins (5 seconds) for setup convenience.
- 🔠 **Special Characters Support**: Accurately types upper case, symbols, and punctuation.
- 📟 **Status Display**: Real-time feedback with countdown and current typing state.
- 🖥️ **User-Friendly GUI**: Built with `tkinter` for simplicity and accessibility.

---

## 🚀 Getting Started

### 📋 Prerequisites

Install the required Python libraries:

```bash
pip install pynput keyboard
```

▶️ How to Run
```bash
python auto_typer.py
```

🖥️ GUI Overview
Text Input Area: Paste or write the text you want to auto-type.

Typing Speed Control: Choose letters per second using the spinbox.

Hotkey Configurations:

Start: Ctrl+Alt+Q

Stop: Ctrl+Alt+W

Pause: Ctrl+Alt+P

Resume: Ctrl+Alt+E

All hotkeys can be customized dynamically.

Footer: "Made by Faizanur Rahman" credits included.

🛠️ Technologies Used
Python 3.x

tkinter – GUI toolkit

pynput – Keyboard simulation

keyboard – Global hotkey management

threading – Background task execution

