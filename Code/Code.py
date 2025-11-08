from pathlib import Path
import hashlib
import json
import csv
import datetime
import difflib
import re

# -------------------------------
# PATHS
# -------------------------------
folder = Path( # Folder extension for the documents put here 
    "  ")
report_folder = Path(  # Folder extension for the reports put here 
    "  ")
report_folder.mkdir(parents=True, exist_ok=True)

# -------------------------------
# Dynamic report filenames with timestamp
# -------------------------------
timestamp = datetime.datetime.now().strftime("%d_%m_%y_%H%M%S")
report_csv = report_folder / f"report_{timestamp}.csv"
report_json = report_folder / f"report_{timestamp}.json"

# -------------------------------
# FUNCTIONS
# -------------------------------


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def split_into_sentences(text):
    """Split text into sentences."""
    text = re.sub(r'([.!?])\s+(?=[A-Z“])', r'\1\n', text)
    return [s.strip() for s in text.splitlines() if s.strip()]


def get_page_and_line(index, words_per_page=500, words_per_line=20):
    word_position = index * words_per_line
    page_number = (word_position // words_per_page) + 1
    line_number = ((word_position % words_per_page) // words_per_line) + 1
    return page_number, line_number


def get_changes_with_context(old_sentences, new_sentences):
    sm = difflib.SequenceMatcher(None, old_sentences, new_sentences)
    changes = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        elif tag == 'replace':
            for k, (old, new) in enumerate(zip(old_sentences[i1:i2], new_sentences[j1:j2])):
                page, line = get_page_and_line(i1 + k)
                changes.append({
                    "page_number": page,
                    "line_number": line,
                    "description": "Word changed",
                    "lines_added_count": 1,
                    "lines_removed_count": 1,
                    "lines_added_text": new,
                    "lines_removed_text": old
                })
        elif tag == 'insert':
            for k, new in enumerate(new_sentences[j1:j2]):
                page, line = get_page_and_line(j1 + k)
                changes.append({
                    "page_number": page,
                    "line_number": line,
                    "description": "Sentence added",
                    "lines_added_count": 1,
                    "lines_removed_count": 0,
                    "lines_added_text": new,
                    "lines_removed_text": ""
                })
        elif tag == 'delete':
            for k, old in enumerate(old_sentences[i1:i2]):
                page, line = get_page_and_line(i1 + k)
                changes.append({
                    "page_number": page,
                    "line_number": line,
                    "description": "Sentence removed",
                    "lines_added_count": 0,
                    "lines_removed_count": 1,
                    "lines_added_text": "",
                    "lines_removed_text": old
                })
    return changes


# -------------------------------
# MAIN AUDIT PROCESS
# -------------------------------
results = []

chapter_prefixes = sorted(set(f.stem.rsplit('_', 1)[0] for f in folder.glob("chapter*_*.txt")),
                          key=lambda x: int(re.search(r'\d+', x).group()))

for chapter_prefix in chapter_prefixes:
    versions = sorted(folder.glob(f"{chapter_prefix}_*.txt"),
                      key=lambda f: int(f.stem.rsplit('_', 1)[1]))

    for i in range(len(versions) - 1):
        old_file = versions[i]
        new_file = versions[i + 1]

        old_text = old_file.read_text(encoding="utf-8")
        new_text = new_file.read_text(encoding="utf-8")

        old_sentences = split_into_sentences(old_text)
        new_sentences = split_into_sentences(new_text)

        old_hash = file_hash(old_file)
        new_hash = file_hash(new_file)

        # get actual modified time of new file
        modified_time = datetime.datetime.fromtimestamp(
            new_file.stat().st_mtime)
        changed_date = modified_time.strftime("%Y-%m-%d")
        changed_time = modified_time.strftime("%H:%M:%S")

        version_change = f"{old_file.stem} to {new_file.stem}"

        if old_hash != new_hash:
            changes = get_changes_with_context(old_sentences, new_sentences)
            if not changes:
                results.append({
                    "document": f"{chapter_prefix}.txt",
                    "version_change": version_change,
                    "status": "unchanged",
                    "changed_date": changed_date,
                    "changed_time": changed_time,
                    "page_number": "",
                    "line_number": "",
                    "description": "No change detected",
                    "lines_added_count": 0,
                    "lines_removed_count": 0,
                    "lines_added_text": "",
                    "lines_removed_text": ""
                })
            else:
                for c in changes:
                    results.append({
                        "document": f"{chapter_prefix}.txt",
                        "version_change": version_change,
                        "status": "changed",
                        "changed_date": changed_date,
                        "changed_time": changed_time,
                        **c
                    })
        else:
            results.append({
                "document": f"{chapter_prefix}.txt",
                "version_change": version_change,
                "status": "unchanged",
                "changed_date": changed_date,
                "changed_time": changed_time,
                "page_number": "",
                "line_number": "",
                "description": "No change detected",
                "lines_added_count": 0,
                "lines_removed_count": 0,
                "lines_added_text": "",
                "lines_removed_text": ""
            })

# Sort results numerically by chapter number
results.sort(key=lambda r: int(re.search(r'\d+', r["document"]).group()))

# -------------------------------
# WRITE REPORTS
# -------------------------------
with report_json.open("w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

with report_csv.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "document",
        "version_change",
        "status",
        "changed_date",
        "changed_time",
        "page_number",
        "line_number",
        "description",
        "lines_added_count",
        "lines_removed_count",
        "lines_added_text",
        "lines_removed_text"
    ])
    for r in results:
        writer.writerow([
            r["document"],
            r["version_change"],
            r["status"],
            r["changed_date"],
            r["changed_time"],
            r["page_number"],
            r["line_number"],
            r["description"],
            r["lines_added_count"],
            r["lines_removed_count"],
            r["lines_added_text"],
            r["lines_removed_text"]
        ])

print(f"✅ Detailed CSV report saved to: {report_csv}")
print(f"✅ JSON report saved to: {report_json}")
