import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from typing import Optional

import sv_ttk

import manager
import parser


class _SettingsDialog(tk.Toplevel):
    def __init__(self, parent: tk.Tk) -> None:
        super().__init__(parent)
        self.title("Settings")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        sv_ttk.set_theme("dark")

        dw, dh = 420, 160
        px = parent.winfo_rootx() + (parent.winfo_width() - dw) // 2
        py = parent.winfo_rooty() + (parent.winfo_height() - dh) // 2
        self.geometry(f"{dw}x{dh}+{px}+{py}")

        frame = ttk.Frame(self, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Backup Suffix:").grid(
            row=0, column=0, sticky=tk.W, pady=(0, 8)
        )
        self.suffix_var = tk.StringVar(value=manager.get_backup_suffix())
        self.suffix_entry = ttk.Entry(frame, textvariable=self.suffix_var, width=20)
        self.suffix_entry.grid(row=0, column=1, sticky=tk.EW, padx=(10, 0), pady=(0, 8))

        ttk.Label(frame, text="Local Folder:").grid(
            row=1, column=0, sticky=tk.W, pady=(0, 8)
        )
        self.folder_var = tk.StringVar(value=str(manager.get_local_backup_path()))
        self.folder_entry = ttk.Entry(frame, textvariable=self.folder_var, width=30)
        self.folder_entry.grid(row=1, column=1, sticky=tk.EW, padx=(10, 0), pady=(0, 8))

        browse_btn = ttk.Button(frame, text="Browse...", command=self._browse)
        browse_btn.grid(row=1, column=2, padx=(5, 0), pady=(0, 8))

        frame.columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=3, sticky=tk.E, pady=(5, 0))

        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(
            side=tk.RIGHT, padx=(5, 0)
        )
        ttk.Button(btn_frame, text="Save", command=self._save).pack(side=tk.RIGHT)

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.wait_window()

    def _browse(self) -> None:
        chosen = filedialog.askdirectory(
            initialdir=self.folder_var.get(),
            title="Select Local Backup Folder",
            parent=self,
        )
        if chosen:
            self.folder_var.set(chosen)

    def _save(self) -> None:
        manager.set_backup_suffix(self.suffix_var.get() or "_backup")
        manager.set_local_backup_path(self.folder_var.get())
        self.destroy()


class RepoSaveManagerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self._recycle_mode = False
        self.root.title("R.E.P.O Save Manager")
        self.root.resizable(True, True)
        w, h = 1024, 600
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

        sv_ttk.set_theme("dark")

        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.header_label = ttk.Label(
            self.main_frame, text="R.E.P.O Save Manager", font=("Helvetica", 16, "bold")
        )
        self.header_label.pack(pady=(0, 10))

        self.lists_frame = ttk.Frame(self.main_frame)
        self.lists_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.repo_frame = ttk.LabelFrame(
            self.lists_frame, text="Steam/REPO Folder (Live Saves)", padding=5
        )
        self.repo_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.repo_list = tk.Listbox(
            self.repo_frame, selectmode=tk.SINGLE, font=("Segoe UI", 10)
        )
        self.repo_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.repo_scrollbar = ttk.Scrollbar(
            self.repo_frame, orient="vertical", command=self.repo_list.yview
        )
        self.repo_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.repo_list.config(yscrollcommand=self.repo_scrollbar.set)

        self.local_frame = ttk.LabelFrame(
            self.lists_frame, text="Local Backups (Managed)", padding=5
        )
        self.local_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.local_list = tk.Listbox(
            self.local_frame, selectmode=tk.SINGLE, font=("Segoe UI", 10)
        )
        self.local_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.local_scrollbar = ttk.Scrollbar(
            self.local_frame, orient="vertical", command=self.local_list.yview
        )
        self.local_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.local_list.config(yscrollcommand=self.local_scrollbar.set)

        self._build_buttons()
        self._build_all_menus()
        self._setup_key_bindings()
        self.refresh_lists()

    def _build_buttons(self) -> None:
        self.buttons_frame = ttk.Frame(self.main_frame, padding="5")
        self.buttons_frame.pack(fill=tk.X, pady=10)

        self.refresh_btn = ttk.Button(
            self.buttons_frame, text="Refresh", command=self.refresh_lists
        )
        self.refresh_btn.pack(side=tk.LEFT, padx=(0, 12))

        ttk.Separator(self.buttons_frame, orient="vertical").pack(
            side=tk.LEFT, fill=tk.Y, padx=10
        )

        self.backup_btn = ttk.Button(
            self.buttons_frame, text="Backup", command=self.backup_action
        )
        self.backup_btn.pack(side=tk.LEFT, padx=3)

        self.restore_btn = ttk.Button(
            self.buttons_frame, text="Restore", command=self._on_restore
        )
        self.restore_btn.pack(side=tk.LEFT, padx=3)

        self.toggle_btn = ttk.Button(
            self.buttons_frame, text="Toggle", command=self.toggle_state_action
        )
        self.toggle_btn.pack(side=tk.LEFT, padx=(3, 12))

        ttk.Separator(self.buttons_frame, orient="vertical").pack(
            side=tk.LEFT, fill=tk.Y, padx=10
        )

        self.rename_btn = ttk.Button(
            self.buttons_frame, text="Rename", command=self.rename_action
        )
        self.rename_btn.pack(side=tk.LEFT, padx=3)

        self.delete_btn = ttk.Button(
            self.buttons_frame, text="Delete", command=self._on_delete
        )
        self.delete_btn.pack(side=tk.LEFT, padx=3)

        self.recycle_btn = ttk.Button(
            self.buttons_frame,
            text="\U0001f5d1  Recycle Bin",
            command=self._toggle_recycle_view,
        )
        self.recycle_btn.pack(side=tk.LEFT, padx=(3, 12))

        ttk.Separator(self.buttons_frame, orient="vertical").pack(
            side=tk.LEFT, fill=tk.Y, padx=10
        )

        self.settings_btn = ttk.Button(
            self.buttons_frame,
            text="\u2699 Settings",
            command=self.open_settings,
        )
        self.settings_btn.pack(side=tk.RIGHT, padx=3)

        self.open_repo_btn = ttk.Button(
            self.buttons_frame,
            text="Open Saves",
            command=self.open_repo_folder,
        )
        self.open_repo_btn.pack(side=tk.RIGHT, padx=3)

        self.open_local_btn = ttk.Button(
            self.buttons_frame,
            text="Open Local",
            command=self.open_local_folder,
        )
        self.open_local_btn.pack(side=tk.RIGHT, padx=(3, 12))

        self.recycle_buttons = [
            self.backup_btn,
            self.restore_btn,
            self.toggle_btn,
            self.rename_btn,
        ]

        self.action_buttons = self.recycle_buttons + [
            self.refresh_btn,
            self.delete_btn,
            self.recycle_btn,
            self.open_local_btn,
            self.open_repo_btn,
            self.settings_btn,
        ]

    def _build_all_menus(self) -> None:
        self.local_menu_normal = tk.Menu(self.root, tearoff=0)
        self.local_menu_normal.add_command(label="Restore", command=self.restore_saves_action)
        self.local_menu_normal.add_command(
            label="Toggle State", command=self.toggle_state_action
        )
        self.local_menu_normal.add_command(label="Rename...", command=self.rename_action)
        self.local_menu_normal.add_separator()
        self.local_menu_normal.add_command(label="Delete", command=self.delete_backup_action)

        self.local_menu_recycle = tk.Menu(self.root, tearoff=0)
        self.local_menu_recycle.add_command(
            label="Restore", command=self.restore_from_recycle_action
        )
        self.local_menu_recycle.add_command(
            label="Delete Forever", command=self.delete_forever_action
        )

        self.repo_menu = tk.Menu(self.root, tearoff=0)
        self.repo_menu.add_command(
            label="Open in Explorer", command=self.open_repo_folder
        )

        self.local_list.bind("<Button-3>", self._show_local_menu)
        self.repo_list.bind("<Button-3>", self._show_repo_menu)

    def _show_local_menu(self, event: tk.Event) -> None:
        try:
            idx = self.local_list.nearest(event.y)
            self.local_list.selection_clear(0, tk.END)
            self.local_list.selection_set(idx)
            menu = self.local_menu_recycle if self._recycle_mode else self.local_menu_normal
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            pass

    def _show_repo_menu(self, event: tk.Event) -> None:
        self.repo_menu.tk_popup(event.x_root, event.y_root)

    def _setup_key_bindings(self) -> None:
        self.root.bind("<F5>", lambda _e: self.refresh_lists())
        self.root.bind("<Delete>", lambda _e: self._on_delete())

    def _toggle_recycle_view(self) -> None:
        self._recycle_mode = not self._recycle_mode
        if self._recycle_mode:
            self.recycle_btn.config(text="\u25c0  Back")
            self.delete_btn.config(text="Delete Forever")
        else:
            self.recycle_btn.config(text="\U0001f5d1  Recycle Bin")
            self.delete_btn.config(text="Delete")
        self._apply_mode_state()
        self.refresh_lists()

    def _apply_mode_state(self) -> None:
        state = tk.DISABLED if self._recycle_mode else tk.NORMAL
        for btn in self.recycle_buttons:
            btn.config(state=state)

    def refresh_lists(self) -> None:
        self.repo_list.delete(0, tk.END)
        self.local_list.delete(0, tk.END)

        repo_path = parser.get_save_path()
        if repo_path and repo_path.exists():
            try:
                for item in repo_path.iterdir():
                    self.repo_list.insert(tk.END, item.name)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read REPO folder: {e}")
        else:
            self.repo_list.insert(tk.END, "[REPO Folder Not Found]")

        if self._recycle_mode:
            local_path = manager.get_recycle_path()
            frame_label = "Recycle Bin"
        else:
            local_path = manager.get_local_backup_path()
            frame_label = "Local Backups (Managed)"

        self.local_frame.config(text=frame_label)

        if local_path.exists():
            try:
                for item in local_path.iterdir():
                    if item.is_dir() and (
                        self._recycle_mode or item.name != manager.RECYCLE_BIN_FOLDER
                    ):
                        self.local_list.insert(tk.END, item.name)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read folder: {e}")

    def _get_selected_local(self) -> Optional[str]:
        selection = self.local_list.curselection()
        if not selection:
            messagebox.showwarning(
                "Selection",
                "Please select a backup from the list.",
            )
            return None
        return self.local_list.get(selection[0])

    def _set_buttons_state(self, state: str) -> None:
        for btn in self.action_buttons:
            btn.config(state=state)
        if self._recycle_mode:
            self._apply_mode_state()

    def _run_async(self, func, success_msg: str, error_prefix: str) -> None:
        self._set_buttons_state(tk.DISABLED)

        def worker() -> None:
            try:
                ok = func()
                self.root.after(
                    0, lambda: self._async_done(ok, success_msg, error_prefix)
                )
            except Exception as exc:
                self.root.after(0, lambda: self._async_error(str(exc), error_prefix))

        threading.Thread(target=worker, daemon=True).start()

    def _async_done(self, ok: bool, success_msg: str, error_prefix: str) -> None:
        self._set_buttons_state(tk.NORMAL)
        if self._recycle_mode:
            self._apply_mode_state()
        self.refresh_lists()
        if ok:
            messagebox.showinfo("Success", success_msg)
        else:
            messagebox.showerror("Error", f"{error_prefix}. Check logs for details.")

    def _async_error(self, exc_msg: str, error_prefix: str) -> None:
        self._set_buttons_state(tk.NORMAL)
        if self._recycle_mode:
            self._apply_mode_state()
        messagebox.showerror("Error", f"{error_prefix}: {exc_msg}")

    def backup_action(self) -> None:
        backup_name = simpledialog.askstring(
            "Backup", "Enter name for the new backup:"
        )
        if backup_name:
            self._run_async(
                lambda: manager.total_backup(backup_name),
                f"Backup '{backup_name}' created successfully.",
                "Backup failed",
            )

    def restore_saves_action(self) -> None:
        backup_name = self._get_selected_local()
        if not backup_name:
            return

        if not messagebox.askyesno(
            "Confirm Restore",
            f"Are you sure you want to restore '{backup_name}'?\n"
            "This will OVERWRITE the current live saves.",
        ):
            return

        self._run_async(
            lambda: manager.restore_saves(backup_name),
            f"Restored '{backup_name}' successfully.",
            "Restore failed",
        )

    def restore_from_recycle_action(self) -> None:
        backup_name = self._get_selected_local()
        if not backup_name:
            return

        if manager.restore_from_recycle(backup_name):
            messagebox.showinfo(
                "Restored", f"'{backup_name}' restored from Recycle Bin."
            )
            self.refresh_lists()
        else:
            messagebox.showerror(
                "Error", "Restore failed. Check logs for details."
            )

    def _on_restore(self) -> None:
        if self._recycle_mode:
            self.restore_from_recycle_action()
        else:
            self.restore_saves_action()

    def delete_backup_action(self) -> None:
        backup_name = self._get_selected_local()
        if not backup_name:
            return

        if not messagebox.askyesno(
            "Confirm Delete",
            f"Move '{backup_name}' to Recycle Bin?\n"
            "You can restore it later from the Recycle Bin.",
        ):
            return

        self._run_async(
            lambda: manager.move_to_recycle(backup_name),
            f"'{backup_name}' moved to Recycle Bin.",
            "Delete failed",
        )

    def delete_forever_action(self) -> None:
        backup_name = self._get_selected_local()
        if not backup_name:
            return

        if not messagebox.askyesno(
            "Confirm Permanent Delete",
            f"Permanently delete '{backup_name}'?\n"
            "This action CANNOT be undone.",
        ):
            return

        self._run_async(
            lambda: manager.permanently_delete(backup_name),
            f"'{backup_name}' permanently deleted.",
            "Delete failed",
        )

    def _on_delete(self) -> None:
        if self._recycle_mode:
            self.delete_forever_action()
        else:
            self.delete_backup_action()

    def toggle_state_action(self) -> None:
        backup_name = self._get_selected_local()
        if not backup_name:
            return

        backup_path = manager.get_local_backup_path() / backup_name
        suffix = manager.get_backup_suffix()
        currently_disabled = backup_name.endswith(suffix)
        new_path = manager.set_backup_state(backup_path, active=currently_disabled)

        if new_path.name != backup_name:
            self.refresh_lists()
        else:
            messagebox.showwarning(
                "No Change",
                "State was not changed (maybe it was already in the desired state?).",
            )

    def rename_action(self) -> None:
        old_name = self._get_selected_local()
        if not old_name:
            return

        new_name = simpledialog.askstring(
            "Rename Backup",
            "Enter new name:",
            initialvalue=old_name,
        )
        if not new_name or new_name == old_name:
            return

        if manager.rename_backup(old_name, new_name):
            messagebox.showinfo("Renamed", f"'{old_name}' renamed to '{new_name}'.")
            self.refresh_lists()
        else:
            messagebox.showerror(
                "Error",
                "Rename failed. Check logs for details.",
            )

    def open_repo_folder(self) -> None:
        repo_path = parser.get_save_path()
        if repo_path and repo_path.exists():
            os.startfile(str(repo_path))
        else:
            messagebox.showwarning("Not Found", "REPO save folder not found.")

    def open_local_folder(self) -> None:
        if self._recycle_mode:
            os.startfile(str(manager.get_recycle_path()))
        else:
            os.startfile(str(manager.get_local_backup_path()))

    def open_settings(self) -> None:
        _SettingsDialog(self.root)
        self.refresh_lists()
