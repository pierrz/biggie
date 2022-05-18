"""
All API endpoints.
"""

import pandas as pd
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from src.db.mongo import db
from src.routers import templates

router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Issue with endpoint"}},
)


@router.get("/live", include_in_schema=False)
async def api_live() -> JSONResponse:
    """
    Check if the api is up
    :return: a basic response
    """
    return JSONResponse({"message": "Hello, World"})


def get_data(sort_column: str, page_size: int = None):
    db_data = db.character.find()
    columns = ["name", "comics_available"]
    df = pd.DataFrame(db_data)
    total = df.shape[0]

    order = True
    if sort_column == columns[1]:
        order = False
    data = df[columns].sort_values(by=[sort_column], ascending=order).to_dict("records")

    if page_size is not None:
        return [
            data[i : i + page_size]  # noqa: E203,E226
            for i in range(0, len(data), page_size)
        ], total

    return data, total


@router.get("/comics_per_characters")
async def comics_per_characters(request: Request, sort_column: str):
    """
    see all characters and the quantity of comics in which they appear:
    character name: text
    quantity of comics they appear in: int

    :param request: query request
    :param sort_column: column to sort the data with, either 'name' or 'comics_available'
    :return: displays the desired table
    """

    rows, total = get_data(sort_column)

    return templates.TemplateResponse(
        "characters_view.html",
        context={
            "request": request,
            "total": total,
            "rows": rows,
            "title": "Marvel characters",
        },
    )


@router.get("/comics_per_characters/paginated")
async def comics_per_characters_paginated(
    request: Request, sort_column: str
) -> JSONResponse:
    """
    WIP (active page button): Same as previous endpoint but with paginated UI
    """

    limit = 100
    pages, total = get_data(sort_column, limit)

    return templates.TemplateResponse(
        "characters_view_paginated.html",
        context={
            "request": request,
            "total": total,
            "pages": pages,
            "limit": limit,
            "title": "Marvel characters",
        },
    )
