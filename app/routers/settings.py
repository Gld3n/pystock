from fastapi import APIRouter

router = APIRouter(prefix="/settings", tags=["Settings"])
IVA: float = 0.16  # Taxes (16%)
exchange_rate: float = 28.02  # USD 1.00 = BsS 28.02


@router.put("/", status_code=200, summary="Modify IVA and exchange rate")
def modify_settings():
    return {"message": "Modify settings"}
