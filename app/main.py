"""
Main FastAPI application entry point with authentication routes
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import user, product, category, customer, supplier, sale, purchase, expense, invoice
from app.routes import auth

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Powered ERP System",
    description="Intelligent accounting and inventory management system",
    version="0.1.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth.router)

# Health check endpoint
@app.get("/")
def read_root():
    return {
        "message": "AI-Powered ERP System Running",
        "status": "operational",
        "version": "0.1.0",
        "docs": "/api/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "erp-system"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
