from fastapi import Depends, APIRouter, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import sessionmaker

from database import get_db
from services.plotter import EfficiencyPlot


router = APIRouter(prefix="/plots", tags=["plots"])


@router.get("/efficiency-plot.png")
def get_efficiency_plot_image(
        test_id: int = Query(..., description="ID of the test to load"),
        plot_type: str = Query("contour", description="Type of plot: 'contour' or 'scatter'"),
        db: sessionmaker = Depends(get_db)
):
    """
    Return efficiency plot as PNG image
    """
    try:
        # Load your actual data here - using sample data for demonstration
        # df = pd.read_csv("your_data.csv") or from database
        plotter = EfficiencyPlot(db, test_id)
        image_bytes = plotter.generate_plot_image(plot_type=plot_type)

        return Response(
            content=image_bytes,
            media_type="image/png",
            headers={"Content-Disposition": "inline; filename=efficiency-plot.png"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating plot: {str(e)}")
