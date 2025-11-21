from fastapi import APIRouter
from assistant_budget.src.schemas.misc_schema import BudgetSchema
from assistant_budget.src.configs.app import settings

router = APIRouter()

@router.get("/health", response_model=BudgetSchema)
async def health():
    return BudgetSchema(
        status="ok",
        version=settings.app.app_version,
    )