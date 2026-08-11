import json
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator

import requests

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_DIR))

from config import OPENWEATHER_API_KEY


URL = "https://api.openweathermap.org/data/2.5/weather"
CIDADES = ["Olinda,BR", "Paulista,BR", "Recife,BR", "Jaboatao,BR"]
RAW_DIR = Path("data/raw")


def salvar_raw(dados: dict) -> Path:
    """Salva os dados de uma cidade em um arquivo JSON."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    cidade = unicodedata.normalize("NFKD", dados["cidade"])
    cidade = cidade.encode("ascii", "ignore").decode().lower().replace(" ", "_")
    carimbo = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    caminho = RAW_DIR / f"clima_{cidade}_{carimbo}.json"

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    return caminho


def coletar_clima() -> Iterator[dict]:
    for cidade in CIDADES:
        params = {
            "q": cidade,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "pt_br",
        }
        resposta = requests.get(URL, params=params, timeout=10)
        resposta.raise_for_status()
        clima = resposta.json()

        yield {
            "cidade": clima["name"],
            "temperatura_c": clima["main"]["temp"],
            "descricao": clima["weather"][0]["description"],
            "pressao_hpa": clima["main"]["pressure"],
            "vento_ms": clima["wind"]["speed"],
            "dt_api": clima["dt"],
        }


if __name__ == "__main__":
    for dados_clima in coletar_clima():
        caminho = salvar_raw(dados_clima)
        print(f"Arquivo salvo: {caminho}")
