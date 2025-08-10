import requests
from flask import Blueprint, jsonify, abort
from datetime import datetime, timedelta

cdi_blueprint = Blueprint('cdi_controller', __name__)

@cdi_blueprint.route('/historical-data/<start_date>', methods=['GET'])
def get_cdi_historical_data(start_date):
    """
    Busca os dados históricos do CDI da API do Banco Central do Brasil.
    """
    # Código da série temporal do CDI no Banco Central.
    # A série 4389 é a taxa DI, que pode ser usada como CDI.
    bcb_series_code = '4389'

    try:
        # Converte a data inicial da string para um objeto datetime
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        abort(400, description="Formato de data inválido. Use YYYY-MM-DD.")

    # Define o período para a busca de dados (últimos 5 anos, por exemplo).
    end_date = datetime.now()

    # Formata as datas para o formato esperado pela API do BCB.
    # Ex: 01/01/2020
    start_date_str = start_date_obj.strftime('%d/%m/%Y')
    end_date_str = end_date.strftime('%d/%m/%Y')

    # Monta a URL para a API do BCB.
    api_url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{bcb_series_code}/dados?formato=json&dataInicial={start_date_str}&dataFinal={end_date_str}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()
        
        return jsonify(data)
    except requests.exceptions.RequestException as e:
        abort(500, description=f"Erro ao buscar dados do BCB: {e}")
