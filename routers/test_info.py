from fastapi import Depends, APIRouter, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import sessionmaker

from database import get_db
from services.plotter import fetch_test_info


router = APIRouter(prefix="/test_info", tags=["test"])


@router.get("/")
def get_test_info(
        db: sessionmaker = Depends(get_db)
):
    """
    Return efficiency plot as PNG image
    """
    response = fetch_test_info(db)
    return response
