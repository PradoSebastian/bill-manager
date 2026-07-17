# Expense Manager

Application for reading JSON files with movements from the current month and updating Excel tables with new expenses and income.

## What it does

The program:

- reads JSON files located in a folder by month,
- classifies movements into debit, income, credit, and credit USD,
- compares the records with those already existing in the Excel file,
- adds only the new movements to the corresponding tables.

## Requirements

- Python 3.12 or higher
- Project dependencies (installed automatically with `uv` or `pip`)

## Installation

Recommended with `uv`:

```bash
uv sync
```

Or with a traditional virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

## iOS Shortcut (optional)

If you also use the iPhone/iPad Shortcut named "Identificar gasto", you can use it to quickly capture a new expense and save it in the format expected by this app.

To use it correctly:

- import the Shortcut into the Apple Shortcuts app,
- run it whenever you want to register a new expense,
- make sure the generated JSON file is saved under the folder configured by `JSON_FILES_PATH` for the current month, for example:

```text
<JSON_FILES_PATH>/<current month>/
```

The shortcut should produce records with the fields expected by the importer: `tipo`, `cuenta_destino`, `valor`, `fecha`, `razon`, and `mes`. If you change the output location, update the shortcut destination or the `JSON_FILES_PATH` setting accordingly.

## Environment variables

The application reads its values from a `.env` file in the project root. The project already includes a working example, but you should adjust it if you change paths or table names.

Example `.env`:

```dotenv
JSON_FILES_PATH="C:/Assets"
EXCEL_PATH="C:/Documents/Bills.xlsx"

DEBIT_TABLE_RANGE="G3:K39"
INCOMES_TABLE_RANGE="G41:I49"

DEBIT_TABLE_NAME="Movimientos_Debito"
CREDIT_TABLE_NAME="Movimientos_Credito"
CREDIT_USD_TABLE_NAME="Movimientos_Credito_USD"

BANNED_HEADERS='["Total"]'
FLAG_HEADER="Monto"
```

### Main variables

- `JSON_FILES_PATH`: folder where the JSON files for each month are stored.
- `EXCEL_PATH`: path to the Excel file where movements will be written.
- `DEBIT_TABLE_NAME`: name of the Excel table for debit movements.
- `CREDIT_TABLE_NAME`: name of the Excel table for credit movements.
- `CREDIT_USD_TABLE_NAME`: name of the Excel table for credit USD movements.
- `FLAG_HEADER`: column used to identify whether a record should be processed.
- `BANNED_HEADERS`: headers to ignore when writing to Excel.
- `DEBIT_TABLE_RANGE`, `INCOMES_TABLE_RANGE`, `CREDIT_TABLE_RANGE`, `CREDIT_USD_TABLE_RANGE`: optional table ranges if you need to override them.

## How to run

From the project root:

```bash
uv run python -m src.gestor.main
```

If you already have the virtual environment activated:

```bash
python -m src.gestor.main
```

The script uses the current month from the system and looks for the JSON files in:

```text
<JSON_FILES_PATH>/<current month>
```

If it finds new movements, it adds them to the corresponding Excel file.
