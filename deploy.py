#!/usr/bin/env python3
"""
Sina - Production Deployment Script
Configures and runs Sina for production deployment
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        import flask
        import werkzeug
        print("✅ Dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True

def setup_environment():
    """Set up production environment variables"""
    os.environ['FLASK_ENV'] = 'production'
    os.environ['PYTHONPATH'] = str(Path.cwd())
    
    # Generate secret key if not provided
    if 'SECRET_KEY' not in os.environ:
        import secrets
        secret_key = secrets.token_hex(32)
        os.environ['SECRET_KEY'] = secret_key
        print(f"✅ Generated secret key: {secret_key[:16]}...")
    
    print("✅ Environment configured for production")

def create_directories():
    """Create necessary directories"""
    directories = ['instance', 'logs']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Directories created")

def get_network_info():
    """Get network information for deployment"""
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    # Try to get actual network IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        network_ip = s.getsockname()[0]
        s.close()
    except:
        network_ip = local_ip
    
    return local_ip, network_ip

def main():
    """Main deployment function"""
    print("🚀 Sina - Production Deployment")
    print("=" * 40)
    
    # Pre-deployment checks
    check_python_version()
    check_dependencies()
    setup_environment()
    create_directories()
    
    # Get network information
    local_ip, network_ip = get_network_info()
    
    print("\n📡 Network Information:")
    print(f"   Local access: http://127.0.0.1:5001")
    print(f"   Network access: http://{network_ip}:5001")
    print(f"   Hostname: {local_ip}")
    
    print("\n🎯 Deployment Options:")
    print("1. Local development (127.0.0.1:5001)")
    print("2. Network access (0.0.0.0:5001)")
    print("3. Custom configuration")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        host = "127.0.0.1"
        port = 5001
        debug = True
    elif choice == "2":
        host = "0.0.0.0"
        port = 5001
        debug = False
    elif choice == "3":
        host = input("Enter host (default: 0.0.0.0): ").strip() or "0.0.0.0"
        port = int(input("Enter port (default: 5001): ").strip() or "5001")
        debug = input("Enable debug mode? (y/N): ").strip().lower() == 'y'
    else:
        print("Invalid choice. Using default network configuration.")
        host = "0.0.0.0"
        port = 5001
        debug = False
    
    print(f"\n🚀 Starting Sina on {host}:{port}")
    print(f"   Debug mode: {'Enabled' if debug else 'Disabled'}")
    print(f"   Access URL: http://{network_ip if host == '0.0.0.0' else host}:{port}")
    print("\n   Press Ctrl+C to stop the server")
    print("=" * 40)
    
    # Import and run the app
    try:
        from app import app, init_db
        
        # Initialize database
        init_db()
        
        # Run the application
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Sina stopped. Thank you for building discipline!")
    except Exception as e:
        print(f"\n❌ Error starting Sina: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 