from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class UserCreateRequest(BaseModel):
    name: str
    email: str
    role: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str


def create_user(name: str, email: str, role: str) -> dict:
    """Create a new user in the database with a specified role."""
    if "@" not in email:
        raise ValueError(f"Invalid email: {email}")

    user = {
        "id": hash(email) % 10000,
        "name": name,
        "email": email,
        "role": role,
    }
    return user


@router.get("/api/users/{user_id}")
async def get_user_endpoint(user_id: int):
    return {"id": user_id, "name": "Alice", "email": "alice@example.com", "role": "admin"}


@router.post("/api/v2/users", response_model=UserResponse)
async def create_user_endpoint(request: UserCreateRequest):
    try:
        user = create_user(request.name, request.email, request.role)
        return UserResponse(**user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
