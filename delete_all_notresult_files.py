from pathlib import Path

# Folders
IN_DIR = Path("EUSES2/spreadsheets/modeling/SEEDED")
OUT_DIR_FOUND = Path("results_llm_sheet_discription_found")
OUT_DIR_FOUND2 = Path("results_llm_basic_found")

# Gather all result filenames without timestamps/extensions
result_files_stem = {f.stem.split("_analysis_")[0] for f in OUT_DIR_FOUND.glob("*.txt")}
result_files_stem2 = {f.stem.split("_analysis_")[0] for f in OUT_DIR_FOUND2.glob("*.txt")}

# Loop through all Excel files in the input folder
for excel_file in IN_DIR.glob("*.xlsx"):
    if excel_file.stem in result_files_stem2:
        print(f"Deleting {excel_file.name} because no result file exists.")