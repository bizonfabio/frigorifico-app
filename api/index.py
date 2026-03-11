"""
Vercel serverless entry point for Django.
Exposes the WSGI app as "app" so the Python runtime finds it.
"""
import sys
from pathlib import Path

# Add project root so "frigorifico_app" can be imported (Django package at root)
_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_root))

from frigorifico_app.wsgi import application

app = application
