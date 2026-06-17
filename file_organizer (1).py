import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from pathlib import Path

# ─── Category definitions ──────────────────────────────────────────────────────
CATEGORIES = {
    "Picturess": {
        "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff",
                       ".tif", ".svg", ".ico", ".heic", ".raw", ".cr2", ".nef"],
        "icon": "🖼️", "color": "#FF6B9D",
    },
    "Filmha": {
        "extensions": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
                       ".m4v", ".3gp", ".mpeg", ".mpg", ".ts", ".vob"],
        "icon": "🎬", "color": "#845EF7",
    },
    "Musicss": {
        "extensions": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a",
                       ".opus", ".aiff", ".mid", ".midi"],
        "icon": "🎵", "color": "#20C997",
    },
    "Programming": {
        "extensions": [".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp",
                       ".cs", ".php", ".rb", ".go", ".rs", ".swift", ".kt", ".sh",
                       ".bash", ".json", ".xml", ".yaml", ".yml", ".sql", ".r",
                       ".dart", ".lua", ".pl", ".scala", ".h", ".hpp", ".jsx",
                       ".tsx", ".vue", ".svelte", ".ipynb", ".toml", ".ini",
                       ".env", ".gitignore", ".dockerfile"],
        "icon": "💻", "color": "#4DABF7",
    },
    "Asnad": {
        "extensions": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
                       ".txt", ".odt", ".ods", ".odp", ".rtf", ".csv", ".md",
                       ".epub", ".pages", ".numbers", ".key"],
        "icon": "📄", "color": "#FFD43B",
    },
    "Feshordeh": {
        "extensions": [".zip", ".rar", ".tar", ".gz", ".7z", ".bz2", ".xz",
                       ".tar.gz", ".tar.bz2", ".tgz", ".dmg", ".iso"],
        "icon": "📦", "color": "#F08C00",
    },
    "Barname_ha": {
        "extensions": [".exe", ".msi", ".app", ".apk", ".deb", ".rpm", ".pkg",
                       ".dmg", ".run", ".bin"],
        "icon": "⚙️", "color": "#F06595",
    },
    "Fontha": {
        "extensions": [".ttf", ".otf", ".woff", ".woff2", ".eot"],
        "icon": "🔤", "color": "#94D82D",
    },
    "Digare": {
        "extensions": [],
        "icon": "📁", "color": "#868E96",
    },
}

LABEL_NAMES = {
    "Picturess":   "عکس‌ها",
    "Filmha":      "فیلم‌ها",
    "Musicss":     "موزیک",
    "Programming": "برنامه‌نویسی",
    "Asnad":       "اسناد",
    "Feshordeh":   "فشرده‌شده",
    "Barname_ha":  "برنامه‌ها",
    "Fontha":      "فونت‌ها",
    "Digare":      "دیگر",
}

# ─── Main App ──────────────────────────────────────────────────────────────────
class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer — مرتب‌ساز فایل")
        self.root.geometry("820x680")
        self.root.configure(bg="#0F1117")
        self.root.resizable(True, True)
        self.selected_folder = tk.StringVar(value="")
        self.counts = {}
        self._build_ui()

    def _build_ui(self):
        # ── Header ────────────────────────────────────────────────────────────
        header = tk.Frame(self.root, bg="#0F1117")
        header.pack(fill="x", padx=28, pady=(22, 2))

        tk.Label(header, text="📂  مرتب‌ساز فایل",
                 font=("Helvetica", 20, "bold"),
                 bg="#0F1117", fg="#FFFFFF").pack(side="left")
        tk.Label(header, text="File Organizer",
                 font=("Helvetica", 11),
                 bg="#0F1117", fg="#3D4455").pack(side="left", padx=10, pady=5)

        # ── Dev badge (top-right) ──────────────────────────────────────────────
        badge = tk.Frame(header, bg="#1A1D26", bd=0,
                         highlightthickness=1, highlightbackground="#2D3142")
        badge.pack(side="right")

        tk.Label(badge, text="⚡", font=("Helvetica", 11),
                 bg="#1A1D26", fg="#4DABF7").pack(side="left", padx=(8,2), pady=6)
        tk.Label(badge, text="Developed by ", font=("Helvetica", 9),
                 bg="#1A1D26", fg="#555E6B").pack(side="left")
        tk.Label(badge, text="Alikay_h", font=("Helvetica", 9, "bold"),
                 bg="#1A1D26", fg="#4DABF7").pack(side="left")
        tk.Label(badge, text=" · ", font=("Helvetica", 9),
                 bg="#1A1D26", fg="#3D4455").pack(side="left")

        gh_link = tk.Label(badge, text="github.com/kayhgng",
                           font=("Helvetica", 9, "underline"),
                           bg="#1A1D26", fg="#20C997", cursor="hand2")
        gh_link.pack(side="left", padx=(0, 10))
        gh_link.bind("<Button-1>", lambda e: self._open_github())

        # ── Folder picker ────────────────────────────────────────────────────
        picker = tk.Frame(self.root, bg="#1A1D26", bd=0,
                          highlightthickness=1, highlightbackground="#2D3142")
        picker.pack(fill="x", padx=28, pady=(12, 4))

        tk.Label(picker, text="📁", font=("Helvetica", 13),
                 bg="#1A1D26", fg="#4DABF7").pack(side="left", padx=(12, 6), pady=12)

        self.folder_label = tk.Label(picker, textvariable=self.selected_folder,
                                     font=("Helvetica", 10), bg="#1A1D26",
                                     fg="#CDD5E0", anchor="w")
        self.folder_label.pack(side="left", fill="x", expand=True)

        btn_pick = tk.Button(picker, text="انتخاب فولدر",
                             font=("Helvetica", 10, "bold"),
                             bg="#4DABF7", fg="#0F1117", relief="flat", bd=0,
                             padx=16, pady=8, cursor="hand2",
                             command=self._pick_folder,
                             activebackground="#74C0FC")
        btn_pick.pack(side="right", padx=8, pady=6)

        # ── Category cards ────────────────────────────────────────────────────
        cards_outer = tk.Frame(self.root, bg="#0F1117")
        cards_outer.pack(fill="x", padx=28, pady=(14, 4))

        tk.Label(cards_outer, text="دسته‌بندی‌ها",
                 font=("Helvetica", 10), bg="#0F1117",
                 fg="#555E6B").pack(anchor="w", pady=(0, 6))

        self.cards_frame = tk.Frame(cards_outer, bg="#0F1117")
        self.cards_frame.pack(fill="x")
        self._build_cards()

        # ── START BUTTON (prominent, always visible) ──────────────────────────
        btn_frame = tk.Frame(self.root, bg="#0F1117")
        btn_frame.pack(fill="x", padx=28, pady=(10, 6))

        self.btn_start = tk.Button(
            btn_frame,
            text="▶   شروع مرتب‌سازی",
            font=("Helvetica", 13, "bold"),
            bg="#20C997", fg="#0F1117",
            relief="flat", bd=0,
            padx=0, pady=13,
            cursor="hand2",
            command=self._start_organize,
            activebackground="#38D9A9"
        )
        self.btn_start.pack(fill="x")

        # ── Log area ──────────────────────────────────────────────────────────
        log_outer = tk.Frame(self.root, bg="#0F1117")
        log_outer.pack(fill="both", expand=True, padx=28, pady=(4, 4))

        tk.Label(log_outer, text="گزارش عملیات",
                 font=("Helvetica", 10), bg="#0F1117",
                 fg="#555E6B").pack(anchor="w", pady=(0, 4))

        log_bg = tk.Frame(log_outer, bg="#1A1D26", bd=0,
                          highlightthickness=1, highlightbackground="#2D3142")
        log_bg.pack(fill="both", expand=True)

        self.log_text = tk.Text(log_bg, bg="#1A1D26", fg="#8B9EB7",
                                font=("Courier", 10), relief="flat", bd=0,
                                wrap="word", state="disabled",
                                padx=12, pady=8)
        scroll = tk.Scrollbar(log_bg, command=self.log_text.yview,
                              bg="#1A1D26", troughcolor="#1A1D26", relief="flat")
        self.log_text.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.log_text.pack(fill="both", expand=True)

        # ── Footer ────────────────────────────────────────────────────────────
        footer = tk.Frame(self.root, bg="#0F1117")
        footer.pack(fill="x", padx=28, pady=(2, 14))

        self.status_label = tk.Label(footer, text="یه فولدر انتخاب کن و دکمه رو بزن 👆",
                                     font=("Helvetica", 10),
                                     bg="#0F1117", fg="#555E6B")
        self.status_label.pack(side="left")

        tk.Label(footer, text="github.com/kayhgng",
                 font=("Helvetica", 9), bg="#0F1117",
                 fg="#2D3142").pack(side="right")

    # ── Github ─────────────────────────────────────────────────────────────────
    def _open_github(self):
        import webbrowser
        webbrowser.open("https://github.com/kayhgng")

    # ── Cards ──────────────────────────────────────────────────────────────────
    def _build_cards(self):
        for w in self.cards_frame.winfo_children():
            w.destroy()

        row_frame = None
        for i, (cat, info) in enumerate(CATEGORIES.items()):
            if i % 5 == 0:
                row_frame = tk.Frame(self.cards_frame, bg="#0F1117")
                row_frame.pack(fill="x", pady=2)

            count = self.counts.get(cat, "—")
            card = tk.Frame(row_frame, bg="#1A1D26", bd=0,
                            highlightthickness=1, highlightbackground="#2D3142",
                            width=146, height=68)
            card.pack(side="left", padx=2, pady=2)
            card.pack_propagate(False)

            top_row = tk.Frame(card, bg="#1A1D26")
            top_row.pack(fill="x", padx=8, pady=(7, 1))

            accent = tk.Frame(top_row, bg=info["color"], width=3, height=14)
            accent.pack(side="left")
            accent.pack_propagate(False)

            tk.Label(top_row, text=f'{info["icon"]} {LABEL_NAMES[cat]}',
                     font=("Helvetica", 8, "bold"), bg="#1A1D26",
                     fg="#CDD5E0").pack(side="left", padx=5)

            tk.Label(card, text=str(count),
                     font=("Helvetica", 16, "bold"),
                     bg="#1A1D26", fg=info["color"]).pack(anchor="w", padx=10)

    # ── Folder picker ──────────────────────────────────────────────────────────
    def _pick_folder(self):
        folder = filedialog.askdirectory(title="انتخاب فولدر")
        if folder:
            self.selected_folder.set(folder)
            self._preview_counts(folder)

    def _preview_counts(self, folder):
        self.counts = {cat: 0 for cat in CATEGORIES}
        try:
            for entry in os.scandir(folder):
                if entry.is_file():
                    ext = Path(entry.name).suffix.lower()
                    matched = False
                    for cat, info in CATEGORIES.items():
                        if cat == "Digare":
                            continue
                        if ext in info["extensions"]:
                            self.counts[cat] += 1
                            matched = True
                            break
                    if not matched:
                        self.counts["Digare"] += 1
        except Exception:
            pass
        self._build_cards()

    # ── Organize ───────────────────────────────────────────────────────────────
    def _start_organize(self):
        folder = self.selected_folder.get()
        if not folder:
            messagebox.showwarning("فولدر انتخاب نشده",
                                   "لطفاً ابتدا یک فولدر انتخاب کنید.")
            return
        if not os.path.isdir(folder):
            messagebox.showerror("خطا", "فولدر انتخابی معتبر نیست.")
            return

        self.btn_start.config(state="disabled", text="⏳  در حال مرتب‌سازی...")
        self._log_clear()
        self._log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        self._log(f"📂  فولدر: {folder}")
        self._log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        threading.Thread(target=self._organize_worker, args=(folder,),
                         daemon=True).start()

    def _organize_worker(self, folder):
        moved_total = 0
        errors = 0
        self.counts = {cat: 0 for cat in CATEGORIES}

        try:
            entries = [e for e in os.scandir(folder) if e.is_file()]
        except PermissionError as ex:
            self._log(f"❌  خطای دسترسی: {ex}")
            self._finish(0, 1)
            return

        for entry in entries:
            name = entry.name
            ext = Path(name).suffix.lower()
            dest_cat = "Digare"

            for cat, info in CATEGORIES.items():
                if cat == "Digare":
                    continue
                if ext in info["extensions"]:
                    dest_cat = cat
                    break

            dest_dir = os.path.join(folder, dest_cat)
            os.makedirs(dest_dir, exist_ok=True)

            dest_path = os.path.join(dest_dir, name)
            if os.path.exists(dest_path):
                base, suffix = os.path.splitext(name)
                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(dest_dir,
                                             f"{base}_{counter}{suffix}")
                    counter += 1

            try:
                shutil.move(entry.path, dest_path)
                self.counts[dest_cat] += 1
                icon = CATEGORIES[dest_cat]["icon"]
                self._log(f"  {icon}  {name}  →  {dest_cat}/")
                moved_total += 1
            except Exception as ex:
                self._log(f"  ⚠️  {name}  خطا: {ex}")
                errors += 1

        self._finish(moved_total, errors)

    def _finish(self, total, errors):
        self._log(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        self._log(f"✅  تمام!  {total} فایل جابجا شد  |  {errors} خطا")
        self._log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        self.root.after(0, self._build_cards)
        self.root.after(0, lambda: self.status_label.config(
            text=f"✅  {total} فایل مرتب شد — by Alikay_h", fg="#20C997"))
        self.root.after(0, lambda: self.btn_start.config(
            state="normal", text="▶   شروع مرتب‌سازی"))

    # ── Log ────────────────────────────────────────────────────────────────────
    def _log(self, msg):
        def _insert():
            self.log_text.config(state="normal")
            self.log_text.insert("end", msg + "\n")
            self.log_text.see("end")
            self.log_text.config(state="disabled")
        self.root.after(0, _insert)

    def _log_clear(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")


# ─── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
