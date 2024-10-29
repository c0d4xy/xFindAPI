# Discord: @codaxy
# Telegram: @virgingod

from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from xfind.services.cryptograph.jwt_barrer import verify_token
from xfind.sipni_sdk import SipniSDK
from xfind.sipni_sdk.exceptions import (
    InvalidCpf,
    InvalidSipniToken,
    PersonNotFound,
)
from xfind.sipni_sdk.models.person import Person as SipniPerson

router = APIRouter()


@router.get("/cpf", response_model=SipniPerson, dependencies=[Depends(verify_token)])
async def get_person_by_cpf(token_payload: dict[str, Any] = Depends(verify_token)):

    cpf = token_payload.get("cpf")
    if not cpf:
        raise HTTPException(status_code=401, detail="JWT inválido: campo 'cpf' ausente")

    sdk = SipniSDK()

    try:
        cpf_query = SipniSDK.CpfQuery(session=sdk.session)
        person_data = await cpf_query.xfind_cpf_query(cpf)
        return person_data
    except InvalidCpf:
        raise HTTPException(status_code=400, detail="CPF Inválido")
    except PersonNotFound:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    except InvalidSipniToken:
        raise HTTPException(
            status_code=503,
            detail="Ocorreu um erro interno ao consultar os dados. Tente novamente...",
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
