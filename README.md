# 🎬 Series Renamer — by Amir Hossein

A modern, responsive Python application to **preview and rename TV series or movie files** based on a structured naming convention (`Serial Name S01 E01`). Supports **drag & drop**, multi-format files, and interactive preview before renaming.

---

## 🛠 Features

- Drag & drop any folder containing series files.
- Preview file renaming without changing files (dry-run).
- Rename video and subtitle files consistently.
- Automatically handles multiple seasons.
- Customizable allowed file extensions (`.mkv, .mp4, .srt`, etc.).
- Responsive UI using **ttkbootstrap** with dark mode theme.
- Clean log view of all actions.

---

## 💻 Installation

### 1. Clone the repository:

```bash
git clone https://github.com/Amir83Nasr/SeriesRenamer.git
cd SeriesRenamer
```

### 2. Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

**Dependencies:**

- `ttkbootstrap`
- `tkinterdnd2` (for drag & drop support)

---

## 🚀 Usage

```bash
python app.py
```

**Steps:**

1. Drag & drop a folder containing your series files **or** click "Select Folder".
2. Enter the **series name**.
3. Press **Preview** to see the proposed renaming.
4. Press **Rename Files** to apply changes.
5. Clear log with the **Clear Log** button if needed.

---

## ⚙️ File Naming Convention

All files will be renamed in the following format:

```
Serial Name S01 E01.ext
```

- `S01` → Season number, 2 digits
- `E01` → Episode number, 2 digits
- `.ext` → Original file extension

---

## 📝 Screenshots

_(Add screenshots here of the app interface, drag & drop, and preview log)_

---

## 💡 Notes

- If season folders are missing, all files in the root folder will be renamed sequentially.
- The app **does not create new folders**—it only renames files based on the series name you provide.

---

## 🛡 License

This project is **MIT Licensed** — see [LICENSE](LICENSE) for details.

---

## 🤝 Contributions

Contributions are welcome! Feel free to open issues or submit pull requests for improvements.

---

## 📞 Contact

**Author:** Amir Hossein
**GitHub:** [Amir83Nasr](https://github.com/Amir83Nasr)
