# Discord: @codaxy
# Telegram: @virgingod

from typing import Optional

from pydantic import BaseModel


class Address(BaseModel):
    tipoEndereco: Optional[int] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    bairro: Optional[str] = None
    municipio: Optional[str | tuple[str, str]] = None
    siglaUf: Optional[str] = None
    pais: Optional[str] = None
    cep: Optional[str] = None


class Nationality(BaseModel):
    nacionalidade: Optional[int] = None
    municipioNascimento: Optional[str | tuple[str, str]] = None
    paisNascimento: Optional[str] = None


class Phone(BaseModel):
    ddi: Optional[str] = None
    ddd: Optional[str] = None
    numero: Optional[str] = None
    tipo: Optional[int] = None


class Person(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    cnsDefinitivo: Optional[str] = None
    dataNascimento: Optional[str] = None
    sexo: Optional[str] = None
    nomeMae: Optional[str] = None
    nomePai: Optional[str] = None
    obito: Optional[bool] = None
    racaCor: Optional[str] = None
    telefone: Optional[list[Phone]] = None
    nacionalidade: Optional[Nationality] = None
    endereco: Optional[Address] = None
 