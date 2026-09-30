# ⏱️ Timer & Stopwatch (Tkinter)

A minimal, elegant **Timer + Stopwatch desktop application** built with **Python & Tkinter**, featuring a smooth animated circular progress ring.

Designed for Linux-first workflows, simple enough to understand, solid enough to use daily.

---

## ✨ Features

### 🕒 Timer Mode
- Set time using: `SS`, `MM:SS`, or `HH:MM:SS`
- Circular countdown animation with smooth arc transition
- Sound notification on completion (uses `paplay` if available)
- Automatic stop at zero

### ⏱️ Stopwatch Mode
- Start / Pause / Reset controls
- Millisecond precision display
- Lap recording with a scrollable lap list

### 🖥️ UI & Behavior
- Clean circular clock design, opens centered on screen
- Fully resizable (minimize / maximize supported)
- No external GUI frameworks required

---

## 📦 Requirements & Environment Setup

- Python **3.8+**
- Tkinter (usually bundled with Python)
- Linux (recommended, optional `paplay` for sound alerts)

**Tkinter is required.** If your Linux distribution does not include it by default:
- Ubuntu/Debian: `sudo apt-get install python3-tk`
- Arch Linux / BlackArch: `sudo pacman -S tk`

---

## 🚀 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Zoom0099/StopWatch.git
   cd StopWatch
