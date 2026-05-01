from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class UserCreateRequest(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


def create_user(name: str, email: str) -> dict:
    """Create a new user in the database."""
    # Validate email format
    if "@" not in email:
        raise ValueError(f"Invalid email: {email}")

    user = {
        "id": hash(email) % 10000,
        "name": name,
        "email": email,
    }
    return user


@router.get("/api/users/{id}")
async def get_user_endpoint(id: int):
    return {"id": id, "name": "Alice", "email": "alice@example.com"}


@router.post("/api/users", response_model=UserResponse)
async def create_user_endpoint(request: UserCreateRequest):
    try:
        user = create_user(request.name, request.email)
        return UserResponse(**user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
