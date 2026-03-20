import os
import json
from pathlib import Path
from collections import defaultdict

folders = [
    "results_llm_basic_found",
    "results_llm_sheet_discription_found",
    "results_llm_few_shot_found"
]

error_dict = defaultdict(list)
solution_dict = defaultdict(list)

for folder_path in folders:
    folder = Path(folder_path)
    if not folder.exists():
        print(f"Folder not found: {folder}")
        continue

    for file_path in folder.glob("*.txt"):
        stem = file_path.stem.split("_analysis_")[0]
        try:
            content = file_path.read_text(encoding="utf-8")
            data = json.loads(content)

            error_dict[stem].append(data.get("errorFound", "No"))
            solution_dict[stem].append(data.get("solutionFound", "No"))

        except json.JSONDecodeError:
            print(f"Skipping {file_path.name}: invalid JSON")

error_all_no = sum(1 for statuses in error_dict.values() if all(s == "No" for s in statuses))
solution_all_no = sum(1 for statuses in solution_dict.values() if all(s == "No" for s in statuses))

print("Files with errorFound=No in ALL folders:", error_all_no)
print("Files with solutionFound=No in ALL folders:", solution_all_no)