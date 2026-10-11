# MP1 Data Pipeline

This project is a command-line data pipeline that loads a dataset, validates it, cleans it according to a YAML configuration, and saves the result as a CSV file. Data moves through five stages in order: the input and config paths are checked, the files are loaded, the data is validated, the enabled cleaning steps are applied, and the cleaned DataFrame is written to disk. `pipeline.py` coordinates this workflow and contains no data-handling logic of its own. The `src/` package holds the modules: `utils.py` sets up logging and checks that input files exist, `data_loaders.py` reads CSV, JSON, and YAML files based on their extension, and `data_validator.py` confirms required columns are present and removes rows with non-numeric values in numeric columns. `data_processor.py` removes duplicates, missing values, and outliers, and builds a summary report of the cleaning results. `data_output.py` saves the cleaned data and creates the output directory if needed. All column names and cleaning choices live in `config/config.yaml`, so the pipeline can run on a different compatible CSV by editing the configuration rather than the code.

## Usage

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

## Example Output

```
INFO     src.utils — Input file validated: fixtures/sample_data.csv
INFO     src.utils — Input file validated: config/config.yaml
INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
INFO     src.data_loaders — Loaded YAML file: config/config.yaml
WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
DEBUG    src.data_validator — Validation: 100 -> 98 rows (2 removed)
INFO     __main__ — Validation complete: 100 -> 98 rows
DEBUG    src.data_processor — remove_duplicates: 98 -> 96 rows
DEBUG    src.data_processor — handle_missing: 96 -> 94 rows
DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, removed=2
INFO     __main__ — Processing complete: 98 -> 92 rows
DEBUG    src.data_output — Saved 92 rows to output/clean.csv
INFO     __main__ — Saved cleaned data to output/clean.csv
Cleaning report:
{'rows_before': 98,
 'rows_after': 92,
 'rows_removed': 6,
 'columns_before': 5,
 'columns_after': 5,
 'columns_removed': 0}
```
