"""
Vercel serverless entry point for Django.
Exposes the WSGI app as "app" so the Python runtime finds it.
"""
import sys
from pathlib import Path

# Add venv (Django project root) to path so "frigorifico_app" can be imported
_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_root))
sys.path.insert(0, str(_root / "venv"))

from frigorifico_app.wsgi import application

app = application
