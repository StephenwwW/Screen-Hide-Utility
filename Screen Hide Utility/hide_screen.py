import tkinter as tk
import ctypes
from ctypes import wintypes
from pynput import keyboard
import threading

# Windows API 結構
user32 = ctypes.windll.user32
EnumDisplayMonitors = user32.EnumDisplayMonitors
GetMonitorInfo = user32.GetMonitorInfoW

class MONITORINFO(ctypes.Structure):
    _fields_ = [
        ('cbSize', wintypes.DWORD),
        ('rcMonitor', wintypes.RECT),
        ('rcWork', wintypes.RECT),
        ('dwFlags', wintypes.DWORD),
    ]

def get_monitors():
    monitors = []

    def monitor_enum_proc(hMonitor, hdcMonitor, lprcMonitor, dwData):
        info = MONITORINFO()
        info.cbSize = ctypes.sizeof(MONITORINFO)
        GetMonitorInfo(hMonitor, ctypes.byref(info))
        r = info.rcMonitor
        monitors.append({
            'x': r.left,
            'y': r.top,
            'width': r.right - r.left,
            'height': r.bottom - r.top
        })
        return 1

    MONITORENUMPROC = ctypes.WINFUNCTYPE(
        ctypes.c_int, wintypes.HMONITOR, wintypes.HDC,
        ctypes.POINTER(wintypes.RECT), wintypes.LPARAM)

    EnumDisplayMonitors(0, 0, MONITORENUMPROC(monitor_enum_proc), 0)
    return monitors

class BlackOverlay:
    def __init__(self, master, screen_index=1):
        self.screen_index = screen_index
        self.overlay = None
        self.master = master
        self.create_overlay()

    def create_overlay(self):
        monitors = get_monitors()
        if self.screen_index >= len(monitors):
            print(f"Error: No monitor at index {self.screen_index}")
            return

        m = monitors[self.screen_index]

        self.overlay = tk.Toplevel(master=self.master)
        self.overlay.overrideredirect(True)
        self.overlay.attributes("-topmost", True)
        self.overlay.geometry(f"{m['width']}x{m['height']}+{m['x']}+{m['y']}")
        self.overlay.configure(bg='black')
        self.overlay.bind("<Escape>", lambda e: self.hide())
        self.overlay.withdraw()

    def show(self):
        if self.overlay:
            # 使用 after 確保在主線程中執行 GUI 操作
            self.master.after(0, self.overlay.deiconify)

    def hide(self):
        if self.overlay:
            # 使用 after 確保在主線程中執行 GUI 操作
            self.master.after(0, self.overlay.withdraw)

def main_gui():
    root = tk.Tk()
    root.title("Screen Control")
    root.geometry("360x120") # 稍微增加高度以容納提示文字
    root.resizable(False, False)

    label = tk.Label(root, text="Secondary Screen Control", font=("Segoe UI", 12))
    label.pack(pady=4)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=4)

    btn_style = {"font": ("Segoe UI", 10), "width": 15, "height": 2}

    overlay_controller = BlackOverlay(master=root, screen_index=1)
    overlay_controller.show()

    btn_hide = tk.Button(btn_frame, text="Hide Screen", command=overlay_controller.show, **btn_style)
    btn_hide.pack(side="left", padx=10)

    btn_show = tk.Button(btn_frame, text="Unhide Screen", command=overlay_controller.hide, **btn_style)
    btn_show.pack(side="left", padx=10)
    
    # 新增快捷鍵提示標籤
    hotkey_label = tk.Label(root, text="快捷鍵: Shift+Q (遮蔽), Shift+W (恢復)", font=("Segoe UI", 9), fg="grey")
    hotkey_label.pack(pady=2)

    # --- 快捷鍵設定 ---
    def setup_hotkeys():
        # 定義快捷鍵觸發的函式
        def on_show_hotkey():
            print("Shift+Q pressed: Showing overlay")
            overlay_controller.show()

        def on_hide_hotkey():
            print("Shift+W pressed: Hiding overlay")
            overlay_controller.hide()

        # 設定快捷鍵組合
        hotkeys = {
            '<shift>+q': on_show_hotkey,
            '<shift>+w': on_hide_hotkey
        }

        # 創建並啟動全域熱鍵監聽器
        hotkey_listener = keyboard.GlobalHotKeys(hotkeys)
        hotkey_listener.start()

    # 在背景線程中設定並監聽快捷鍵，避免阻塞 GUI
    hotkey_thread = threading.Thread(target=setup_hotkeys, daemon=True)
    hotkey_thread.start()

    root.mainloop()

if __name__ == "__main__":
    main_gui()