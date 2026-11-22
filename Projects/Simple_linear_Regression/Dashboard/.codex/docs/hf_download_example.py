"""Ejemplo para un agente: descargar la fuente versión controlada.
No se ejecuta automáticamente; reemplaza revision con el SHA verificado.
"""
from huggingface_hub import HfApi, hf_hub_download

REPO = "Jefferson7c/Econometrics"
info = HfApi().repo_info(repo_id=REPO, repo_type="dataset", revision="main")
sha = info.sha
path = hf_hub_download(
    repo_id=REPO,
    filename="data_clean.parquet",
    repo_type="dataset",
    revision=sha,
)
print({"revision": sha, "path": path})
