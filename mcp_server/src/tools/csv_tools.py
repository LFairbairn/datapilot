import pandas as pd
from pathlib import Path

_df: pd.DataFrame | None = None


def load_csv(file_path: str) -> str:
    """Load a CSV file and return a summary of its contents."""
    global _df
    path = Path(file_path)
    if not path.exists():
        return f"Error: file not found at {file_path}"
    _df = pd.read_csv(path)
    col_info = ", ".join(f"{col} ({_df[col].dtype})" for col in _df.columns)
    return (
        f"Loaded {len(_df)} rows and {len(_df.columns)} columns.\n"
        f"Columns: {col_info}"
    )


def query_data(expression: str) -> str:
    """
    Query the loaded DataFrame using a pandas query expression.
    Example expressions: "Age == 'Adult'", "Running == True", "`Primary Fur Color` == 'Gray'"
    """
    if _df is None:
        return "Error: no CSV loaded. Call load_csv first."
    try:
        result = _df.query(expression)
        if result.empty:
            return "No rows matched that query."
        return (
            f"{len(result)} rows matched:\n{result.to_string(index=False, max_rows=20)}"
        )
    except Exception as e:
        return (
            f"Error running query: {e}. "
            "Column names with spaces must be wrapped in backticks, "
            "e.g. `Primary Fur Color` == 'Gray'."
        )
