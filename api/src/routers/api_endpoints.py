"""
All API endpoints.
"""
from typing import List

from fastapi import APIRouter, Depends, Request
# from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.db import models, schemas
from src.db.postgres import get_db
from src.routers.templates import templates
from starlette.responses import RedirectResponse

router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Issue with endpoint"}},
)


@router.get("/")
def main():
    return RedirectResponse(url="/docs/")


@router.get("/per_country", response_model=List[schemas.Country])
def per_country_data(db: Session = Depends(get_db)):
    data = db.query(models.Country).all()
    return data


@router.get("/per_country_ui", response_model=List[schemas.Country])
def show_per_country(request: Request, db: Session = Depends(get_db)):
    per_country_data = db.query(models.Country).all()

    return templates.TemplateResponse(
        "per_country_view.html",
        context={
            "request": request,
            "total": len(per_country_data),
            "rows": per_country_data,
            "title": "Per country report",
        },
    )
