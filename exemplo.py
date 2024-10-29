# Discord: @codaxy
# Telegram: @virgingod

import json

import requests

from xfind.core.config import Settings
from xfind.services.cryptograph.jwt_helper import JwtHelper

jwt_helper = JwtHelper(Settings.JWT_TOKEN_SECRET)


def get_person_by_cpf(token: str):
    url = "http://127.0.0.1:8080/v1/query/cpf"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 400:
        print("Erro: CPF inválido.")
    elif response.status_code == 401:
        print("Erro: Token inválido.")
    elif response.status_code == 404:
        print("Erro: Pessoa não encontrada.")
    else:
        print("Erro inesperado:", response.status_code, response.text)


if __name__ == "__main__":
    cpf_input = ""
    jwt_token = jwt_helper.encode({"cpf": cpf_input})

    person_data = get_person_by_cpf(jwt_token)
    if person_data:
        print(json.dumps(person_data, indent=4, ensure_ascii=False))
