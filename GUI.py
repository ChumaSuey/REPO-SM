import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import sv_ttk
import os
import pathlib
import manager
import parser

class RepoSaveManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("R.E.P.O Save Manager")
        self.root.geometry("800x600")
        
        # Configure style
        # self.style = ttk.Style()
        # self.style.theme_use('clam')
        sv_ttk.set_theme("dark")
        
        # Main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.header_label = ttk.Label(self.main_frame, text="R.E.P.O Save Manager", font=("Helvetica", 16, "bold"))
        self.header_label.pack(pady=(0, 10))
        
        # Lists Container
        self.lists_frame = ttk.Frame(self.main_frame)
        self.lists_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # --- Left Side: Steam/REPO Backups ---
        self.repo_frame = ttk.LabelFrame(self.lists_frame, text="Steam/REPO Folder (Live Saves)", padding=5)
        self.repo_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.repo_list = tk.Listbox(self.repo_frame, selectmode=tk.SINGLE, font=("Segoe UI", 10))
        self.repo_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.repo_scrollbar = ttk.Scrollbar(self.repo_frame, orient="vertical", command=self.repo_list.yview)
        self.repo_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.repo_list.config(yscrollcommand=self.repo_scrollbar.set)
        
        # --- Right Side: Local Backups ---
        self.local_frame = ttk.LabelFrame(self.lists_frame, text="Local Backups (Managed)", padding=5)
        self.local_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.local_list = tk.Listbox(self.local_frame, selectmode=tk.SINGLE, font=("Segoe UI", 10))
        self.local_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.local_scrollbar = ttk.Scrollbar(self.local_frame, orient="vertical", command=self.local_list.yview)
        self.local_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.local_list.config(yscrollcommand=self.local_scrollbar.set)
        
        # Buttons Frame
        self.buttons_frame = ttk.Frame(self.main_frame, padding="5")
        self.buttons_frame.pack(fill=tk.X, pady=10)
        
        # Buttons
        self.refresh_btn = ttk.Button(self.buttons_frame, text="Refresh Lists", command=self.refresh_lists)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        self.backup_btn = ttk.Button(self.buttons_frame, text="Backup (REPO -> Local)", command=self.backup_action)
        self.backup_btn.pack(side=tk.LEFT, padx=5)
        
        self.restore_btn = ttk.Button(self.buttons_frame, text="Restore (Local -> REPO)", command=self.restore_action)
        self.restore_btn.pack(side=tk.LEFT, padx=5)
        
        self.change_local_btn = ttk.Button(self.buttons_frame, text="Change Local", command=self.settings_action)
        self.change_local_btn.pack(side=tk.RIGHT, padx=5)
        
        self.change_local_label = ttk.Label(self.buttons_frame, text="Change local folder ->")
        self.change_local_label.pack(side=tk.RIGHT, padx=5)
        
        # Initial Load
        self.refresh_lists()

    def refresh_lists(self):
        # Clear lists
        self.repo_list.delete(0, tk.END)
        self.local_list.delete(0, tk.END)
        
        # Load REPO (Steam) Folder contents
        repo_path = parser.get_save_path()
        if repo_path and repo_path.exists():
            try:
                # List all items in the save folder (files and folders)
                # Usually saves are folders or files. Let's list everything for now.
                for item in repo_path.iterdir():
                    self.repo_list.insert(tk.END, item.name)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read REPO folder: {e}")
        else:
            self.repo_list.insert(tk.END, "[REPO Folder Not Found]")
            
        # Load Local Backups
        local_path = manager.get_local_backup_path()
        if local_path.exists():
            try:
                for item in local_path.iterdir():
                    if item.is_dir(): # Only list directories as backups
                        self.local_list.insert(tk.END, item.name)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read Local folder: {e}")

    def backup_action(self):
        # Ask for backup name
        backup_name = simpledialog.askstring("Backup", "Enter name for the new backup:")
        if backup_name:
            if manager.total_backup(backup_name):
                messagebox.showinfo("Success", f"Backup '{backup_name}' created successfully.")
                self.refresh_lists()
            else:
                messagebox.showerror("Error", "Backup failed. Check console/logs for details.")

    def restore_action(self):
        # Get selected item from Local list
        selection = self.local_list.curselection()
        if not selection:
            messagebox.showwarning("Selection", "Please select a backup from the Local Backups list to restore.")
            return
            
        backup_name = self.local_list.get(selection[0])
        
        # Confirm
        if messagebox.askyesno("Confirm Restore", f"Are you sure you want to restore '{backup_name}'?\nThis will OVERWRITE the current live saves."):
            if manager.restore_saves(backup_name):
                messagebox.showinfo("Success", f"Restored '{backup_name}' successfully.")
                self.refresh_lists()
            else:
                messagebox.showerror("Error", "Restore failed. Check console/logs for details.")

    def settings_action(self):
        current_path = manager.get_local_backup_path()
        new_path = filedialog.askdirectory(initialdir=current_path, title="Select Local Backup Folder")
        if new_path:
            manager.set_local_backup_path(new_path)
            messagebox.showinfo("Settings", f"Local backup path updated to:\n{new_path}")
            self.refresh_lists()

if __name__ == "__main__":
    root = tk.Tk()
    app = RepoSaveManagerApp(root)
    root.mainloop()
