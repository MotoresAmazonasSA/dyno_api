import pandas as pd
import io
from fastapi import Depends, APIRouter, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import sessionmaker

from database import get_db
from services.plotter import fetch_test_info, EfficiencyPlot

from typing import List

from schemas.scadalts import TestInfoR

router = APIRouter(prefix="/test_info", tags=["test"])


@router.get("/", response_model=List[TestInfoR])
def get_test_info(
        db: sessionmaker = Depends(get_db)
):
    """
    Return efficiency plot as PNG image
    """
    response = fetch_test_info(db)
    return response

@router.get("/download_test_csv")
def get_efficiency_plot_image(
        test_id: int = Query(..., description="ID of the test to load"),
        db: sessionmaker = Depends(get_db)
):
    """
    Return a csv file of a test
    """
    try:
        # Load your actual data here - using sample data for demonstration
        # df = pd.read_csv("your_data.csv") or from database
        plotter = EfficiencyPlot(db, test_id)
        buf = io.StringIO()
        plotter.df.to_csv(buf, index=False)
        buf.seek(0)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating csv: {str(e)}")

    return Response(
        content=buf.getvalue(),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=efficiency_data.csv"
        }
    )
