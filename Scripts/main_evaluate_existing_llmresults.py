from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel

load_dotenv()

client = OpenAI()

class FeedbackEvent(BaseModel):
    faultyCell: str
    repairFormula: str
    errorFound: str
    solutionFound: str
    otherPoints: str

DIR = Path(__file__).resolve().parent
IN_DIR = DIR / "results_llm_few_shot"
IN_PROP_DIR = DIR / "EUSES/all_configs"
OUT_DIR_FOUND = DIR / "results_llm_few_shot_2"
OUT_DIR_FOUND.mkdir(exist_ok=True)

def read_txt_as_string(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return content

def compare_llm_result_with_propertie_file(llm_result, prop_file) -> str:
    propertie_file = read_txt_as_string(prop_file)

    response = client.responses.parse(
        model="gpt-5-mini",
        temperature=1,
        top_p=1,
        input=[
            {
                "role": "system",
                "content": "I asked a llm to find an error. Evaluate with the propertie File if the llm fouond the correct FAULTY_CELL and gave back the right expected value/formula. "
                "Give back only the faulty cell, the repair formula, error found (Yes,No), solution found(Yes,No) and how many other cell Errors the llm gave back as otherPoints. If there are many cells with the same other error count it as plus 1"
                "The LLM Result and Propertie File are separated by a |"
            },
            {
                "role": "user",
                "content": "LLM Result: " + llm_result + " | Propertie File: " + propertie_file
            }
        ],
        text_format=FeedbackEvent,
    )

    return response.output_parsed


if __name__ == "__main__":

    txt_files = list(IN_DIR.glob("*.txt"))

    if not txt_files:
        raise FileNotFoundError(f"No Excel files found in {IN_DIR}")

    for txt_file in txt_files:

        full_name = txt_file.stem

        if "_analysis_" in full_name:
            file_name = full_name.split("_analysis_")[0]
        else:
            file_name = full_name

        prop_file = IN_PROP_DIR / f"{file_name}.properties"

        print(f"Evaluating {txt_file.name}...")

        if not prop_file.exists():
            print(f"Property file missing for {txt_file.name}, skipping.")
            continue

        try:
            result_text = read_txt_as_string(txt_file)

            result_found_text = compare_llm_result_with_propertie_file(
                result_text, prop_file
            )

            print(f"Output {result_found_text}")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            output_found_file = OUT_DIR_FOUND / f"{file_name}_evaluation_{timestamp}.txt"
            with open(output_found_file, "w", encoding="utf-8") as f:
                f.write(result_found_text.model_dump_json(indent=2))

            print(f"Result saved to: {output_found_file}")

        except Exception as e:
            print(f"Error processing {txt_file.name}: {e}")
