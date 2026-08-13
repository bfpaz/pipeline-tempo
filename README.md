# Pipeline de Dados Meteorológicos

Este projeto é um desafio da disciplina de Introdução à Engenharia de Dados. Ele implementa um pipeline ETL em **Python** que consulta a API **OpenWeatherMap** para coletar informações meteorológicas de Olinda, Paulista, Recife e Jaboatão. Os dados coletados incluem cidade, temperatura, descrição do tempo, pressão, velocidade do vento e data/hora da medição.

O projeto utiliza as bibliotecas **Requests** para consumir a API, **Pandas** para transformação e validação dos dados, e **SQLAlchemy** com **psycopg2-binary** para a carga no **PostgreSQL**. O fluxo inicia na extração, salvando uma cópia dos retornos da API em arquivos JSON na camada `data/raw`; depois, os arquivos são convertidos, têm os campos padronizados e são validados; por fim, os dados tratados são carregados na tabela `clima` do banco de dados. A transformação também gera o arquivo `data/tratada/clima_tratado.csv`.

## Como executar

1. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

2. Configure no arquivo `config.py` uma chave válida da OpenWeatherMap e a URL de conexão do PostgreSQL.

3. Execute o pipeline completo:

   ```bash
   python src/pipeline_clima.py
   ```
