import os
import time
import threading
from pathlib import Path
from tkinter import filedialog, messagebox, END
from tkinter.scrolledtext import ScrolledText
from tkinterdnd2 import TkinterDnD, DND_FILES
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from core.logic import (
    find_season_folders,
    prepare_rename_map_for_season,
    parse_season_episode,
)


class RenomicApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎬 Series Renamer — by Amir83Nasr")
        self.geometry("900x600")
        self.minsize(500, 400)
        self.style = ttk.Style("darkly")

        # --- State ---
        self.root_folder = None
        self.series_name = ttk.StringVar()
        self.allowed_exts = ttk.StringVar(value=".mkv,.srt,.mka,.mp4")
        self.include_season = ttk.BooleanVar(value=True)  # ✅ برای کنترل نمایش فصل

        self.setup_ui()
        self.register_drag_drop()

    # ---------------- UI setup ----------------
    def setup_ui(self):
        ttk.Label(
            self,
            text="Series Renamer",
            font=("Segoe UI", 22, "bold"),
            bootstyle="primary",
        ).pack(pady=(20, 10))

        # Folder & Name inputs
        top = ttk.Frame(self)
        top.pack(pady=10, fill=X, padx=30)

        ttk.Entry(top, textvariable=self.series_name, width=30, bootstyle="info").pack(
            side=LEFT, padx=(0, 10)
        )
        ttk.Button(
            top,
            text="Select Folder",
            command=self.choose_folder,
            bootstyle="secondary-outline",
        ).pack(side=LEFT, padx=10)

        # ✅ Checkbox برای نمایش یا حذف شماره فصل
        options_frame = ttk.Frame(self)
        options_frame.pack(pady=(0, 5))
        ttk.Checkbutton(
            options_frame,
            text="Include Season Number (e.g. S01 E01)",
            variable=self.include_season,
            bootstyle="round-toggle",
        ).pack(side=LEFT, padx=10)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        ttk.Button(
            btn_frame, text="Preview", bootstyle="primary", command=self.start_preview
        ).pack(side=LEFT, padx=8)
        ttk.Button(
            btn_frame,
            text="Rename Files",
            bootstyle="success",
            command=self.start_rename,
        ).pack(side=LEFT, padx=8)
        ttk.Button(
            btn_frame, text="Clear Log", bootstyle="secondary", command=self.clear_log
        ).pack(side=LEFT, padx=8)
        ttk.Button(
            btn_frame, text="← Back", bootstyle="danger-outline", command=self.reset_app
        ).pack(side=LEFT, padx=8)

        # Logs
        log_frame = ttk.Frame(self)
        log_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        self.preview_box = ScrolledText(
            log_frame, bg="#111827", fg="#d1d5db", font=("Consolas", 11)
        )
        self.preview_box.pack(fill=BOTH, expand=True)
        self.preview_box.insert("end", "📂 Drop a folder or select one to start...\n")

    def register_drag_drop(self):
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.on_drop)

    # ---------------- Logic ----------------

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.root_folder = Path(folder)
            self.series_name.set(self.root_folder.name)
            self.show_preview()

    def on_drop(self, event):
        folder = event.data.strip("{}")
        if os.path.isdir(folder):
            self.root_folder = Path(folder)
            self.series_name.set(self.root_folder.name)
            self.show_preview()

    def start_preview(self):
        if not self.validate_inputs():
            return
        threading.Thread(target=self.show_preview, daemon=True).start()

    def start_rename(self):
        if not self.validate_inputs():
            return
        threading.Thread(target=self.rename_all, daemon=True).start()

    def validate_inputs(self):
        if not self.root_folder:
            messagebox.showwarning("⚠️ Error", "Select a folder first.")
            return False
        if not self.series_name.get().strip():
            messagebox.showwarning("⚠️ Error", "Enter a series name.")
            return False
        return True

    def show_preview(self):
        self.preview_box.delete("1.0", END)
        self.preview_box.insert("end", f"📁 Folder: {self.root_folder}\n\n")
        allowed = [
            x.strip().lower() for x in self.allowed_exts.get().split(",") if x.strip()
        ]
        total = 0
        include_season = self.include_season.get()

        for s_idx, season in enumerate(find_season_folders(self.root_folder), start=1):
            season_num = s_idx if season != self.root_folder else 1
            pairs, preview_lines = prepare_rename_map_for_season(
                season,
                self.series_name.get().strip(),
                season_num,
                allowed,
                include_season=include_season,  # ✅ استفاده از مقدار چک‌باکس
            )

            if not preview_lines:
                continue
            self.preview_box.insert("end", f"=== {season.name} ===\n", "header")
            for _, old, new, _ in preview_lines:
                self.preview_box.insert("end", f"  {old}  →  {new}\n")
                total += 1
            self.preview_box.insert("end", "\n")
        self.preview_box.insert("end", f"\n✅ {total} files ready for rename.\n")

    def rename_all(self):
        allowed = [
            x.strip().lower() for x in self.allowed_exts.get().split(",") if x.strip()
        ]
        include_season = self.include_season.get()
        total = 0

        for s_idx, season in enumerate(find_season_folders(self.root_folder), start=1):
            season_num = s_idx if season != self.root_folder else 1
            pairs, preview_lines = prepare_rename_map_for_season(
                season,
                self.series_name.get().strip(),
                season_num,
                allowed,
                include_season=include_season,
            )
            for old, new in pairs:
                old.rename(new)
                total += 1
                time.sleep(0.02)
        messagebox.showinfo("✅ Done", f"{total} files renamed successfully.")
        self.show_preview()

    def clear_log(self):
        self.preview_box.delete("1.0", END)
        self.preview_box.insert("end", "🧹 Logs cleared.\n")

    def reset_app(self):
        self.series_name.set("")
        self.root_folder = None
        self.preview_box.delete("1.0", END)
        self.preview_box.insert(
            "end", "🔙 Back to start. Drop a folder or select one.\n"
        )
