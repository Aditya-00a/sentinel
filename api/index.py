"""
Vercel serverless entry point.
Re-exports the FastAPI app so Vercel can serve it.
"""
import sys
from pathlib import Path

# Add project root to path so backend imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.main import app
