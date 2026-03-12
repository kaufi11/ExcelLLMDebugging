from pathlib import Path

FOLDER1 = Path("EUSES/spreadsheets/modeling/SEEDED")
FOLDER2 = Path("EUSES3/spreadsheets/modeling/SEEDED")

files1 = {f.stem: f for f in FOLDER1.glob("*.xlsx")}
files2 = {f.stem: f for f in FOLDER2.glob("*.xls")}

duplicates = set(files1.keys()) & set(files2.keys())

print(f"Found {len(duplicates)} duplicate spreadsheets")

for stem in duplicates:
    file_to_delete = files2[stem]
    print(f"Deleting {file_to_delete}")
    file_to_delete.unlink()