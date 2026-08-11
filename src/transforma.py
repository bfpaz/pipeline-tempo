import json, logging
from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")
TRATADA_DIR = Path("data/tratada")

logging.basicConfig(level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def listar_raws() -> list[Path]:
    return sorted(RAW_DIR.glob("clima_*.json"))

def carregar_raw(caminho: Path) -> dict:
    with open(caminho, encoding="utf-8") as arq:
        return json.load(arq)

def transformar(dados: dict, origem: str) -> pd.DataFrame:
    """Transforma os dados brutos de uma cidade em uma linha tipada."""
    df = pd.DataFrame([dados])

    numericas = ["temperatura_c","pressao_hpa","vento_ms"]

    for coluna in numericas:
        df[coluna] = df[coluna].astype(float)

    df["dt_api"] = pd.to_datetime(df["dt_api"], unit="s", utc=True)
    df["origem"] = origem

    return df
