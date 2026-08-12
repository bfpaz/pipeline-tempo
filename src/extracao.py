import json
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
import requests

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_DIR))

from config import OPENWEATHER_API_KEY


URL = "https://api.openweathermap.org/data/2.5/weather"
CIDADES = ["Olinda,BR", "Paulista,BR", "Recife,BR", "Jaboatao,BR"]
RAW_DIR = Path("data/raw")


def salvar_raw(dados: dict) -> Path:
    """Salva a resposta bruta da API em um arquivo JSON."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    cidade = unicodedata.normalize("NFKD", dados["name"])
    cidade = cidade.encode("ascii", "ignore").decode().lower().replace(" ", "_")
    carimbo = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    caminho = RAW_DIR / f"clima_{cidade}_{carimbo}.json"

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)

    return caminho


def coletar_clima() -> None:
    """Coleta os dados climáticos e salva cada resposta na camada raw."""
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

        dados = {
            "name": clima["name"],
            "temp": clima["main"]["temp"],
            "description": clima["weather"][0]["description"],
            "pressure": clima["main"]["pressure"],
            "speed": clima["wind"]["speed"],
            "dt": clima["dt"],
        }
        caminho = salvar_raw(dados)
        print(f"Arquivo salvo: {caminho}")


if __name__ == "__main__":
    coletar_clima()
