import json
from pathlib import Path
from collections import defaultdict
from collections import Counter

folders = [
    "../LLM_Result_Files/results_llm_basic_2",
    "../LLM_Result_Files/results_llm_sheet_discription_2",
    "../LLM_Result_Files/results_llm_few_shot_2",
    "../LLM_Result_Files/results_llm_basic_one_error_2"
]

error_dict = defaultdict(dict)
solution_dict = defaultdict(dict)

for folder_path in folders:
    folder = Path(folder_path)
    if not folder.exists():
        print(f"Folder not found: {folder}")
        continue

    for file_path in folder.glob("*.txt"):
        stem = file_path.stem.split("_evaluation_")[0]

        try:
            content = file_path.read_text(encoding="utf-8")
            data = json.loads(content)

            error_val = data.get("errorFound", "No").strip().lower()
            solution_val = data.get("solutionFound", "No").strip().lower()

            error_dict[stem][folder_path] = error_val
            solution_dict[stem][folder_path] = solution_val

        except json.JSONDecodeError:
            print(f"Skipping {file_path.name}: invalid JSON")

error_all_no_files = [
    stem for stem, statuses in error_dict.items()
    if len(statuses) == len(folders) and all(v == "no" for v in statuses.values())
]

solution_all_no_files = [
    stem for stem, statuses in solution_dict.items()
    if len(statuses) == len(folders) and all(v == "no" for v in statuses.values())
]

# ✅ Print results
print("Files with errorFound=No in ALL 3 folders:", len(error_all_no_files))
print("Files with solutionFound=No in ALL 3 folders:", len(solution_all_no_files))

print("\nFiles where errorFound=No in ALL 3 folders:")
for f in error_all_no_files:
    print(f)

print("\nFiles where solutionFound=No in ALL 3 folders:")
for f in solution_all_no_files:
    print(f)

prefixes = [stem[:10] for stem in solution_all_no_files]
prefix_counts = Counter(prefixes)

duplicates = {k: v for k, v in prefix_counts.items() if v > 1}

print("\n--- Duplicate prefixes (first 10 characters) among SOLUTION-ALL-NO files ---")
print("Number of duplicated prefixes:", len(duplicates))

for prefix, count in duplicates.items():
    print(f"{prefix} -> {count} files")