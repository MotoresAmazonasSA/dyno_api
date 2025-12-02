from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routers import plots, test_info


app = FastAPI(
    title="Motor Efficiency API",
    description="API for generating motor efficiency plots",
    version="1.0.0"
)

# Include routers
app.include_router(test_info.router)
app.include_router(plots.router)


@app.get("/")
def root():
    """Redirect to docs"""
    return RedirectResponse(url="/docs")


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
