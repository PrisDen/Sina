#!/usr/bin/env python3
"""
Sina - The Disciplined Mentor
Startup Script

This script initializes the database and starts the Flask application.
"""

import os
import sys
import webbrowser
import time
from threading import Timer

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import flask
        from werkzeug.security import generate_password_hash
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def create_directories():
    """Create necessary directories if they don't exist."""
    directories = ['instance', 'static/css', 'static/js', 'templates']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created directory: {directory}")

def open_browser():
    """Open the default web browser to the application URL."""
    webbrowser.open('http://127.0.0.1:5000')

def main():
    """Main startup function."""
    print("🧠 Starting Sina - The Disciplined Mentor")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Import and run the Flask app
    try:
        from app import app, init_db
        
        # Initialize database
        print("📊 Initializing database...")
        init_db()
        print("✓ Database initialized")
        
        # Schedule browser opening
        Timer(2.0, open_browser).start()
        
        print("\n🚀 Starting Sina application...")
        print("📱 Open your browser to: http://127.0.0.1:5000")
        print("🛑 Press Ctrl+C to stop the application")
        print("=" * 50)
        
        # Start the Flask application
        app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
        
    except ImportError:
        print("✗ Could not import Flask application")
        print("Make sure app.py exists in the current directory")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Sina says goodbye! Remember, discipline is a daily choice.")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 