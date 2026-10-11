import logging
import pandas as pd

logger = logging.getLogger(__name__)


def remove_duplicates(df):
    """Remove duplicate rows."""
    result = df.drop_duplicates()
    logger.debug(f"remove_duplicates: {len(df)} -> {len(result)} rows")
    return result


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis == "rows":
        result = df.dropna()
        logger.debug(f"handle_missing: {len(df)} -> {len(result)} rows")
    elif axis == "columns":
        result = df.dropna(axis=1)
        logger.debug(f"handle_missing: {len(df.columns)} -> {len(result.columns)} columns")
    else:
        logger.error(f"Unsupported axis: {axis}")
        raise ValueError(f"Unsupported axis: {axis}")
    return result


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method not in ["iqr", "zscore"]:
        logger.error(f"Unsupported outlier method: {method}")
        raise ValueError(f"Unsupported outlier method: {method}")

    for col in columns:
        if col not in df.columns:
            logger.warning(f"Column not found: {col}")
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            logger.warning(f"Column is not numeric: {col}")
            continue

        before = len(df)
        if method == "iqr":
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            keep = df[col].between(q1 - threshold * iqr, q3 + threshold * iqr)
        else:
            z = (df[col] - df[col].mean()) / df[col].std()
            keep = z.abs() <= threshold
        df = df[keep]
        logger.debug(f"{col}: method={method}, threshold={threshold}, removed={before - len(df)}")

    return df


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    settings = config["processing"]
    missing = settings["missing"]
    outliers = settings["outliers"]

    if settings["remove_duplicates"]:
        df = remove_duplicates(df)
    if missing["enabled"]:
        df = handle_missing(df, missing["axis"])
    if outliers["enabled"]:
        df = remove_outliers(df, outliers["columns"], outliers["method"], outliers["threshold"])
    return df


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    return {
        "rows_before": len(df_before),
        "rows_after": len(df_after),
        "rows_removed": len(df_before) - len(df_after),
        "columns_before": len(df_before.columns),
        "columns_after": len(df_after.columns),
        "columns_removed": len(df_before.columns) - len(df_after.columns),
    }
