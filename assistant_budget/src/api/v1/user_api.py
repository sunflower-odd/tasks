from fastapi import APIRouter, Depends
from uuid import UUID

from assistant_budget.src.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from assistant_budget.src.repositories.users import get_user_repository, UserRepository
from assistant_budget.src.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


def get_service(
    repo: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(repo)


@router.get("/", response_model=list[UserResponse])
async def list_users(service: UserService = Depends(get_service)):
    return await service.get_all()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, service: UserService = Depends(get_service)):
    return await service.get(user_id)


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(data: UserCreate, service: UserService = Depends(get_service)):
    return await service.create(data)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    data: UserUpdate,
    service: UserService = Depends(get_service)
):
    return await service.update(user_id, data)


@router.delete("/{user_id}")
async def delete_user(user_id: UUID, service: UserService = Depends(get_service)):
    return await service.delete(user_id)