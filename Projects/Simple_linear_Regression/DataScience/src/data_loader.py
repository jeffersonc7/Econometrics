from pathlib import Path

import pandas as pd
from huggingface_hub import hf_hub_download


def load_data(filename, repo_id="Jefferson7c/Econometrics", revision="main"):
    """Download a CSV, Parquet, or ODS file and return a DataFrame."""
    extension = Path(filename).suffix.lower()
    if extension not in {".csv", ".parquet", ".ods"}:
        raise ValueError(f"Unsupported file format: {extension}")

    file_path = hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        repo_type="dataset",
        revision=revision,
    )

    if extension == ".csv":
        return pd.read_csv(file_path, sep=";", low_memory=False)
    if extension == ".parquet":
        return pd.read_parquet(file_path)
    return pd.read_excel(file_path, engine="odf")