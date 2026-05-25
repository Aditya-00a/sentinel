"""
Vercel serverless entry point.
Re-exports the FastAPI app so Vercel can serve it.
"""
import sys
import os
from pathlib import Path

# Add project root to path so `backend.*` imports resolve
root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

# Load .env if present (local dev fallback; Vercel uses env vars directly)
try:
    from dotenv import load_dotenv
    load_dotenv(root / ".env")
except ImportError:
    pass

from backend.main import app
