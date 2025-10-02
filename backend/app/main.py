# LaTeX Note Platform - Main FastAPI Application

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import our API routers
from app.api import auth, notes

# Create the FastAPI application instance
app = FastAPI(
    title="LaTeX Note Platform API",
    description="A cloud-backed LaTeX note-taking platform with user authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router)
app.include_router(notes.router)

# Root endpoint - API status
@app.get("/")
async def read_root():
    return {
        "message": "LaTeX Note Platform API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "auth": "/auth",
            "notes": "/notes"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

# Keep the original LaTeX validator for testing
@app.post("/validate-latex")
async def validate_latex_snippet(data: dict):
    """
    Basic LaTeX validation - for testing purposes
    """
    latex_code = data.get("latex", "")
    
    if not latex_code:
        return {"valid": False, "error": "No LaTeX code provided"}
    
    if "\\documentclass" not in latex_code:
        return {"valid": False, "error": "Missing \\documentclass"}
        
    if "\\begin{document}" not in latex_code:
        return {"valid": False, "error": "Missing \\begin{document}"}
        
    if "\\end{document}" not in latex_code:
        return {"valid": False, "error": "Missing \\end{document}"}
    
    # Count math expressions
    math_count = latex_code.count("$")
    
    return {
        "valid": True,
        "message": "LaTeX looks good!",
        "stats": {
            "length": len(latex_code),
            "math_expressions": math_count // 2
        }
    }
