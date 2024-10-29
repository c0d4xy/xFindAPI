# Discord: @codaxy
# Telegram: @virgingod

import json
import random
from typing import Any

import aiohttp

from xfind.core.config import Settings
from xfind.services.aiohttp_helper import AiohttpHelper
from xfind.sipni_sdk.exceptions import (
    InvalidCpf,
    InvalidSipniLogin,
    InvalidSipniToken,
    PersonNotFound,
)
from xfind.sipni_sdk.models.person import Person
from xfind.sipni_sdk.models.token import Token


class SipniSDK:
    _email = Settings.SIPNI_EMAIL
    _password = Settings.SIPNI_PASSWORD

    session = AiohttpHelper.get_session()

    async def get_access_token(self) -> Token:
        headers = {
            "accept": "application/json",
            "DNT": "1",
            "Referer": "https://si-pni.saude.gov.br/",
            "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
            "X-Authorization": aiohttp.BasicAuth(
                self._email, self._password, "utf-8"
            ).encode(),
        }

        url = "https://servicos-cloud.saude.gov.br/pni-bff/v1/autenticacao/tokenAcesso"

        async with self.session.post(url=url, headers=headers) as response:
            if response.status != 200:
                parsed_response = await response.json()

                if parsed_response["erro-mensagem"] == "Authentication":
                    raise InvalidSipniLogin("Credenciais inválidas")

                raise Exception("Erro ao gerar token de acesso do SIPNI")

            return Token(**await response.json())

    class CpfQuery:
        def __init__(
            self,
            session: aiohttp.ClientSession,
            config_path: str = "xfind/sipni_sdk/config.json",
        ) -> None:
            self.session = session
            self.config_path = config_path
            self._config = self._load_config()
            self._bearer_token = self._config.get("sipni_token", "")

        def _load_config(self) -> Any:
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except FileNotFoundError:
                print("Arquivo de configuração não encontrado. Criando novo arquivo.")
                return {"sipni_token": ""}
            except json.JSONDecodeError as e:
                print(f"Erro ao decodificar o arquivo de configuração: {str(e)}")
                raise

        def _save_config(self) -> None:
            try:
                with open(self.config_path, "w", encoding="utf-8") as f:
                    json.dump(self._config, f, ensure_ascii=False, indent=4)
            except IOError as e:
                print(f"Erro ao salvar o arquivo de configuração: {str(e)}")
                raise

        def _make_headers(self):
            return {
                "User-Agent": f"Mozilla/5.0 (Windows NT {random.randint(11, 99)}.0; Win64; x64) "
                f"AppleWebKit/{random.randint(111, 991)}.{random.randint(11, 99)} "
                f"(KHTML, like Gecko) Chrome/{random.randint(11, 99)}.0.0.0 Safari/537.36",
                "Authorization": f"Bearer {self._bearer_token}",
                "DNT": "1",
                "Referer": "https://si-pni.saude.gov.br/",
            }

        def sanitize_cpf(self, cpf: str) -> str:
            return "".join([char for char in cpf if char.isdigit()])

        def validate_cpf(self, cpf: str):
            if len(cpf) != 11:
                raise InvalidCpf("CPF inválido")

        async def _generate_new_token(self):
            sdk = SipniSDK()
            auth_response = await sdk.get_access_token()

            self._config["sipni_token"] = auth_response.accessToken
            self._save_config()
            self._bearer_token = self._config["sipni_token"]

        async def _query_municipio(self, municipio_id: str) -> tuple[str, str] | None:
            url = f"https://servicos-cloud.saude.gov.br/pni-bff/v1/municipio/{municipio_id}"
            headers = self._make_headers()

            async with self.session.get(url=url, headers=headers) as response:
                if response.status == 200:
                    parsed_response = await response.json()
                    return (
                        parsed_response["record"]["nome"],
                        parsed_response["record"]["siglaUf"],
                    )
                else:
                    return None

        async def _query_racacor(self, raca_id: str) -> str | None:
            url = f"https://servicos-cloud.saude.gov.br/pni-bff/v1/racacor/{raca_id}"
            headers = self._make_headers()

            async with self.session.get(url=url, headers=headers) as response:
                if response.status == 200:
                    parsed_response = await response.json()
                    return parsed_response["record"]["descricao"]
                else:
                    return None

        async def xfind_cpf_query(self, cpf: str) -> Person:
            cpf = self.sanitize_cpf(cpf)
            self.validate_cpf(cpf)

            url = f"https://servicos-cloud.saude.gov.br/pni-bff/v1/cidadao/cpf/{cpf}"
            headers = self._make_headers()

            async with self.session.get(url=url, headers=headers) as response:
                if response.status == 401:
                    await self._generate_new_token()
                    raise InvalidSipniToken(
                        "Token inválido. Gerando novo token de acesso..."
                    )

                elif response.status == 200:
                    parsed_response = await response.json()

                    if "records" not in parsed_response:
                        raise PersonNotFound

                    person = Person(**parsed_response["records"][0])

                    if person.racaCor is not None:
                        raca = await self._query_racacor(person.racaCor)
                        person.racaCor = raca if raca != "SEM INFORMACAO" else None

                    if person.nacionalidade.municipioNascimento is not None:  # type: ignore
                        municipio_nascimento = await self._query_municipio(person.nacionalidade.municipioNascimento)  # type: ignore
                        person.nacionalidade.municipioNascimento = municipio_nascimento if municipio_nascimento != "SEM INFORMACAO" else None  # type: ignore

                    if person.endereco.municipio is not None:  # type: ignore
                        municipio = await self._query_municipio(person.endereco.municipio)  # type: ignore
                        person.endereco.municipio = municipio if municipio != "SEM INFORMACAO" else None  # type: ignore

                    return person
                else:
                    raise Exception("Ocorreu um erro inesperado")
