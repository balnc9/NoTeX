# This is the entry point, where FastAPI starts
from fastapi import FastAPI 

# Create the FastAPI application instance
app = FastAPI(
    title="LaTeX Note Platform",
    description="A cloud-backed LaTeX note-taking platform",
    version="1.0.0"
)

# Root endpoint - this will be our "Hello World"
@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the LaTeX Note Platform!",
        "status": "running",
        "version": "1.0.0"
    }

# Health check endpoint - useful for monitoring
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Simple test endpoint that accepts parameters
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello, {name}! Ready to take some LaTeX notes?"}

# POST endpoint - accepts JSON data in request body
@app.post("/validate-latex")
async def validate_latex_snippet(data: dict):
    """
    Takes LaTeX code and does basic validation
    This is a preview of what we'll build for real LaTeX processing!
    """
    latex_code = data.get("latex", "")
    
    # Basic validation (we'll make this much more sophisticated later)
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
            "math_expressions": math_count // 2  # Pairs of $...$
        }
    }
