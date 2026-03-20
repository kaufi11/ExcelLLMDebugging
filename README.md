# ExcelLLMDebugging
All script and output Files to my research about "Debugging of Excel Spreadsheets using Large
Language Models". 

## Folders
- EUSES
  - The configuration files, the faulty spreadsheets and the correct spreadsheets
  - .Property files are in all_configs and in configuration_files because of the evaluate_existing_llmresults script
- LLM_Raw_Output_Files
  - The debug-feedback form the llm devided into the different approaches
- LLM_Result_Files
  - The evaluation form the LLM_Raw_Output_Files
- Scripts
  - main_ files for the different approaches (API Key needed)
  - convert file for converting spreadsheets from .xls to .xlsx
  - evaluate_ files for counting the found result/solution and otherPoints values.
  - To execute the openAI API scripts you need your own API key setup in an .env file. The scripts are only working with .xlsx files if you have .xls files you need to use the .xls to .xlsx converter script. The scripts are only designed for looping over a directory if you want to debug just 1 Excel File you need to delete the loop over the directory.
- Old_Results
  - Outdated result files

## Requirements

- Python 3.10+
- OpenAI API Key
