#!/usr/bin/env python3
"""
Quick Test for AI Cost Observatory
Verifies all components are working correctly
"""

import sys
import os
import requests
import time
import subprocess
from pathlib import Path

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_python_version():
    print_header("Checking Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    if version < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    print("✅ Python version OK")
    return True

def check_dependencies():
    print_header("Checking Dependencies")
    
    required = ['requests', 'sqlalchemy', 'fastapi', 'streamlit']
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg)
            print(f"✅ {pkg}")
        except ImportError:
            print(f"❌ {pkg} (missing)")
            missing.append(pkg)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r server/requirements.txt")
        return False
    
    return True

def check_database():
    print_header("Checking Database")
    
    if os.path.exists("ai_cost_observatory.db"):
        size = os.path.getsize("ai_cost_observatory.db")
        print(f"✅ Database exists ({size} bytes)")
        return True
    else:
        print("❌ Database not found")
        print("   Run: python3 init.py")
        return False

def check_file_structure():
    print_header("Checking File Structure")
    
    required_files = [
        "README.md",
        "docker-compose.yml",
        "server/api/main.py",
        "server/database/__init__.py",
        "server/models/database.py",
        "sdk/ai_observer/__init__.py",
        "ui/dashboard.py",
        "examples/basic_openai.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (missing)")
            all_exist = False
    
    return all_exist

def test_sdk_import():
    print_header("Testing SDK Import")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent / "sdk"))
        from ai_observer import observe, log_event, configure
        print("✅ SDK imports successfully")
        print("   - observe")
        print("   - log_event")
        print("   - configure")
        return True
    except Exception as e:
        print(f"❌ SDK import failed: {e}")
        return False

def test_api_server(start_server=False):
    print_header("Testing API Server")
    
    api_url = "http://localhost:8000"
    
    # Check if server is running
    try:
        response = requests.get(f"{api_url}/health", timeout=2)
        if response.status_code == 200:
            print(f"✅ API server is running at {api_url}")
            print(f"   Response: {response.json()}")
            return True
    except requests.exceptions.RequestException:
        pass
    
    print(f"⚠️  API server not running at {api_url}")
    
    if start_server:
        print("   Starting server...")
        # This is just a check script, we won't actually start it
        print("   Run: cd server && python -m api.main")
    
    return False

def generate_test_event():
    print_header("Testing Event Creation")
    
    api_url = "http://localhost:8000"
    
    test_event = {
        "model": "gpt-4o-mini",
        "prompt_tokens": 100,
        "completion_tokens": 50,
        "total_tokens": 150,
        "latency_ms": 500,
        "input_cost": 0.000015,
        "output_cost": 0.000030,
        "total_cost": 0.000045,
        "currency": "USD",
        "project": "test-project",
        "agent": "test-agent",
        "tags": {"env": "test"}
    }
    
    try:
        response = requests.post(
            f"{api_url}/events",
            json=test_event,
            timeout=5
        )
        if response.status_code == 200:
            print("✅ Test event created successfully")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Event creation failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Could not connect to API: {e}")
        return False

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║           🔭 AI Cost Observatory - System Test            ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    results = {
        "Python Version": check_python_version(),
        "Dependencies": check_dependencies(),
        "Database": check_database(),
        "File Structure": check_file_structure(),
        "SDK Import": test_sdk_import(),
    }
    
    # Test API if available
    api_running = test_api_server()
    results["API Server"] = api_running
    
    if api_running:
        results["Event Creation"] = generate_test_event()
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(results.values())
    total = len(results)
    
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\n📚 Next steps:")
        print("   1. Start API: cd server && python -m api.main")
        print("   2. Start Dashboard: cd ui && streamlit run dashboard.py")
        print("   3. Generate sample data: python examples/generate_sample_data.py")
        print("   4. View dashboard: http://localhost:8501")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
