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
    colunas_traduzidas = {
        "name": "cidade",
        "temp": "temperatura_c",
        "description": "descricao",
        "pressure": "pressao_hpa",
        "speed": "vento_ms",
        "dt": "data_hora",
    }

    numericas = ["temp","pressure","speed"]

    for coluna in numericas:
        df[coluna] = df[coluna].astype(float)

    df["dt"] = pd.to_datetime(df["dt"], unit="s", utc=True).dt.tz_convert(
        "America/Recife"
    ).dt.strftime("%Y-%m-%d %H:%M:%S")
    df["origem"] = origem

    return df.rename(columns=colunas_traduzidas)

def validar(df: pd.DataFrame) -> None:
    obrigatorias = ["cidade", "temperatura_c"]
    for coluna in obrigatorias:
        if coluna not in df.columns:
            raise ValueError(f"coluna ausente: {coluna}")
        if df[coluna].isna().any():
            raise ValueError(f"coluna com nulo: {coluna}")
    if (df["temperatura_c"] <= 0).any():
        raise ValueError("temperatura <= 0: dado suspeito, carga abortada")
    logger.info("validacao ok: %d linhas integras", len(df))


def main() -> None:
    caminhos_raw = listar_raws()
    if not caminhos_raw:
        logger.warning(f"Nenhum arquivo raw encontrado em {RAW_DIR}")
        return

    dataframes = [
        transformar(carregar_raw(caminho), caminho.name)
        for caminho in caminhos_raw
    ]
    dados_tratados = pd.concat(dataframes, ignore_index=True)
    validar(dados_tratados)

    TRATADA_DIR.mkdir(parents=True, exist_ok=True)
    caminho_saida = TRATADA_DIR / "clima_tratado.csv"
    dados_tratados.to_csv(caminho_saida, index=False, encoding="utf-8")
    logger.info(f"Arquivo tratado salvo: {caminho_saida}")


if __name__ == "__main__":
    main()
