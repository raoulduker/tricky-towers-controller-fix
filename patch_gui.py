#!/usr/bin/env python3
"""
Tricky Towers Steam Input Patch - GUI
"""

from pathlib import Path
from tkinter import Tk, Label, Button, Frame, filedialog, messagebox
from tkinter.font import Font

from patch import patch_dll, restore_dll

STEAM_APP = (
    Path.home() / "Library" / "Application Support" / "Steam" / "steamapps" / "common"
    / "Tricky Towers" / "TrickyTowers.app"
)
DLL_RELATIVE = Path("Contents") / "Resources" / "Data" / "Managed" / "Assembly-CSharp.dll"


class PatcherApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Tricky Towers Controller Patch")
        self.root.resizable(False, False)

        self.dll_path: Path | None = None
        self.setup_ui()
        self.check_steam()

    def setup_ui(self):
        self.root.configure(padx=20, pady=20)

        title_font = Font(size=14, weight="bold")
        Label(self.root, text="Tricky Towers", font=title_font).pack()
        Label(self.root, text="Steam Input Controller Patch").pack()

        Frame(self.root, height=10).pack()

        self.status = Label(self.root, text="No game selected", fg="gray")
        self.status.pack(pady=10)

        self.path_label = Label(self.root, text="", fg="gray", wraplength=300, justify="center")
        self.path_label.pack()

        Frame(self.root, height=10).pack()

        btn_frame = Frame(self.root)
        btn_frame.pack(pady=10)

        self.patch_btn = Button(btn_frame, text="Patch", width=10, command=self.do_patch, state="disabled")
        self.patch_btn.pack(side="left", padx=5)

        self.restore_btn = Button(btn_frame, text="Restore", width=10, command=self.do_restore, state="disabled")
        self.restore_btn.pack(side="left", padx=5)

        Button(self.root, text="Select Different App...", command=self.browse).pack(pady=5)

    def check_steam(self):
        steam_dll = STEAM_APP / DLL_RELATIVE
        if steam_dll.exists():
            use_steam = messagebox.askyesno(
                "Steam Version Found",
                "Found Tricky Towers in Steam library.\n\nUse this version?"
            )
            if use_steam:
                self.set_dll(steam_dll)
                return
        self.browse()

    def browse(self):
        app_path = filedialog.askopenfilename(
            title="Select TrickyTowers.app",
            filetypes=[("Application", "*.app")],
            initialdir=Path.home()
        )
        if app_path:
            dll_path = Path(app_path) / DLL_RELATIVE
            if dll_path.exists():
                self.set_dll(dll_path)
            else:
                messagebox.showerror("Error", "Assembly-CSharp.dll not found in selected app")

    def set_dll(self, path: Path):
        self.dll_path = path
        self.path_label.config(text=str(path.parent))
        self.patch_btn.config(state="normal")

        backup = path.with_suffix(".dll.bak")
        if backup.exists():
            self.status.config(text="Ready (backup exists)", fg="green")
            self.restore_btn.config(state="normal")
        else:
            self.status.config(text="Ready", fg="green")
            self.restore_btn.config(state="disabled")

    def do_patch(self):
        if not self.dll_path:
            return
        if patch_dll(self.dll_path):
            self.status.config(text="Patched!", fg="green")
            self.restore_btn.config(state="normal")
            messagebox.showinfo(
                "Success",
                "Patch applied!\n\nNow enable Steam Input:\nSteam → Tricky Towers → Properties → Controller"
            )
        else:
            self.status.config(text="Patch failed", fg="red")
            messagebox.showerror("Error", "Patch failed - strings not found or already patched")

    def do_restore(self):
        if not self.dll_path:
            return
        if restore_dll(self.dll_path):
            self.status.config(text="Restored", fg="green")
            messagebox.showinfo("Success", "Restored from backup!")
        else:
            self.status.config(text="Restore failed", fg="red")
            messagebox.showerror("Error", "No backup found")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    PatcherApp().run()
