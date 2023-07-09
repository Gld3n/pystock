from fastapi import APIRouter

router = APIRouter(prefix="/settings", tags=["Settings"])
IVA: float = 0.16  # Taxes (16%)
EXCHANGE_RATE: float = 28.02  # USD 1.00 = BsS 28.02


@router.put("/", status_code=200, summary="Modify IVA and exchange rate")
def modify_settings(
    new_iva: float | None = None, new_exchange_rate: float | None = None
) -> str:
    if new_iva is not None:
        global IVA
        IVA = new_iva
        return f"IVA updated: {IVA*100}%"
    elif new_exchange_rate is not None:
        global EXCHANGE_RATE
        EXCHANGE_RATE = new_exchange_rate
        return f"Exchange rate updated: BsS.{EXCHANGE_RATE}"
