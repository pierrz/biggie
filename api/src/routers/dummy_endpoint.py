"""
All API endpoints.
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/live",
    tags=["live"],
    responses={404: {"description": "Issue with endpoint"}},
)


@router.get("/dummy", include_in_schema=False)
async def hello_karen() -> JSONResponse:
    """
    Check if the api is up
    :return: a basic response
    """
    return JSONResponse({"message": "Hello, world"})
