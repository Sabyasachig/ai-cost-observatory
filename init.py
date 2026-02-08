#!/usr/bin/env python3
"""
Initialize AI Cost Observatory
Sets up the database and creates necessary directories
"""

import os
import sys

def main():
    print("🔭 AI Cost Observatory - Initialization")
    print("=" * 50)
    print()
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return 1
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check current directory
    if not os.path.exists("server"):
        print("❌ Please run this script from the project root directory")
        return 1
    
    print("✅ Project root directory detected")
    
    # Initialize database
    print("\n📦 Initializing database...")
    try:
        sys.path.insert(0, os.path.join(os.getcwd(), "server"))
        from database import init_db
        init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return 1
    
    # Create .env if not exists
    if not os.path.exists(".env"):
        print("\n📝 Creating .env file...")
        try:
            with open(".env.example", "r") as src:
                content = src.read()
            with open(".env", "w") as dst:
                dst.write(content)
            print("✅ .env file created (please update with your API keys)")
        except Exception as e:
            print(f"⚠️  Could not create .env file: {e}")
    else:
        print("\n✅ .env file already exists")
    
    print("\n" + "=" * 50)
    print("🎉 Initialization complete!")
    print()
    print("Next steps:")
    print("1. Update .env with your API keys")
    print("2. Start the API server:")
    print("   cd server && python -m api.main")
    print("3. Start the dashboard (new terminal):")
    print("   cd ui && streamlit run dashboard.py")
    print("4. Run an example:")
    print("   python examples/generate_sample_data.py")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
