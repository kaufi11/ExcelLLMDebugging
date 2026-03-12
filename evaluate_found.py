import os
import json
import re
from collections import Counter

#folder_path = "results_llm_basic_found"
#folder_path = "results_llm_basic_another_try_found"
#folder_path = "results_llm_sheet_discription_found"
folder_path = "results_llm_few_shot_found"

error_counter = Counter()
solution_counter = Counter()

total_other_points = 0
counted_files = 0
skipped_large = 0

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        try:
            data = json.loads(content)

            error_counter[data.get("errorFound", "No")] += 1
            solution_counter[data.get("solutionFound", "No")] += 1

            other_points_raw = data.get("otherPoints", 0)

            # Extract number safely
            match = re.search(r"\d+", str(other_points_raw))

            if match:
                other_points = int(match.group())

                if other_points <= 20:
                    total_other_points += other_points
                    counted_files += 1
                else:
                    skipped_large += 1
                    #print(filename)

        except json.JSONDecodeError:
            print(f"Skipping {filename}: invalid JSON")

print("Error Found counts:", dict(error_counter))
print("Solution Found counts:", dict(solution_counter))
print("Total otherPoints:", total_other_points)
print("Files counted:", counted_files)
print("Percent: ",counted_files/total_other_points)
print("Skipped because otherPoints > 10:", skipped_large)