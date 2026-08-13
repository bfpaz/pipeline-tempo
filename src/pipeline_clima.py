import logging
import sys

from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
from sqlalchemy import create_engine
from extracao import coletar_clima
from transformacao import carregar_raw, listar_raws, transformar, validar
from config import POSTGRES_URL

NOME_TABELA = "clima"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

def extract() -> None:
    coletar_clima()
    logger.info("extracao concluida")

def transform() -> pd.DataFrame:
    arquivos = listar_raws()
    logger.info(f"{len(arquivos)} arquivos raw encontrados")
    if not arquivos:
        raise FileNotFoundError("nenhum arquivo raw encontrado")
    tabelas = [transformar(carregar_raw(c), origem=c.name)
               for c in arquivos]
    df = pd.concat(tabelas, ignore_index=True)
    validar(df)
    return df

def load(df: pd.DataFrame) -> None:
    engine = create_engine(POSTGRES_URL)
    df.to_sql(NOME_TABELA, engine, if_exists="replace", index=False)
    total = pd.read_sql(
        f"SELECT COUNT(*) AS n FROM {NOME_TABELA}", engine)["n"][0]
    logger.info(f"Carga concluida: {total} linhas")

def main() -> None:
    logger.info("Pipeline iniciado")
    extract()
    df = transform()
    load(df)
    logger.info("Pipeline concluido com sucesso")


if __name__ == "__main__":
    main()
