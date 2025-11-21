from fastapi import APIRouter, Depends
from uuid import UUID

from assistant_budget.src.schemas.family_schema import FamilyCreate, FamilyUpdate, FamilyResponse
from assistant_budget.src.repositories.families import FamilyRepository, get_family_repository
from assistant_budget.src.services.family_service import FamilyService

router = APIRouter(prefix="/families", tags=["Families"])


def get_service(
    repo: FamilyRepository = Depends(get_family_repository)
) -> FamilyService:
    return FamilyService(repo)


@router.get("/", response_model=list[FamilyResponse])
async def list_families(service: FamilyService = Depends(get_service)):
    return await service.get_all()


@router.get("/{family_id}", response_model=FamilyResponse)
async def get_family(
    family_id: UUID,
    service: FamilyService = Depends(get_service)
):
    return await service.get(family_id)


@router.post("/", response_model=FamilyResponse, status_code=201)
async def create_family(
    data: FamilyCreate,
    service: FamilyService = Depends(get_service)
):
    return await service.create(data)


@router.patch("/{family_id}", response_model=FamilyResponse)
async def update_family(
    family_id: UUID,
    data: FamilyUpdate,
    service: FamilyService = Depends(get_service)
):
    return await service.update(family_id, data)


@router.delete("/{family_id}")
async def delete_family(
    family_id: UUID,
    service: FamilyService = Depends(get_service)
):
    return await service.delete(family_id)