#!/usr/bin/env python3
"""
WSGI entry point for Sina production deployment
Use with Gunicorn, uWSGI, or other WSGI servers
"""

import os
from app import app, init_db

# Initialize database on startup
init_db()

# Set production environment
os.environ.setdefault('FLASK_ENV', 'production')

if __name__ == "__main__":
    app.run() 