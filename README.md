## 🎮  Playhub - Gamestore - Project Background

***Q1,Q2‑Review: Game Shop Sales Report Jan-Jun 2025***



---

The Excel file used to inspect clean and analyse the data is [here](Dataset/unclean_data.csv).  

To view data cleaning process using PANDAS click [here.](Dataset/README.md)


<img width="989" height="590" alt="barchart" src="https://github.com/user-attachments/assets/2121cc4f-9d71-4218-8950-2fcefedd8b5d" />  

---

### ⚙️ Key Features

- 🔍 **Version Comparison:** Handles multiple versions (`_0`, `_1`, `_2`, etc.) automatically.
- 🧠 **Smart Diffing:** Uses sentence-level comparison for precise reporting.
- 📘 **Change Classification:** Detects “Word changed”, “Sentence added”, or “Sentence removed”.
- 📄 **Detailed Reports:** Includes page numbers, line numbers, and text of added/removed lines.
- 🕒 **Timestamped Reports:** Reports saved as `report_07_11_25_150315.csv` for easy versioning.
- 🧹 **Report Cleanup:** Keeps your folder tidy by retaining the last 5 reports.

---

### 🧰 Libraries Used

| Library | Purpose |
| -------- | -------- |
| `pathlib` | File and folder management |
| `hashlib` | Detect file changes via SHA256 hashes |
| `difflib` | Sentence-level comparison between versions |
| `csv`, `json` | Export reports in readable formats |
| `datetime` | Timestamps and versioning |
| `re` | Sentence parsing and text processing |

---

### 🧾 Example Output (Excerpt)

| document     | status  | changed_on               | page_number | line_number | description     | lines_added_count | lines_removed_count | lines_added_text                              | lines_removed_text                          |
| ------------ | ------- | ------------------------ | ----------- | ----------- | --------------- | ---------------- | ----------------- | --------------------------------------------- | ------------------------------------------- |
| chapter1.txt | changed | 2025-11-07T15:08:34Z     | 1           | 2           | Word changed    | 1                | 1                 | The doors...High Council’s seal             | The doors...Council’s sigil                 |
| chapter2.txt | changed | 2025-11-07T15:08:34Z     | 1           | 7           | Sentence added  | 1                | 0                 | A faint hum of magic lingered...            |                                             |

---

### 🧭 Folder Structure

