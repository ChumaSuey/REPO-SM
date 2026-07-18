import tkinter as tk

import manager
import GUI

if __name__ == "__main__":
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except (AttributeError, OSError):
        pass

    manager.setup_logging()
    root = tk.Tk()
    GUI.RepoSaveManagerApp(root)
    root.mainloop()
