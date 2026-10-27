import argparse
import logging
import sys
from pprint import pprint

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--config", "-c", required=True)
    parser.add_argument("--output", "-o", required=True)
    parser.add_argument("--verbose", "-v", action="store_true")
    return parser.parse_args()


def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(f"Arguments parsed: input={args.input}, config={args.config}, output={args.output}")

    if not validate_input(args.input) or not validate_input(args.config):
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]

    loaded_rows = len(data)
    try:
        data = validate_dataframe(data, required_columns, numeric_columns)
    except ValueError:
        sys.exit(1)
    logger.info(f"Validation complete: {loaded_rows} -> {len(data)} rows")

    original = data.copy()
    try:
        cleaned = process_data(data, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(original, cleaned)
    logger.info(f"Processing complete: {len(original)} -> {len(cleaned)} rows")

    output_path = save_data(cleaned, args.output)
    logger.info(f"Saved cleaned data to {output_path}")

    print("Cleaning report:")
    pprint(report, sort_dicts=False)


if __name__ == "__main__":
    main()

