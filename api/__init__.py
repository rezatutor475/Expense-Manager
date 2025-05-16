"""
API package initializer.
Sets up FastAPI app instance, includes routers, and configures middleware and event handlers.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from .routes import expense_routes

# Create the FastAPI app
app = FastAPI(
    title="Expense Management API",
    description="API for managing personal and business expenses.",
    version="1.0.0"
)

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(expense_routes.router, prefix="/expenses", tags=["Expenses"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Expense Management API"}

# Custom exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."},
    )

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    logging.info("Starting Expense Management API...")

@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Shutting down Expense Management API...")
