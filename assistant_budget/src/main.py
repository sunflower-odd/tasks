from fastapi import FastAPI
from assistant_budget.src.api.v1 import (
    category_api,
    user_api,
    family_api,
    expense_api,
    expense_participant_api,
    misc
)

app = FastAPI(title="Assistant Budget API")

app.include_router(category_api.router)
app.include_router(user_api.router)
app.include_router(family_api.router)
app.include_router(expense_api.router)
app.include_router(expense_participant_api.router)
app.include_router(misc.router)