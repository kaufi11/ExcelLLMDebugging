import win32com.client as win32
from pathlib import Path

INPUT_DIR = Path(r"../EUSES/spreadsheets/financial/SEEDED")
xls_files = list(INPUT_DIR.glob("*.xls"))

excel = win32.Dispatch("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False

for xls_file in xls_files:
    try:
        print(f"Converting: {xls_file.name}")
        
        wb = excel.Workbooks.Open(str(xls_file.resolve()))
        xlsx_file = INPUT_DIR / f"{xls_file.stem}.xlsx"
        wb.SaveAs(str(xlsx_file.resolve()), 51)
        wb.Close()
        
        xls_file.unlink()
        print(f"{xls_file.name} → {xlsx_file.name} (Formula!)")
        
    except Exception as e:
        print(f"Error: {e}")

excel.Quit()
